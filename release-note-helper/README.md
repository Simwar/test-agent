# release-note-helper

An agent that helps you craft your release notes

## Quick start

```bash
# Install dependencies
bun install

# Start the agent locally
ast dev
```

## Project structure

```
release-note-helper/
├── agent/
│   └── index.ts          # Agent entry point
├── ingestion/
│   ├── startup/
│   │   ├── index.ts      # startup ingestion pipeline
│   │   └── Dockerfile
├── astropods.yml             # Agent specification
├── Dockerfile            # Agent container
├── .env                  # Environment variables (set via ast configure; not committed)
└── package.json
```

## Configuration

The agent is configured in `astropods.yml`. Key sections:

### Integrations

| Integration | Type | Environment variable |
|------------|------|---------------------|
| Anthropic | Model API | `ANTHROPIC_API_KEY` |
| GitHub | Tool | `GITHUB_TOKEN` |

### Interfaces
- **Web** — HTTP/SSE endpoint (playground available at `localhost:3000` during dev)
- **Slack** — bot integration via Socket Mode

### Ingestion

Data pipeline triggered via **startup**. Edit `ingestion/index.ts` to define how data flows into your knowledge stores.

