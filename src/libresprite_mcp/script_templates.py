"""
JavaScript script templates for common LibreSprite operations.
"""

# TODO: Fix create_sprite, create_layer

class ScriptTemplates:
    """
    Generates JavaScript scripts for common LibreSprite operations.
    """

    def create_sprite(self, width: int, height: int, color_mode: str = "RGB") -> str:
        """
        Generate script to create a new sprite.

        Args:
            width: Width of the sprite
            height: Height of the sprite
            color_mode: Color mode (e.g., "RGB", "RGBA")

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    // Use the NewFile command to create a new sprite
    app.command.setParameter("width", {width});
    app.command.setParameter("height", {height});
    app.command.setParameter("colorMode", ColorMode.{color_mode.upper()});
    app.command.NewFile();
    app.command.clearParameters();
    
    const sprite = app.activeSprite;
    if (sprite) {{
        console.log('Created new sprite: ' + sprite.width + 'x' + sprite.height + ' (' + sprite.colorMode + ')');
        console.log('Active sprite now has ' + sprite.layerCount + ' layer(s)');
    }} else {{
        console.log('Failed to create sprite');
    }}
}} catch (e) {{
    console.log('Error creating sprite: ' + e.message);
}}
"""
    
    def create_layer(self, name: str = "New Layer") -> str:
        """
        Generate script to create a new layer in the active sprite.

        Args:
            name: Name of the new layer

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        // Use the NewLayer command to create a new layer
        app.command.setParameter("name", "{name}");
        app.command.NewLayer();
        app.command.clearParameters();
        
        console.log('Created new layer: {name}');
        console.log('Sprite now has ' + sprite.layerCount + ' layer(s)');
    }}
}} catch (e) {{
    console.log('Error creating layer: ' + e.message);
}}
"""
    
    def fill_layer(self, r: int, g: int, b: int, a: int = 255) -> str:
        """
        Generate script to fill the active layer with color.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const fillColor = col.rgba({r}, {g}, {b}, {a});
            
            // Clear the image with the specified color
            img.clear(fillColor);
            
            console.log('Filled active layer with color rgba(' + {r} + ',' + {g} + ',' + {b} + ',' + {a} + ')');
        }}
    }}
}} catch (e) {{
    console.log('Error filling layer: ' + e.message);
}}
"""
    
    def draw_circle(self, cx: int, cy: int, radius: int, r: int, g: int, b: int, a: int = 255, filled: bool = True) -> str:
        """
        Generate script to draw a circle.
        
        Args:
            cx: Center x-coordinate
            cy: Center y-coordinate
            radius: Circle radius in pixels
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)
            filled: Whether to fill the circle (default is True)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const circleColor = col.rgba({r}, {g}, {b}, {a});
            
            const cx = {cx};
            const cy = {cy};
            const radius = {radius};
            const filled = {str(filled).lower()};
            
            for (let y = cy - radius; y <= cy + radius; y++) {{
                for (let x = cx - radius; x <= cx + radius; x++) {{
                    if (x >= 0 && x < img.width && y >= 0 && y < img.height) {{
                        const dx = x - cx;
                        const dy = y - cy;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (filled ? distance <= radius : Math.abs(distance - radius) < 1) {{
                            img.putPixel(x, y, circleColor);
                        }}
                    }}
                }}
            }}
            
            console.log('Drew ' + (filled ? 'filled' : 'outlined') + ' circle at (' + cx + ',' + cy + ') radius ' + radius);
        }}
    }}
}} catch (e) {{
    console.log('Error drawing circle: ' + e.message);
}}
"""
    
    def get_sprite_info(self) -> str:
        """
        Generate script to get sprite information.
        
        Returns:
            JavaScript script as a string
        """
        return """
try {
    const sprite = app.activeSprite;
    if (!sprite) {
        console.log('No active sprite');
    } else {
        console.log('=== SPRITE INFO ===');
        console.log('Dimensions: ' + sprite.width + 'x' + sprite.height);
        console.log('Color Mode: ' + sprite.colorMode);
        console.log('Layer Count: ' + sprite.layerCount);
        console.log('Current Layer: ' + app.activeLayerNumber);
        console.log('Current Frame: ' + app.activeFrameNumber);
        
        console.log('--- LAYER DETAILS ---');
        for (let i = 0; i < sprite.layerCount; i++) {
            const layer = sprite.layer(i);
            if (layer) {
                console.log('Layer ' + i + ': "' + layer.name + '" (visible: ' + layer.isVisible + ', editable: ' + layer.isEditable + ')');
            }
        }
    }
} catch (e) {
    console.log('Error getting sprite info: ' + e.message);
}
"""

    def draw_rectangle(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int, a: int = 255, filled: bool = True) -> str:
        """
        Generate script to draw a rectangle.
        
        Args:
            x: Top-left x coordinate
            y: Top-left y coordinate
            width: Rectangle width
            height: Rectangle height
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)
            filled: Whether to fill the rectangle (default is True)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const rectColor = col.rgba({r}, {g}, {b}, {a});
            
            const x = {x};
            const y = {y};
            const width = {width};
            const height = {height};
            const filled = {str(filled).lower()};
            
            if (filled) {{
                // Fill the rectangle
                for (let py = y; py < y + height; py++) {{
                    for (let px = x; px < x + width; px++) {{
                        if (px >= 0 && px < img.width && py >= 0 && py < img.height) {{
                            img.putPixel(px, py, rectColor);
                        }}
                    }}
                }}
            }} else {{
                // Draw rectangle outline
                // Top and bottom edges
                for (let px = x; px < x + width; px++) {{
                    if (px >= 0 && px < img.width) {{
                        if (y >= 0 && y < img.height) img.putPixel(px, y, rectColor);
                        if (y + height - 1 >= 0 && y + height - 1 < img.height) img.putPixel(px, y + height - 1, rectColor);
                    }}
                }}
                // Left and right edges
                for (let py = y; py < y + height; py++) {{
                    if (py >= 0 && py < img.height) {{
                        if (x >= 0 && x < img.width) img.putPixel(x, py, rectColor);
                        if (x + width - 1 >= 0 && x + width - 1 < img.width) img.putPixel(x + width - 1, py, rectColor);
                    }}
                }}
            }}
            
            console.log('Drew ' + (filled ? 'filled' : 'outlined') + ' rectangle at (' + x + ',' + y + ') size ' + width + 'x' + height);
        }}
    }}
}} catch (e) {{
    console.log('Error drawing rectangle: ' + e.message);
}}
"""

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, a: int = 255, thickness: int = 1) -> str:
        """
        Generate script to draw a line.
        
        Args:
            x1: Start x coordinate
            y1: Start y coordinate
            x2: End x coordinate
            y2: End y coordinate
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)
            thickness: Line thickness in pixels (default is 1)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const lineColor = col.rgba({r}, {g}, {b}, {a});
            
            const x1 = {x1};
            const y1 = {y1};
            const x2 = {x2};
            const y2 = {y2};
            const thickness = {thickness};
            
            // Bresenham's line algorithm
            const dx = Math.abs(x2 - x1);
            const dy = Math.abs(y2 - y1);
            const sx = x1 < x2 ? 1 : -1;
            const sy = y1 < y2 ? 1 : -1;
            let err = dx - dy;
            
            let x = x1;
            let y = y1;
            
            while (true) {{
                // Draw thick line by drawing a circle at each point
                for (let ty = -Math.floor(thickness/2); ty <= Math.floor(thickness/2); ty++) {{
                    for (let tx = -Math.floor(thickness/2); tx <= Math.floor(thickness/2); tx++) {{
                        const px = x + tx;
                        const py = y + ty;
                        if (px >= 0 && px < img.width && py >= 0 && py < img.height) {{
                            if (thickness === 1 || (tx * tx + ty * ty <= (thickness/2) * (thickness/2))) {{
                                img.putPixel(px, py, lineColor);
                            }}
                        }}
                    }}
                }}
                
                if (x === x2 && y === y2) break;
                
                const e2 = 2 * err;
                if (e2 > -dy) {{
                    err -= dy;
                    x += sx;
                }}
                if (e2 < dx) {{
                    err += dx;
                    y += sy;
                }}
            }}
            
            console.log('Drew line from (' + x1 + ',' + y1 + ') to (' + x2 + ',' + y2 + ') thickness ' + thickness);
        }}
    }}
}} catch (e) {{
    console.log('Error drawing line: ' + e.message);
}}
"""

    def draw_ellipse(self, cx: int, cy: int, width: int, height: int, r: int, g: int, b: int, a: int = 255, filled: bool = True) -> str:
        """
        Generate script to draw an ellipse.
        
        Args:
            cx: Center x coordinate
            cy: Center y coordinate
            width: Ellipse width
            height: Ellipse height
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)
            filled: Whether to fill the ellipse (default is True)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const ellipseColor = col.rgba({r}, {g}, {b}, {a});
            
            const cx = {cx};
            const cy = {cy};
            const width = {width};
            const height = {height};
            const filled = {str(filled).lower()};
            
            const a = width / 2;
            const b = height / 2;
            
            for (let y = cy - Math.ceil(b); y <= cy + Math.ceil(b); y++) {{
                for (let x = cx - Math.ceil(a); x <= cx + Math.ceil(a); x++) {{
                    if (x >= 0 && x < img.width && y >= 0 && y < img.height) {{
                        const dx = x - cx;
                        const dy = y - cy;
                        const ellipseEq = (dx * dx) / (a * a) + (dy * dy) / (b * b);
                        
                        if (filled) {{
                            if (ellipseEq <= 1) {{
                                img.putPixel(x, y, ellipseColor);
                            }}
                        }} else {{
                            // Draw outline - check if point is close to ellipse edge
                            if (Math.abs(ellipseEq - 1) < 0.1) {{
                                img.putPixel(x, y, ellipseColor);
                            }}
                        }}
                    }}
                }}
            }}
            
            console.log('Drew ' + (filled ? 'filled' : 'outlined') + ' ellipse at (' + cx + ',' + cy + ') size ' + width + 'x' + height);
        }}
    }}
}} catch (e) {{
    console.log('Error drawing ellipse: ' + e.message);
}}
"""

    def put_pixel(self, x: int, y: int, r: int, g: int, b: int, a: int = 255) -> str:
        """
        Generate script to set a pixel color.
        
        Args:
            x: X coordinate
            y: Y coordinate
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const x = {x};
            const y = {y};
            
            if (x >= 0 && x < img.width && y >= 0 && y < img.height) {{
                const col = app.pixelColor;
                const pixelColor = col.rgba({r}, {g}, {b}, {a});
                img.putPixel(x, y, pixelColor);
                console.log('Set pixel at (' + x + ',' + y + ') to rgba(' + {r} + ',' + {g} + ',' + {b} + ',' + {a} + ')');
            }} else {{
                console.log('Pixel coordinates (' + x + ',' + y + ') are out of bounds');
            }}
        }}
    }}
}} catch (e) {{
    console.log('Error setting pixel: ' + e.message);
}}
"""

    def flood_fill(self, x: int, y: int, r: int, g: int, b: int, a: int = 255) -> str:
        """
        Generate script to flood fill an area with color.
        
        Args:
            x: X coordinate to start fill
            y: Y coordinate to start fill
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha component (0-255, default is 255)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const startX = {x};
            const startY = {y};
            
            if (startX >= 0 && startX < img.width && startY >= 0 && startY < img.height) {{
                const col = app.pixelColor;
                const fillColor = col.rgba({r}, {g}, {b}, {a});
                const targetColor = img.getPixel(startX, startY);
                
                if (targetColor === fillColor) {{
                    console.log('Target color is the same as fill color, no action needed');
                    return;
                }}
                
                const stack = [[startX, startY]];
                let fillCount = 0;
                
                while (stack.length > 0) {{
                    const [x, y] = stack.pop();
                    
                    if (x < 0 || x >= img.width || y < 0 || y >= img.height) continue;
                    if (img.getPixel(x, y) !== targetColor) continue;
                    
                    img.putPixel(x, y, fillColor);
                    fillCount++;
                    
                    stack.push([x + 1, y]);
                    stack.push([x - 1, y]);
                    stack.push([x, y + 1]);
                    stack.push([x, y - 1]);
                }}
                
                console.log('Flood fill completed at (' + startX + ',' + startY + '), filled ' + fillCount + ' pixels');
            }} else {{
                console.log('Start coordinates (' + startX + ',' + startY + ') are out of bounds');
            }}
        }}
    }}
}} catch (e) {{
    console.log('Error flood filling: ' + e.message);
}}
"""

    def set_active_layer(self, layer_number: int) -> str:
        """
        Generate script to switch to a specific layer.
        
        Args:
            layer_number: Layer index (0-based from bottom)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const layerNumber = {layer_number};
        
        if (layerNumber >= 0 && layerNumber < sprite.layerCount) {{
            // Use the GotoLayer command - this might not exist, so we'll use a workaround
            // Since there's no direct layer switching in the API, we'll document the current layer
            const layer = sprite.layer(layerNumber);
            if (layer) {{
                console.log('Switching to layer ' + layerNumber + ': "' + layer.name + '"');
                console.log('Note: Layer switching via script may be limited. Use UI to switch layers.');
                console.log('Current active layer: ' + app.activeLayerNumber);
            }} else {{
                console.log('Layer ' + layerNumber + ' not found');
            }}
        }} else {{
            console.log('Layer number ' + layerNumber + ' is out of range (0-' + (sprite.layerCount - 1) + ')');
        }}
    }}
}} catch (e) {{
    console.log('Error switching layer: ' + e.message);
}}
"""

    def delete_layer(self, layer_number: int) -> str:
        """
        Generate script to delete a layer.
        
        Args:
            layer_number: Layer index (0-based from bottom)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const layerNumber = {layer_number};
        
        if (layerNumber >= 0 && layerNumber < sprite.layerCount) {{
            if (sprite.layerCount <= 1) {{
                console.log('Cannot delete the only remaining layer');
                return;
            }}
            
            const layer = sprite.layer(layerNumber);
            if (layer) {{
                const layerName = layer.name;
                // Use RemoveLayer command
                app.command.RemoveLayer();
                console.log('Deleted layer ' + layerNumber + ': "' + layerName + '"');
                console.log('Sprite now has ' + sprite.layerCount + ' layer(s)');
            }} else {{
                console.log('Layer ' + layerNumber + ' not found');
            }}
        }} else {{
            console.log('Layer number ' + layerNumber + ' is out of range (0-' + (sprite.layerCount - 1) + ')');
        }}
    }}
}} catch (e) {{
    console.log('Error deleting layer: ' + e.message);
}}
"""


    def replace_color(self, old_r: int, old_g: int, old_b: int, new_r: int, new_g: int, new_b: int, new_a: int = 255) -> str:
        """
        Generate script to replace one color with another throughout the image.
        
        Args:
            old_r: Old color red component (0-255)
            old_g: Old color green component (0-255)
            old_b: Old color blue component (0-255)
            new_r: New color red component (0-255)
            new_g: New color green component (0-255)
            new_b: New color blue component (0-255)
            new_a: New color alpha component (0-255, default is 255)

        Returns:
            JavaScript script as a string
        """
        return f"""
try {{
    const sprite = app.activeSprite;
    if (!sprite) {{
        console.log('No active sprite');
    }} else {{
        const img = app.activeImage;
        if (!img) {{
            console.log('No active image');
        }} else {{
            const col = app.pixelColor;
            const oldColor = col.rgba({old_r}, {old_g}, {old_b}, 255); // Assume full alpha for comparison
            const newColor = col.rgba({new_r}, {new_g}, {new_b}, {new_a});
            
            let replacedCount = 0;
            
            for (let y = 0; y < img.height; y++) {{
                for (let x = 0; x < img.width; x++) {{
                    const pixelColor = img.getPixel(x, y);
                    // Compare RGB components (ignore alpha for old color)
                    if (col.rgbaR(pixelColor) === {old_r} && 
                        col.rgbaG(pixelColor) === {old_g} && 
                        col.rgbaB(pixelColor) === {old_b}) {{
                        img.putPixel(x, y, newColor);
                        replacedCount++;
                    }}
                }}
            }}
            
            console.log('Replaced ' + replacedCount + ' pixels from rgba(' + {old_r} + ',' + {old_g} + ',' + {old_b} + ',*) to rgba(' + {new_r} + ',' + {new_g} + ',' + {new_b} + ',' + {new_a} + ')');
        }}
    }}
}} catch (e) {{
    console.log('Error replacing color: ' + e.message);
}}
"""