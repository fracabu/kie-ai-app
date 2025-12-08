[![Logo](https://files.buildwithfern.com/openrouter.docs.buildwithfern.com/docs/5a7e2b0bd58241d151e9e352d7a4f898df12c062576c0ce0184da76c3635c5d3/content/assets/logo.svg)![Logo](https://files.buildwithfern.com/openrouter.docs.buildwithfern.com/docs/6f95fbca823560084c5593ea2aa4073f00710020e6a78f8a3f54e835d97a8a0b/content/assets/logo-white.svg)](https://openrouter.ai/)

Search
`/`
Ask AI

[Models](https://openrouter.ai/models) [Chat](https://openrouter.ai/chat) [Ranking](https://openrouter.ai/rankings) [Docs](https://openrouter.ai/docs/api-reference/overview)

[Docs](https://openrouter.ai/docs/quickstart) [API Reference](https://openrouter.ai/docs/api/reference/overview) [SDK Reference](https://openrouter.ai/docs/sdks/typescript/overview)

[Docs](https://openrouter.ai/docs/quickstart) [API Reference](https://openrouter.ai/docs/api/reference/overview) [SDK Reference](https://openrouter.ai/docs/sdks/typescript/overview)

- API Guides

  - [Overview](https://openrouter.ai/docs/api/reference/overview)
  - [Streaming](https://openrouter.ai/docs/api/reference/streaming)
  - [Embeddings](https://openrouter.ai/docs/api/reference/embeddings)
  - [Limits](https://openrouter.ai/docs/api/reference/limits)
  - [Authentication](https://openrouter.ai/docs/api/reference/authentication)
  - [Parameters](https://openrouter.ai/docs/api/reference/parameters)
  - [Errors](https://openrouter.ai/docs/api/reference/errors)
  - Responses API
- API Reference

  - Responses

  - OAuth

  - Analytics

  - Credits

  - Embeddings

  - Generations

  - Models

  - Endpoints

  - Parameters

  - Providers

  - API Keys

  - Chat

  - Completions

[Models](https://openrouter.ai/models) [Chat](https://openrouter.ai/chat) [Ranking](https://openrouter.ai/rankings) [Docs](https://openrouter.ai/docs/api-reference/overview)

System

On this page

- [Requests](https://openrouter.ai/docs/api/reference/overview#requests)
- [Completions Request Format](https://openrouter.ai/docs/api/reference/overview#completions-request-format)
- [Headers](https://openrouter.ai/docs/api/reference/overview#headers)
- [Assistant Prefill](https://openrouter.ai/docs/api/reference/overview#assistant-prefill)
- [Responses](https://openrouter.ai/docs/api/reference/overview#responses)
- [CompletionsResponse Format](https://openrouter.ai/docs/api/reference/overview#completionsresponse-format)
- [Finish Reason](https://openrouter.ai/docs/api/reference/overview#finish-reason)
- [Querying Cost and Stats](https://openrouter.ai/docs/api/reference/overview#querying-cost-and-stats)

[API Guides](https://openrouter.ai/docs/api/reference/overview)

# API Reference

Copy page

An overview of OpenRouter's API

OpenRouter’s request and response schemas are very similar to the OpenAI Chat API, with a few small differences. At a high level, **OpenRouter normalizes the schema across models and providers** so you only need to learn one.

## Requests

### Completions Request Format

Here is the request schema as a TypeScript type. This will be the body of your `POST` request to the `/api/v1/chat/completions` endpoint (see the [quick start](https://openrouter.ai/docs/quick-start) above for an example).

For a complete list of parameters, see the [Parameters](https://openrouter.ai/docs/api-reference/parameters).

Request Schema

```
// Definitions of subtypes are below
type Request = {
  // Either "messages" or "prompt" is required
  messages?: Message[];
  prompt?: string;

  // If "model" is unspecified, uses the user's default
  model?: string; // See "Supported Models" section

  // Allows to force the model to produce specific output format.
  // See models page and note on this docs page for which models support it.
  response_format?: { type: 'json_object' };

  stop?: string | string[];
  stream?: boolean; // Enable streaming

  // See LLM Parameters (openrouter.ai/docs/api-reference/parameters)
  max_tokens?: number; // Range: [1, context_length)\
  temperature?: number; // Range: [0, 2]\
\
  // Tool calling\
  // Will be passed down as-is for providers implementing OpenAI's interface.\
  // For providers with custom interfaces, we transform and map the properties.\
  // Otherwise, we transform the tools into a YAML template. The model responds with an assistant message.\
  // See models supporting tool calling: openrouter.ai/models?supported_parameters=tools\
  tools?: Tool[];\
  tool_choice?: ToolChoice;\
\
  // Advanced optional parameters\
  seed?: number; // Integer only\
  top_p?: number; // Range: (0, 1]
  top_k?: number; // Range: [1, Infinity) Not available for OpenAI models\
  frequency_penalty?: number; // Range: [-2, 2]\
  presence_penalty?: number; // Range: [-2, 2]\
  repetition_penalty?: number; // Range: (0, 2]
  logit_bias?: { [key: number]: number };
  top_logprobs: number; // Integer only
  min_p?: number; // Range: [0, 1]
  top_a?: number; // Range: [0, 1]

  // Reduce latency by providing the model with a predicted output
  // https://platform.openai.com/docs/guides/latency-optimization#use-predicted-outputs
  prediction?: { type: 'content'; content: string };

  // OpenRouter-only parameters
  // See "Prompt Transforms" section: openrouter.ai/docs/transforms
  transforms?: string[];
  // See "Model Routing" section: openrouter.ai/docs/model-routing
  models?: string[];
  route?: 'fallback';
  // See "Provider Routing" section: openrouter.ai/docs/provider-routing
  provider?: ProviderPreferences;
  user?: string; // A stable identifier for your end-users. Used to help detect and prevent abuse.
};

// Subtypes:

type TextContent = {
  type: 'text';
  text: string;
};

type ImageContentPart = {
  type: 'image_url';
  image_url: {
    url: string; // URL or base64 encoded image data
    detail?: string; // Optional, defaults to "auto"
  };
};

type ContentPart = TextContent | ImageContentPart;

type Message =
  | {
      role: 'user' | 'assistant' | 'system';
      // ContentParts are only for the "user" role:
      content: string | ContentPart[];
      // If "name" is included, it will be prepended like this
      // for non-OpenAI models: `{name}: {content}`
      name?: string;
    }
  | {
      role: 'tool';
      content: string;
      tool_call_id: string;
      name?: string;
    };

type FunctionDescription = {
  description?: string;
  name: string;
  parameters: object; // JSON Schema object
};

type Tool = {
  type: 'function';
  function: FunctionDescription;
};

type ToolChoice =
  | 'none'
  | 'auto'
  | {
      type: 'function';
      function: {
        name: string;
      };
    };
```

The `response_format` parameter ensures you receive a structured response from the LLM. The parameter is only supported by OpenAI models, Nitro models, and some others - check the providers on the model page on openrouter.ai/models to see if it’s supported, and set `require_parameters` to true in your Provider Preferences. See [Provider Routing](https://openrouter.ai/docs/features/provider-routing)

### Headers

OpenRouter allows you to specify some optional headers to identify your app and make it discoverable to users on our site.

- `HTTP-Referer`: Identifies your app on openrouter.ai
- `X-Title`: Sets/modifies your app’s title

TypeScript

```
fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer <OPENROUTER_API_KEY>',
    'HTTP-Referer': '<YOUR_SITE_URL>', // Optional. Site URL for rankings on openrouter.ai.
    'X-Title': '<YOUR_SITE_NAME>', // Optional. Site title for rankings on openrouter.ai.
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-4o',
    messages: [\
      {\
        role: 'user',\
        content: 'What is the meaning of life?',\
      },\
    ],
  }),
});
```

##### Model routing

If the `model` parameter is omitted, the user or payer’s default is used.
Otherwise, remember to select a value for `model` from the [supported\\
models](https://openrouter.ai/models) or [API](https://openrouter.ai/api/v1/models), and include the organization
prefix. OpenRouter will select the least expensive and best GPUs available to
serve the request, and fall back to other providers or GPUs if it receives a
5xx response code or if you are rate-limited.

##### Streaming

[Server-Sent Events\\
(SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format)
are supported as well, to enable streaming _for all models_. Simply send
`stream: true` in your request body. The SSE stream will occasionally contain
a “comment” payload, which you should ignore (noted below).

##### Non-standard parameters

If the chosen model doesn’t support a request parameter (such as `logit_bias`
in non-OpenAI models, or `top_k` for OpenAI), then the parameter is ignored.
The rest are forwarded to the underlying model API.

### Assistant Prefill

OpenRouter supports asking models to complete a partial response. This can be useful for guiding models to respond in a certain way.

To use this features, simply include a message with `role: "assistant"` at the end of your `messages` array.

TypeScript

```
fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer <OPENROUTER_API_KEY>',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-4o',
    messages: [\
      { role: 'user', content: 'What is the meaning of life?' },\
      { role: 'assistant', content: "I'm not sure, but my best guess is" },\
    ],
  }),
});
```

## Responses

### CompletionsResponse Format

OpenRouter normalizes the schema across models and providers to comply with the [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat).

This means that `choices` is always an array, even if the model only returns one completion. Each choice will contain a `delta` property if a stream was requested and a `message` property otherwise. This makes it easier to use the same code for all models.

Here’s the response schema as a TypeScript type:

TypeScript

```
// Definitions of subtypes are below
type Response = {
  id: string;
  // Depending on whether you set "stream" to "true" and
  // whether you passed in "messages" or a "prompt", you
  // will get a different output shape
  choices: (NonStreamingChoice | StreamingChoice | NonChatChoice)[];
  created: number; // Unix timestamp
  model: string;
  object: 'chat.completion' | 'chat.completion.chunk';

  system_fingerprint?: string; // Only present if the provider supports it

  // Usage data is always returned for non-streaming.
  // When streaming, you will get one usage object at
  // the end accompanied by an empty choices array.
  usage?: ResponseUsage;
};
```

```
// If the provider returns usage, we pass it down
// as-is. Otherwise, we count using the GPT-4 tokenizer.

type ResponseUsage = {
  /** Including images and tools if any */
  prompt_tokens: number;
  /** The tokens generated */
  completion_tokens: number;
  /** Sum of the above two fields */
  total_tokens: number;
};
```

```
// Subtypes:
type NonChatChoice = {
  finish_reason: string | null;
  text: string;
  error?: ErrorResponse;
};

type NonStreamingChoice = {
  finish_reason: string | null;
  native_finish_reason: string | null;
  message: {
    content: string | null;
    role: string;
    tool_calls?: ToolCall[];
  };
  error?: ErrorResponse;
};

type StreamingChoice = {
  finish_reason: string | null;
  native_finish_reason: string | null;
  delta: {
    content: string | null;
    role?: string;
    tool_calls?: ToolCall[];
  };
  error?: ErrorResponse;
};

type ErrorResponse = {
  code: number; // See "Error Handling" section
  message: string;
  metadata?: Record<string, unknown>; // Contains additional error information such as provider details, the raw error message, etc.
};

type ToolCall = {
  id: string;
  type: 'function';
  function: FunctionCall;
};
```

Here’s an example:

```
{
  "id": "gen-xxxxxxxxxxxxxx",
  "choices": [\
    {\
      "finish_reason": "stop", // Normalized finish_reason\
      "native_finish_reason": "stop", // The raw finish_reason from the provider\
      "message": {\
        // will be "delta" if streaming\
        "role": "assistant",\
        "content": "Hello there!"\
      }\
    }\
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 4,
    "total_tokens": 4
  },
  "model": "openai/gpt-3.5-turbo" // Could also be "anthropic/claude-2.1", etc, depending on the "model" that ends up being used
}
```

### Finish Reason

OpenRouter normalizes each model’s `finish_reason` to one of the following values: `tool_calls`, `stop`, `length`, `content_filter`, `error`.

Some models and providers may have additional finish reasons. The raw finish\_reason string returned by the model is available via the `native_finish_reason` property.

### Querying Cost and Stats

The token counts that are returned in the completions API response are **not** counted via the model’s native tokenizer. Instead it uses a normalized, model-agnostic count (accomplished via the GPT4o tokenizer). This is because some providers do not reliably return native token counts. This behavior is becoming more rare, however, and we may add native token counts to the response object in the future.

Credit usage and model pricing are based on the **native** token counts (not the ‘normalized’ token counts returned in the API response).

For precise token accounting using the model’s native tokenizer, you can retrieve the full generation information via the `/api/v1/generation` endpoint.

You can use the returned `id` to query for the generation stats (including token counts and cost) after the request is complete. This is how you can get the cost and tokens for _all models and requests_, streaming and non-streaming.

Query Generation Stats

```
const generation = await fetch(
  'https://openrouter.ai/api/v1/generation?id=$GENERATION_ID',
  { headers },
);

const stats = await generation.json();
```

Please see the [Generation](https://openrouter.ai/docs/api-reference/get-a-generation) API reference for the full response shape.

Note that token counts are also available in the `usage` field of the response body for non-streaming completions.

Was this page helpful?

YesNo

[**Streaming**\\
\\
Next](https://openrouter.ai/docs/api/reference/streaming) [Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=openrouter.ai)

Ask AI

Assistant

Hi, I'm an AI assistant with access to documentation and other content.

Tip: You can toggle this pane with

`⌘`

+

`/`

Suggestions

How do I integrate OpenRouter with LangChain in my Python or JavaScript application?

What are the different ways to enable real-time web search capabilities with OpenRouter models?

How can I use prompt caching with OpenRouter to reduce my AI model inference costs?

What file types and input methods does OpenRouter support for sending PDFs and videos to models?

How does OpenRouter's provider routing work and what parameters can I use to customize routing behavior?