"""
MCP Server for RackSum - Provides site stats and resource information
"""
import os
import sys
import django
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from asgiref.sync import sync_to_async

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Site, Rack, Device, RackDevice


# Create MCP server instance
app = Server("racksum-stats")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="get_site_stats",
            description="Get statistics for all sites including rack count, device count, and resource usage",
            inputSchema={
                "type": "object",
                "properties": {},
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
                    }
                }
            }
        ),
        Tool(
            name="get_resource_summary",
            description="Get overall resource utilization summary across all sites",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "get_site_stats":
        return await get_site_stats()
    elif name == "get_site_details":
        site_name = arguments.get("site_name")
        if not site_name:
            return [TextContent(type="text", text="Error: site_name is required")]
        return await get_site_details(site_name)
    elif name == "get_rack_details":
        site_name = arguments.get("site_name")
        rack_name = arguments.get("rack_name")
        if not site_name or not rack_name:
            return [TextContent(type="text", text="Error: site_name and rack_name are required")]
        return await get_rack_details(site_name, rack_name)
    elif name == "get_available_resources":
        category = arguments.get("category")
        return await get_available_resources(category)
    elif name == "get_resource_summary":
        return await get_resource_summary()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def get_site_stats() -> list[TextContent]:
    """Get statistics for all sites"""
    @sync_to_async
    def get_stats():
        sites = list(Site.objects.all())

        if not sites:
            return "No sites found in the database."

        stats = []
        stats.append("=== SITE STATISTICS ===\n")

        for site in sites:
            racks = list(site.racks.all())
            total_racks = len(racks)
            total_devices = sum(rack.rack_devices.count() for rack in racks)
            total_power = sum(rack.get_power_utilization() for rack in racks)
            total_hvac = sum(rack.get_hvac_load() for rack in racks)

            stats.append(f"\n📍 Site: {site.name}")
            if site.description:
                stats.append(f"   Description: {site.description}")
            stats.append(f"   Racks: {total_racks}")
            stats.append(f"   Devices: {total_devices}")
            stats.append(f"   Total Power: {total_power:,.0f} W ({total_power/1000:.2f} kW)")
            stats.append(f"   Total HVAC Load: {total_hvac:,.0f} BTU/hr ({total_hvac/12000:.2f} tons)")
            stats.append(f"   Created: {site.created_at.strftime('%Y-%m-%d %H:%M')}")

        return "\n".join(stats)

    result = await get_stats()
    return [TextContent(type="text", text=result)]


async def get_site_details(site_name: str) -> list[TextContent]:
    """Get detailed information about a specific site"""
    @sync_to_async
    def get_details():
        try:
            site = Site.objects.get(name=site_name)
        except Site.DoesNotExist:
            return f"Site '{site_name}' not found."

        details = []
        details.append(f"=== SITE DETAILS: {site.name} ===\n")

        if site.description:
            details.append(f"Description: {site.description}")
        details.append(f"Created: {site.created_at.strftime('%Y-%m-%d %H:%M')}")
        details.append(f"Last Updated: {site.updated_at.strftime('%Y-%m-%d %H:%M')}\n")

        racks = list(site.racks.all())
        details.append(f"Total Racks: {len(racks)}\n")

        if racks:
            details.append("--- RACKS ---")
            for rack in racks:
                devices = list(rack.rack_devices.all())
                power = rack.get_power_utilization()
                hvac = rack.get_hvac_load()
                ru_used = sum(device.device.ru_size for device in devices)
                ru_available = rack.ru_height - ru_used

                details.append(f"\n🔲 Rack: {rack.name}")
                if rack.description:
                    details.append(f"   Description: {rack.description}")
                details.append(f"   Height: {rack.ru_height}U")
                details.append(f"   Space Used: {ru_used}U / {rack.ru_height}U ({(ru_used/rack.ru_height*100):.1f}%)")
                details.append(f"   Available: {ru_available}U")
                details.append(f"   Devices: {len(devices)}")
                details.append(f"   Power: {power:,.0f} W ({power/1000:.2f} kW)")
                details.append(f"   HVAC Load: {hvac:,.0f} BTU/hr")

        return "\n".join(details)

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_rack_details(site_name: str, rack_name: str) -> list[TextContent]:
    """Get detailed information about a specific rack"""
    @sync_to_async
    def get_details():
        try:
            site = Site.objects.get(name=site_name)
            rack = Rack.objects.get(site=site, name=rack_name)
        except Site.DoesNotExist:
            return f"Site '{site_name}' not found."
        except Rack.DoesNotExist:
            return f"Rack '{rack_name}' not found in site '{site_name}'."

        details = []
        details.append(f"=== RACK DETAILS: {site.name} - {rack.name} ===\n")

        if rack.description:
            details.append(f"Description: {rack.description}")
        details.append(f"Height: {rack.ru_height}U")
        details.append(f"Created: {rack.created_at.strftime('%Y-%m-%d %H:%M')}")
        details.append(f"Last Updated: {rack.updated_at.strftime('%Y-%m-%d %H:%M')}\n")

        devices = list(rack.rack_devices.all().select_related('device'))
        ru_used = sum(device.device.ru_size for device in devices)
        ru_available = rack.ru_height - ru_used
        power = rack.get_power_utilization()
        hvac = rack.get_hvac_load()

        details.append(f"Space Used: {ru_used}U / {rack.ru_height}U ({(ru_used/rack.ru_height*100):.1f}%)")
        details.append(f"Space Available: {ru_available}U")
        details.append(f"Total Power: {power:,.0f} W ({power/1000:.2f} kW)")
        details.append(f"HVAC Load: {hvac:,.0f} BTU/hr ({hvac/12000:.2f} tons)\n")

        if devices:
            details.append("--- DEVICES ---")
            for rack_device in devices:
                device = rack_device.device
                display_name = rack_device.instance_name or device.name

                details.append(f"\n⚙️  {display_name}")
                details.append(f"   Type: {device.name}")
                details.append(f"   Category: {device.category}")
                details.append(f"   Position: RU {rack_device.position}")
                details.append(f"   Size: {device.ru_size}U")
                details.append(f"   Power: {device.power_draw} W")
                details.append(f"   Heat: {device.power_draw * 3.41:.0f} BTU/hr")
        else:
            details.append("No devices installed in this rack.")

        return "\n".join(details)

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_available_resources(category: str = None) -> list[TextContent]:
    """Get information about available device types"""
    @sync_to_async
    def get_resources():
        devices = Device.objects.all()

        if category:
            devices = devices.filter(category__icontains=category)

        devices_list = list(devices)

        if not devices_list:
            msg = f"No devices found" + (f" in category '{category}'" if category else "")
            return msg + "."

        details = []
        details.append("=== AVAILABLE DEVICE TYPES ===\n")

        # Group by category
        categories = {}
        for device in devices_list:
            if device.category not in categories:
                categories[device.category] = []
            categories[device.category].append(device)

        for cat, cat_devices in sorted(categories.items()):
            details.append(f"\n📦 {cat}")
            for device in cat_devices:
                details.append(f"\n   • {device.name} ({device.device_id})")
                if device.description:
                    details.append(f"     Description: {device.description}")
                details.append(f"     Size: {device.ru_size}U")
                details.append(f"     Power: {device.power_draw} W")
                details.append(f"     Heat: {device.power_draw * 3.41:.0f} BTU/hr")
                details.append(f"     Color: {device.color}")

        details.append(f"\n\nTotal device types: {len(devices_list)}")

        return "\n".join(details)

    result = await get_resources()
    return [TextContent(type="text", text=result)]


async def get_resource_summary() -> list[TextContent]:
    """Get overall resource utilization summary"""
    @sync_to_async
    def get_summary():
        sites = list(Site.objects.all())

        if not sites:
            return "No sites found in the database."

        summary = []
        summary.append("=== RESOURCE UTILIZATION SUMMARY ===\n")

        total_sites = len(sites)
        total_racks = Rack.objects.count()
        total_rack_devices = RackDevice.objects.count()
        total_device_types = Device.objects.count()

        # Calculate overall power and HVAC
        overall_power = 0
        overall_hvac = 0
        total_ru_capacity = 0
        total_ru_used = 0

        for rack in Rack.objects.all():
            overall_power += rack.get_power_utilization()
            overall_hvac += rack.get_hvac_load()
            total_ru_capacity += rack.ru_height
            total_ru_used += sum(device.device.ru_size for device in rack.rack_devices.all())

        summary.append(f"Total Sites: {total_sites}")
        summary.append(f"Total Racks: {total_racks}")
        summary.append(f"Total Devices Installed: {total_rack_devices}")
        summary.append(f"Device Types Available: {total_device_types}\n")

        summary.append("--- CAPACITY ---")
        summary.append(f"Total RU Capacity: {total_ru_capacity}U")
        summary.append(f"Total RU Used: {total_ru_used}U")
        summary.append(f"Total RU Available: {total_ru_capacity - total_ru_used}U")
        if total_ru_capacity > 0:
            summary.append(f"Utilization: {(total_ru_used/total_ru_capacity*100):.1f}%\n")

        summary.append("--- POWER & COOLING ---")
        summary.append(f"Total Power Draw: {overall_power:,.0f} W ({overall_power/1000:.2f} kW)")
        summary.append(f"Total HVAC Load: {overall_hvac:,.0f} BTU/hr ({overall_hvac/12000:.2f} tons)")

        if total_racks > 0:
            avg_power_per_rack = overall_power / total_racks
            summary.append(f"\nAverage per Rack: {avg_power_per_rack:,.0f} W ({avg_power_per_rack/1000:.2f} kW)")

        return "\n".join(summary)

    result = await get_summary()
    return [TextContent(type="text", text=result)]


async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
