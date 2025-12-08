[![Logo](https://files.buildwithfern.com/openrouter.docs.buildwithfern.com/docs/5a7e2b0bd58241d151e9e352d7a4f898df12c062576c0ce0184da76c3635c5d3/content/assets/logo.svg)![Logo](https://files.buildwithfern.com/openrouter.docs.buildwithfern.com/docs/6f95fbca823560084c5593ea2aa4073f00710020e6a78f8a3f54e835d97a8a0b/content/assets/logo-white.svg)](https://openrouter.ai/)

Search
`/`
Ask AI

[Models](https://openrouter.ai/models) [Chat](https://openrouter.ai/chat) [Ranking](https://openrouter.ai/rankings) [Docs](https://openrouter.ai/docs/api-reference/overview)

[Docs](https://openrouter.ai/docs/quickstart) [API Reference](https://openrouter.ai/docs/api/reference/overview) [SDK Reference](https://openrouter.ai/docs/sdks/typescript/overview)

[Docs](https://openrouter.ai/docs/quickstart) [API Reference](https://openrouter.ai/docs/api/reference/overview) [SDK Reference](https://openrouter.ai/docs/sdks/typescript/overview)

- Overview

  - [Quickstart](https://openrouter.ai/docs/quickstart)
  - [Principles](https://openrouter.ai/docs/guides/overview/principles)
  - [Models](https://openrouter.ai/docs/guides/overview/models)
  - Multimodal

  - Authentication

  - [FAQ](https://openrouter.ai/docs/faq)
  - [Enterprise](https://openrouter.ai/enterprise)
- Models & Routing

  - [Auto Model Selection](https://openrouter.ai/docs/guides/routing/auto-model-selection)
  - [Model Fallbacks](https://openrouter.ai/docs/guides/routing/model-fallbacks)
  - [Provider Selection](https://openrouter.ai/docs/guides/routing/provider-selection)
  - Model Variants
- Features

  - [Presets](https://openrouter.ai/docs/guides/features/presets)
  - [Tool Calling](https://openrouter.ai/docs/guides/features/tool-calling)
  - [Web Search](https://openrouter.ai/docs/guides/features/web-search)
  - [Structured Outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
  - [Message Transforms](https://openrouter.ai/docs/guides/features/message-transforms)
  - [Model Routing](https://openrouter.ai/docs/guides/features/model-routing)
  - [Zero Completion Insurance](https://openrouter.ai/docs/guides/features/zero-completion-insurance)
  - [ZDR](https://openrouter.ai/docs/guides/features/zdr)
  - [App Attribution](https://openrouter.ai/docs/app-attribution)
  - [Broadcast](https://openrouter.ai/docs/guides/features/broadcast)
  - [Provisioning API Keys](https://openrouter.ai/docs/guides/features/provisioning-api-keys)
  - Privacy

  - Best Practices

  - Guides

  - Community

[Models](https://openrouter.ai/models) [Chat](https://openrouter.ai/chat) [Ranking](https://openrouter.ai/rankings) [Docs](https://openrouter.ai/docs/api-reference/overview)

System

On this page

- [Using the OpenRouter SDK (Beta)](https://openrouter.ai/docs/quickstart#using-the-openrouter-sdk-beta)
- [Using the OpenRouter API directly](https://openrouter.ai/docs/quickstart#using-the-openrouter-api-directly)
- [Using the OpenAI SDK](https://openrouter.ai/docs/quickstart#using-the-openai-sdk)
- [Using third-party SDKs](https://openrouter.ai/docs/quickstart#using-third-party-sdks)

[Overview](https://openrouter.ai/docs/quickstart)

# Quickstart

Copy page

Get started with OpenRouter

OpenRouter provides a unified API that gives you access to hundreds of AI models through a single endpoint, while automatically handling fallbacks and selecting the most cost-effective options. Get started with just a few lines of code using your preferred SDK or framework.

Looking for information about free models and rate limits? Please see the [FAQ](https://openrouter.ai/docs/faq#how-are-rate-limits-calculated)

In the examples below, the OpenRouter-specific headers are optional. Setting them allows your app to appear on the OpenRouter leaderboards. For detailed information about app attribution, see our [App Attribution guide](https://openrouter.ai/docs/app-attribution).

## Using the OpenRouter SDK (Beta)

First, install the SDK:

npmyarnpnpm

```
npm install @openrouter/sdk
```

Then use it in your code:

TypeScript SDK

```
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  defaultHeaders: {
    'HTTP-Referer': '<YOUR_SITE_URL>', // Optional. Site URL for rankings on openrouter.ai.
    'X-Title': '<YOUR_SITE_NAME>', // Optional. Site title for rankings on openrouter.ai.
  },
});

const completion = await openRouter.chat.send({
  model: 'openai/gpt-4o',
  messages: [\
    {\
      role: 'user',\
      content: 'What is the meaning of life?',\
    },\
  ],
  stream: false,
});

console.log(completion.choices[0].message.content);
```

## Using the OpenRouter API directly

You can use the interactive [Request Builder](https://openrouter.ai/request-builder) to generate OpenRouter API requests in the language of your choice.

PythonTypeScript (fetch)Shell

```
import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer <OPENROUTER_API_KEY>",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openai/gpt-4o", # Optional
    "messages": [\
      {\
        "role": "user",\
        "content": "What is the meaning of life?"\
      }\
    ]
  })
)
```

## Using the OpenAI SDK

TypescriptPython

```
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: '<OPENROUTER_API_KEY>',
  defaultHeaders: {
    'HTTP-Referer': '<YOUR_SITE_URL>', // Optional. Site URL for rankings on openrouter.ai.
    'X-Title': '<YOUR_SITE_NAME>', // Optional. Site title for rankings on openrouter.ai.
  },
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: 'openai/gpt-4o',
    messages: [\
      {\
        role: 'user',\
        content: 'What is the meaning of life?',\
      },\
    ],
  });

  console.log(completion.choices[0].message);
}

main();
```

The API also supports [streaming](https://openrouter.ai/docs/api/reference/streaming).

## Using third-party SDKs

For information about using third-party SDKs and frameworks with OpenRouter, please [see our frameworks documentation.](https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview)

Was this page helpful?

YesNo

[**Principles** \\
\\
Core principles and values of OpenRouter\\
\\
Next](https://openrouter.ai/docs/guides/overview/principles) [Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=openrouter.ai)

Ask AI

Assistant

Hi, I'm an AI assistant with access to documentation and other content.

Tip: You can toggle this pane with

`⌘`

+

`/`

Suggestions

How do I integrate OpenRouter with LangChain in Python or JavaScript applications?

What is the difference between using the :online variant and the web plugin for real-time web search capabilities?

How can I send PDF documents to OpenRouter models and what formats are supported?

Which models on OpenRouter support reasoning tokens and how are they charged in the API response?

How does OpenRouter's provider routing work and what options are available to customize request routing across providers?