"""
MCP tool handler implementations for RackSum datacenter management
"""
import logging
from typing import Optional
from asgiref.sync import sync_to_async
from mcp.types import TextContent

from api.models import Site, Rack, Device, RackDevice
from .formatters import format_power, format_hvac, format_space_utilization, calculate_heat_output

logger = logging.getLogger(__name__)


async def get_site_stats() -> list[TextContent]:
    """Get statistics for all sites"""
    @sync_to_async
    def get_stats():
        try:
            logger.info("Fetching site statistics")
            # Use prefetch_related to avoid N+1 queries
            sites = list(Site.objects.prefetch_related(
                'racks__rack_devices__device'
            ).all())

            if not sites:
                logger.info("No sites found in database")
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
                stats.append(f"   Total Power: {format_power(total_power)}")
                stats.append(f"   Total HVAC Load: {format_hvac(total_hvac)}")
                stats.append(f"   Created: {site.created_at.strftime('%Y-%m-%d %H:%M')}")

            logger.info(f"Successfully retrieved stats for {len(sites)} sites")
            return "\n".join(stats)
        except Exception as e:
            logger.error(f"Error fetching site stats: {e}", exc_info=True)
            return f"Error retrieving site statistics: {str(e)}"

    result = await get_stats()
    return [TextContent(type="text", text=result)]


async def get_site_details(site_name: str) -> list[TextContent]:
    """Get detailed information about a specific site"""
    @sync_to_async
    def get_details():
        try:
            logger.info(f"Fetching details for site: {site_name}")
            # Use prefetch_related to avoid N+1 queries
            # Use case-insensitive lookup for better user experience
            site = Site.objects.prefetch_related(
                'racks__rack_devices__device'
            ).get(name__iexact=site_name)
        except Site.DoesNotExist:
            logger.warning(f"Site not found: {site_name}")
            return f"Site '{site_name}' not found."
        except Exception as e:
            logger.error(f"Error fetching site details: {e}", exc_info=True)
            return f"Error retrieving site details: {str(e)}"

        try:
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
                    details.append(f"   Space Used: {format_space_utilization(ru_used, rack.ru_height)}")
                    details.append(f"   Available: {ru_available}U")
                    details.append(f"   Devices: {len(devices)}")
                    details.append(f"   Power: {format_power(power)}")
                    details.append(f"   HVAC Load: {format_hvac(hvac)}")

            logger.info(f"Successfully retrieved details for site: {site_name}")
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error formatting site details: {e}", exc_info=True)
            return f"Error formatting site details: {str(e)}"

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_rack_details(site_name: str, rack_name: str) -> list[TextContent]:
    """Get detailed information about a specific rack"""
    @sync_to_async
    def get_details():
        try:
            logger.info(f"Fetching rack details: {site_name}/{rack_name}")
            # Use case-insensitive lookups for better user experience
            site = Site.objects.get(name__iexact=site_name)
            rack = Rack.objects.prefetch_related(
                'rack_devices__device'
            ).get(site=site, name__iexact=rack_name)
        except Site.DoesNotExist:
            logger.warning(f"Site not found: {site_name}")
            return f"Site '{site_name}' not found."
        except Rack.DoesNotExist:
            logger.warning(f"Rack not found: {rack_name} in site {site_name}")
            return f"Rack '{rack_name}' not found in site '{site_name}'."
        except Exception as e:
            logger.error(f"Error fetching rack details: {e}", exc_info=True)
            return f"Error retrieving rack details: {str(e)}"

        try:
            details = []
            details.append(f"=== RACK DETAILS: {site.name} - {rack.name} ===\n")

            if rack.description:
                details.append(f"Description: {rack.description}")
            details.append(f"Height: {rack.ru_height}U")
            details.append(f"Created: {rack.created_at.strftime('%Y-%m-%d %H:%M')}")
            details.append(f"Last Updated: {rack.updated_at.strftime('%Y-%m-%d %H:%M')}\n")

            devices = list(rack.rack_devices.all())
            ru_used = sum(device.device.ru_size for device in devices)
            ru_available = rack.ru_height - ru_used
            power = rack.get_power_utilization()
            hvac = rack.get_hvac_load()

            details.append(f"Space Used: {format_space_utilization(ru_used, rack.ru_height)}")
            details.append(f"Space Available: {ru_available}U")
            details.append(f"Total Power: {format_power(power)}")
            details.append(f"HVAC Load: {format_hvac(hvac)}\n")

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
                    details.append(f"   Heat: {calculate_heat_output(device.power_draw):.0f} BTU/hr")
            else:
                details.append("No devices installed in this rack.")

            logger.info(f"Successfully retrieved rack details: {site_name}/{rack_name}")
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error formatting rack details: {e}", exc_info=True)
            return f"Error formatting rack details: {str(e)}"

    result = await get_details()
    return [TextContent(type="text", text=result)]


