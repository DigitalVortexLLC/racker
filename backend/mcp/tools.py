"""
MCP tool definitions for RackSum datacenter management
"""
from mcp.types import Tool


def get_tool_definitions() -> list[Tool]:
    """Return list of available MCP tools"""
    return [
        Tool(
            name="get_site_stats",
            description="Get statistics for all sites including rack count, device count, and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_site_details",
            description="Get detailed information about a specific site including all racks and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {
                        "type": "string",
                        "description": "Name of the site to get details for"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": ["site_name"]
            }
        ),
        Tool(
            name="get_rack_details",
            description="Get detailed information about a specific rack including devices and resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_name": {
                        "type": "string",
                        "description": "Name of the site containing the rack"
                    },
                    "rack_name": {
                        "type": "string",
                        "description": "Name of the rack to get details for"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": ["site_name", "rack_name"]
            }
        ),
        Tool(
            name="get_available_resources",
            description="Get information about available device types and their specifications",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter devices by category (optional)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of devices to return (optional, default: no limit)"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                }
            }
        ),
        Tool(
            name="get_resource_summary",
            description="Get overall resource utilization summary across all sites",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format: 'text' (default, human-readable) or 'json' (structured data)",
                        "default": "text"
                    }
                },
                "required": []
            }
        )
    ]
