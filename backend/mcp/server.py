"""
MCP Server for RackSum - Main entry point

Provides site stats and resource information through the Model Context Protocol.
This server exposes datacenter infrastructure data to AI assistants like Claude.
"""
import os
import sys
import django
import asyncio
import logging
from mcp.server import Server
from mcp.types import TextContent
from mcp.server.stdio import stdio_server

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .tools import get_tool_definitions
from . import handlers

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[MCP] %(asctime)s - %(levelname)s - %(message)s'
)

# Create MCP server instance
app = Server("racksum-stats")


@app.list_tools()
async def list_tools():
    """List available MCP tools"""
    return get_tool_definitions()


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to appropriate handlers"""

    if name == "get_site_stats":
        return await handlers.get_site_stats()

    elif name == "get_site_details":
        site_name = arguments.get("site_name")
        if not site_name:
            return [TextContent(type="text", text="Error: site_name is required")]
        return await handlers.get_site_details(site_name)

    elif name == "get_rack_details":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await handlers.get_rack_details(site_name, rack_name)

    elif name == "get_available_resources":
        category = arguments.get("category")
        limit = arguments.get("limit")
        return await handlers.get_available_resources(category, limit)

    elif name == "get_resource_summary":
        return await handlers.get_resource_summary()

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting RackSum MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