async def get_available_resources(category: Optional[str] = None, limit: Optional[int] = None) -> list[TextContent]:
    """Get information about available device types"""
    @sync_to_async
    def get_resources():
        try:
            logger.info(f"Fetching available resources{f' for category: {category}' if category else ''}{f' (limit: {limit})' if limit else ''}")
            devices = Device.objects.all()

            if category:
                devices = devices.filter(category__icontains=category)

            # Apply limit if specified
            if limit and limit > 0:
                devices = devices[:limit]

            devices_list = list(devices)

            if not devices_list:
                msg = f"No devices found" + (f" in category '{category}'" if category else "")
                logger.info(msg)
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
                    details.append(f"     Heat: {calculate_heat_output(device.power_draw):.0f} BTU/hr")
                    details.append(f"     Color: {device.color}")

            details.append(f"\n\nTotal device types shown: {len(devices_list)}")
            if limit and limit > 0:
                total_count = Device.objects.filter(category__icontains=category).count() if category else Device.objects.count()
                if total_count > len(devices_list):
                    details.append(f"(Showing first {len(devices_list)} of {total_count} total devices)")

            logger.info(f"Successfully retrieved {len(devices_list)} device types")
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching available resources: {e}", exc_info=True)
            return f"Error retrieving available resources: {str(e)}"

    result = await get_resources()
    return [TextContent(type="text", text=result)]


async def get_resource_summary() -> list[TextContent]:
    """Get overall resource utilization summary"""
    @sync_to_async
    def get_summary():
        try:
            logger.info("Fetching resource summary")
            sites = list(Site.objects.all())

            if not sites:
                logger.info("No sites found in database")
                return "No sites found in the database."

            summary = []
            summary.append("=== RESOURCE UTILIZATION SUMMARY ===\n")

            total_sites = len(sites)
            total_racks = Rack.objects.count()
            total_rack_devices = RackDevice.objects.count()
            total_device_types = Device.objects.count()

            # Calculate overall power and HVAC - use prefetch_related to avoid N+1 queries
            overall_power = 0
            overall_hvac = 0
            total_ru_capacity = 0
            total_ru_used = 0

            # Fetch all racks with their devices in a single query
            racks = Rack.objects.prefetch_related('rack_devices__device').all()
            for rack in racks:
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
            summary.append(f"Total Power Draw: {format_power(overall_power)}")
            summary.append(f"Total HVAC Load: {format_hvac(overall_hvac)}")

            if total_racks > 0:
                avg_power_per_rack = overall_power / total_racks
                summary.append(f"\nAverage per Rack: {format_power(avg_power_per_rack)}")

            logger.info(f"Successfully retrieved resource summary: {total_sites} sites, {total_racks} racks")
            return "\n".join(summary)
        except Exception as e:
            logger.error(f"Error fetching resource summary: {e}", exc_info=True)
            return f"Error retrieving resource summary: {str(e)}"

    result = await get_summary()
    return [TextContent(type="text", text=result)]
