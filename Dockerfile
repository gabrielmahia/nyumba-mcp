# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for nyumba-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/nyumba-mcp"
LABEL org.opencontainers.image.description="nyumba-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir nyumba-mcp

CMD ["nyumba-mcp"]
