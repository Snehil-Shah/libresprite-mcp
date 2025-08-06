"""
MCP server implementation that exposes tools for interacting with the libresprite-proxy server.
"""

import os
from mcp.server.fastmcp import FastMCP, Context
from .libresprite_proxy import LibrespriteProxy
from .script_templates import ScriptTemplates


class MCPServer:
    """The LibreSprite MCP Server."""

    def __init__(self, libresprite_proxy: LibrespriteProxy, server_name: str = "libresprite"):
        self._libresprite_proxy = libresprite_proxy

        # Initialize FastMCP
        self.mcp = FastMCP(server_name)

        # Initialize script templates
        self.script_templates = ScriptTemplates()

        # Setup MCP tools, prompts, and resources
        self._setup_tools()
        self._setup_resources()
        self._setup_prompts()

    def _setup_tools(self):
        """Setup MCP tools."""

        @self.mcp.tool()
        def run_script(script: str, ctx: Context) -> str:
            """
            Run a JavaScript script inside Libresprite.

            IMPORTANT: Make sure you are well versed with the
            documentation and examples provided in the resources
            `docs:reference` and `docs:examples`.

            Args:
                script: The script to execute

            Returns:
                Console output
            """
            return self._libresprite_proxy.run_script(script, ctx)
        
        @self.mcp.tool()
        def create_sprite(width: int, height: int, color_mode: str, ctx: Context) -> str:
            """
            Creates a new sprite with specified dimensions and color mode.

            Args:
                width: Width of the sprite
                height: Height of the sprite
                color_mode: Color mode (default is "RGB")
            
            Returns:
                Confirmation message
            """
            script = self.script_templates.create_sprite(width, height, color_mode)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def create_layer(name: str, ctx: Context) -> str:
            """
            Adds a new layer to the active sprite.

            Args:
            name: Name for the new layer (default is "New Layer")

            Returns:
                Confirmation message
            """
            script = self.script_templates.create_layer(name)
            return self._libresprite_proxy.run_script(script, ctx)
        
        @self.mcp.tool()
        def fill_layer(color_r: int, color_g: int, color_b: int, color_a: int, ctx: Context) -> str:
            """
            Fill the active layer with a solid color.

            Args:
                color_r: Red component (0-255)
                color_g: Green component (0-255)  
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255, default is 255)

            Returns:
                Confirmation message
            """
            script = self.script_templates.fill_layer(color_r, color_g, color_b, color_a)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def draw_circle(center_x: int, center_y: int, radius: int,
                        color_r: int, color_g: int, color_b: int,
                        color_a: int, filled: bool,
                        ctx: Context) -> str:
            """
            Draw a circle on the active layer.

            Args:
                center_x: X coordinate of circle center
                center_y: Y coordinate of circle center
                radius: Circle radius in pixels
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255, default is 255)
                filled: Whether to fill the circle (default is True)

            Returns:
                Confirmation message
            """
            script = self.script_templates.draw_circle(center_x,
                                                    center_y, radius,
                                                    color_r, color_g,
                                                    color_b, color_a, 
                                                    filled)
            return self._libresprite_proxy.run_script(script, ctx)
        
        @self.mcp.tool()
        def get_sprite_info(ctx: Context) -> str:
            """
            Get information about the active sprite including 
            dimensions, layers, and frames.

            Returns:
                Sprite information and layer details
            """
            script = self.script_templates.get_sprite_info()
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def draw_rectangle(x: int, y: int, width: int, height: int,
                            color_r: int, color_g: int, color_b: int,
                            color_a: int, filled: bool,
                            ctx: Context) -> str:
            """
            Draw a rectangle on the active layer.

            Args:
                x: Top-left x coordinate
                y: Top-left y coordinate
                width: Rectangle width
                height: Rectangle height
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255)
                filled: Whether to fill the rectangle

            Returns:
                Confirmation message
            """
            script = self.script_templates.draw_rectangle(x, y, width, height,
                                                        color_r, color_g, color_b, color_a, filled)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def draw_line(x1: int, y1: int, x2: int, y2: int,
                        color_r: int, color_g: int, color_b: int,
                        color_a: int, thickness: int,
                        ctx: Context) -> str:
            """
            Draw a line on the active layer.

            Args:
                x1: Start x coordinate
                y1: Start y coordinate
                x2: End x coordinate
                y2: End y coordinate
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255)
                thickness: Line thickness in pixels

            Returns:
                Confirmation message
            """
            script = self.script_templates.draw_line(x1, y1, x2, y2,
                                                    color_r, color_g, color_b, color_a, thickness)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def draw_ellipse(center_x: int, center_y: int, width: int, height: int,
                        color_r: int, color_g: int, color_b: int,
                        color_a: int, filled: bool,
                        ctx: Context) -> str:
            """
            Draw an ellipse on the active layer.

            Args:
                center_x: Center x coordinate
                center_y: Center y coordinate
                width: Ellipse width
                height: Ellipse height
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255)
                filled: Whether to fill the ellipse

            Returns:
                Confirmation message
            """
            script = self.script_templates.draw_ellipse(center_x, center_y, width, height,
                                                        color_r, color_g, color_b, color_a, filled)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def put_pixel(x: int, y: int, color_r: int, color_g: int, color_b: int, color_a: int, ctx: Context) -> str:
            """
            Set a single pixel color.

            Args:
                x: X coordinate
                y: Y coordinate
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255)

            Returns:
                Confirmation message
            """
            script = self.script_templates.put_pixel(x, y, color_r, color_g, color_b, color_a)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def flood_fill(x: int, y: int, color_r: int, color_g: int, color_b: int, color_a: int, ctx: Context) -> str:
            """
            Flood fill an area with color.

            Args:
                x: X coordinate to start fill
                y: Y coordinate to start fill
                color_r: Red component (0-255)
                color_g: Green component (0-255)
                color_b: Blue component (0-255)
                color_a: Alpha component (0-255)

            Returns:
                Confirmation message with fill count
            """
            script = self.script_templates.flood_fill(x, y, color_r, color_g, color_b, color_a)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def delete_layer(layer_number: int, ctx: Context) -> str:
            """
            Delete a layer.

            Args:
                layer_number: Layer index to delete (0-based from bottom)

            Returns:
                Confirmation message
            """
            script = self.script_templates.delete_layer(layer_number)
            return self._libresprite_proxy.run_script(script, ctx)

        @self.mcp.tool()
        def replace_color(old_color_r: int, old_color_g: int, old_color_b: int,
                            new_color_r: int, new_color_g: int, new_color_b: int,
                            new_color_a: int, ctx: Context) -> str:
            """
            Replace one color with another throughout the image.

            Args:
                old_color_r: Old color red component (0-255)
                old_color_g: Old color green component (0-255)
                old_color_b: Old color blue component (0-255)
                new_color_r: New color red component (0-255)
                new_color_g: New color green component (0-255)
                new_color_b: New color blue component (0-255)
                new_color_a: New color alpha component (0-255)

            Returns:
                Confirmation message with replacement count
            """
            script = self.script_templates.replace_color(old_color_r, old_color_g, old_color_b,
                                                        new_color_r, new_color_g, new_color_b, new_color_a)
            return self._libresprite_proxy.run_script(script, ctx)

    def _setup_resources(self):
        """Setup MCP resources."""

        base_dir = os.path.dirname(os.path.abspath(__file__))

        @self.mcp.resource("docs://reference")
        def read_reference() -> str:
            """Read the libresprite command reference documentation."""
            doc_path = os.path.join(base_dir, "resources", "reference.txt")
            try:
                with open(doc_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading reference.txt: {e}"

        @self.mcp.resource("docs://examples")
        def read_examples() -> str:
            """Read example scripts using libresprite commands."""
            example_path = os.path.join(base_dir, "resources", "examples.txt")
            try:
                with open(example_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading examples.txt: {e}"

    def _setup_prompts(self):
        """Setup MCP prompts."""

        @self.mcp.prompt(title="libresprite")
        def libresprite(prompt: str) -> str:
            """
            Prompt template to use the libresprite tool with proper context conditioning.

            Args:
                prompt: User prompt

            Returns:
                Prompt to process
            """
            return f"""
            Libresprite is a program for creating and editing pixel art and animations using JavaScript.

            IMPORTANT: You have dedicated MCP tools available. ALWAYS use these tools instead of run_script():

            SPRITE & LAYER MANAGEMENT:
            - create_sprite(width, height, color_mode) - CREATE NEW SPRITES  
            - create_layer(name) - ADD LAYERS
            - delete_layer(layer_number) - DELETE LAYERS
            - get_sprite_info() - GET SPRITE DETAILS

            DRAWING TOOLS:
            - fill_layer(r, g, b, a) - SOLID COLOR FILLS
            - draw_circle(cx, cy, radius, r, g, b, a, filled) - DRAW CIRCLES
            - draw_rectangle(x, y, width, height, r, g, b, a, filled) - DRAW RECTANGLES
            - draw_line(x1, y1, x2, y2, r, g, b, a, thickness) - DRAW LINES
            - draw_ellipse(cx, cy, width, height, r, g, b, a, filled) - DRAW ELLIPSES

            PIXEL OPERATIONS:
            - put_pixel(x, y, r, g, b, a) - SET SINGLE PIXEL
            - flood_fill(x, y, r, g, b, a) - FLOOD FILL AREAS
            - replace_color(old_r, old_g, old_b, new_r, new_g, new_b, new_a) - REPLACE COLORS

            You can use the `run_script` tool to execute JavaScript scripts in the context of libresprite.
            ONLY use `run_script` for complex custom operations not covered by the above tools.

            Before proceeding, please ensure you are well versed with the documentation and examples provided in the resources `docs:reference` and `docs:examples`.
            
            Here's what you need to do using the above tools and resources:

            {prompt}
            """

    def run(self, transport: str = 'stdio'):
        """Run the MCP server."""
        self.mcp.run(transport=transport)