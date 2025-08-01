"""
Main entry point for the Libresprite MCP server application.
"""

import click
import logging
from .libresprite_proxy import LibrespriteProxy
from .mcp_server import MCPServer

def main() -> None:
    """Main entry point for the application."""
    # Disable unwanted logging to avoid messing with stdio
    logging.disable(logging.WARN)
    # HACK: https://stackoverflow.com/a/57086684
    def secho(text, file=None, nl=None, err=None, color=None, **styles):
        pass
    def echo(text, file=None, nl=None, err=None, color=None, **styles):
        pass
    click.echo = echo
    click.secho = secho

    # Initialize and start HTTP relay server
    libresprite_proxy = LibrespriteProxy(port=64823)
    libresprite_proxy.start()

    # Initialize and run MCP server (this blocks)
    mcp_server = MCPServer(libresprite_proxy)
    mcp_server.run(transport='stdio')

if __name__ == '__main__':
    main()