"""
MCP Server for RackSum - Backward compatibility wrapper

This file maintains backward compatibility with existing imports.
The actual implementation has been modularized into the mcp package:
  - mcp/server.py: Main server entry point
  - mcp/tools.py: Tool definitions
  - mcp/handlers.py: Tool handler implementations
  - mcp/formatters.py: Output formatting helpers
"""

# Import main function for backward compatibility
from mcp.server import main

# Re-export for compatibility
__all__ = ['main']
