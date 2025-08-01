"""
Proxy server for Libresprite.
"""

import threading
from typing import Optional
from mcp.server.fastmcp import Context
from flask import Flask, jsonify, request

class LibrespriteProxy:
    """
    Proxy server for Libresprite.

    This is a relay server that acts as a bridge between the MCP server and the remote libresprite script.
    From the POV of the MCP server, this fully abstracts libresprite into a convenient IO interface to execute remote scripts.
    """

    def __init__(self, port: int):
        # Stores current script
        self._script: str | None = None

        # Stores output of the script execution
        self._output: str | None = None

        # Stores flag indicating if execution is in progress
        self._lock: bool = False

        # Initialize event handlers
        self._script_event = threading.Event()
        self._output_event = threading.Event()

        # Relay server configuration
        self.port = port
        self.app = Flask(__name__)

        # Initialize server routes
        self._setup_routes()
        self._server_thread: Optional[threading.Thread] = None

    def _setup_routes(self):
        """Setup Flask routes."""

        @self.app.get('/')
        def get_script():
            """Get the current script."""
            if self._script is None:
                self._script_event.wait()
                self._script_event.clear()
            script = self._script
            self._script = None
            return jsonify({"script": script})

        @self.app.post('/')
        def post_output():
            """Post execution output."""
            if not self._lock:
                # ignore random requests
                return jsonify({"status": "ignored"})
            req = request.get_json(force=True, silent=True)
            if req:
                output = req.get('output')
            else:
                return jsonify({"status": "invalid"})
            self._output = output
            self._output_event.set()
            return jsonify({"status": "success"})

        @self.app.get('/ping')
        def ping():
            """Ping endpoint for health checks."""
            return jsonify({"status": "pong"})

    def _run_server(self):
        """Run the Flask server."""
        self.app.run(
            host='localhost',
            port=self.port,
            debug=False,
            use_reloader=False
        )

    def start(self):
        """Start the HTTP server in a background thread."""
        if self._server_thread and self._server_thread.is_alive():
            return

        self._server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self._server_thread.start()

    def run_script(self, script: str, ctx: Context) -> str:
        """
        Run a script in the execution context.

        WARNING: This method is synchronous and blocking.

        Args:
            script: The script to execute
        """
        # This proxy only allows one script to be executed at a time
        if self._lock:
            ctx.error("Script execution is already in progress...")
            raise RuntimeError("Script execution is already in progress.")

        # Sending the script
        ctx.info("Sending script to libresprite...")
        self._lock = True
        self._script = script
        self._script_event.set()

        # Waiting for execution
        if not self._output_event.wait(timeout=15):
            ctx.warning("This is taking longer than usual, make sure the user has the Libresprite application with the remote script running?")
        self._output_event.wait()
        self._output_event.clear()

        # Return the output
        ctx.info("Script execution completed, checking the logs...")
        output = self._output
        self._output = None
        self._lock = False
        return output