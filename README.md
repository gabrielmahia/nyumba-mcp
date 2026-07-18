# nyumba-mcp
<!-- mcp-name: io.github.gabrielmahia/nyumba-mcp -->

[![nyumba-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/nyumba-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/nyumba-mcp)
[![smithery badge](https://smithery.ai/badge/@gabrielmahia/nyumba-mcp)](https://smithery.ai/server/@gabrielmahia/nyumba-mcp)


---
**Compatible with `claude-sonnet-5`** (released 2026-06-30) — Anthropic's most agentic
Sonnet yet. Runs multi-step tool chains end-to-end without stopping short.
Install: `pip install nyumba-mcp` · Use with any MCP client.

---

MCP server for Kenya housing — rental market, tenant rights, building permits, affordable housing programs, and housing finance. 5 tools.

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
Connect it to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) —
the coordination event bus that routes signals between domains automatically.

```bash
pip install africa-coord-bus
```

All 32 servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)
Live demo: [coord-cascade-demo](https://github.com/gabrielmahia/coord-cascade-demo)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — 33 MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
