# Architecture

Unlike Aseprite, LibreSprite lacks a command-line interface for doing things. The only thing it provides to programmatically control its interface is a JavaScript scripting interface. These scripts run in a very limited context and the closest thing I could find around networking was the `storage.fetch` method which can make a network request.

To make it work, I wrote a relay server that acts as a convenient proxy for the MCP server to interact with LibreSprite, while a remote script running inside LibreSprite polls the endpoints for scripts to execute.

![architecture](https://raw.githubusercontent.com/Snehil-Shah/libresprite-mcp/main/assets/architecture.svg)