# release-note-helper

Helps craft release notes from Jira issues and GitHub PRs. Queries Jira for completed issues in a date range, lets the user accept/deny candidates, verifies linked PRs on GitHub, and drafts a formatted release note.

Uses Redis (Astro-provided) for per-user preferences and LibSQL for conversation memory.

## Manual env vars

Set these in `.env` (not auto-injected by Astro):

- `JIRA_BASE_URL` — e.g. `https://yourcompany.atlassian.net`
- `JIRA_EMAIL` — Atlassian account email
- `JIRA_API_TOKEN` — Atlassian API token
