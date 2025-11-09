# API Workflow Guide

This guide demonstrates how to use the Racker API to programmatically manage device types, create sites, and populate them with unracked devices.

## Overview

The typical workflow involves:

1. **Define Custom Device Types** - Add your equipment to the device library
2. **Create Device Groups** - Organize devices into logical categories
3. **Create a Site** - Set up a new datacenter or location
4. **Add Unracked Devices** - Populate the site with devices ready for placement

## Prerequisites

- Racker backend running (default: `http://localhost:3000`)
- API endpoint: `http://localhost:3000/api`
- Tools: `curl`, `jq`, or any HTTP client

## Authentication

!!! note "Authentication Status"
    If authentication is **disabled** (default), no credentials are required. All users share the same data.

    If authentication is **enabled**, you'll need to include authentication headers with your requests.

## 1. Adding Custom Device Types

Device types define the equipment available in your library. Each device has properties like RU size, power draw, and color.

### Device Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `device_id` | string | Yes | Unique identifier (e.g., "dell-r750-custom") |
| `name` | string | Yes | Display name (e.g., "Dell PowerEdge R750") |
| `category` | string | Yes | Device category/group |
| `ru_size` | integer | Yes | Rack units consumed (1-42) |
| `power_draw` | integer | Yes | Power consumption in watts |
| `power_ports_used` | integer | No | Number of PDU ports required (default: 1) |
| `color` | string | No | Hex color code (default: "#000000") |
| `description` | string | No | Additional details |

### Add a Device Type

```bash
curl -X POST http://localhost:3000/api/devices \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "dell-r750-custom",
    "name": "Dell PowerEdge R750",
    "category": "servers",
    "ru_size": 2,
    "power_draw": 1400,
    "power_ports_used": 2,
    "color": "#8E44AD",
    "description": "2U dual-socket server with dual PSU"
  }'
```

### Add Multiple Device Types

```bash
# Create a devices file
cat > custom_devices.json << 'EOF'
{
  "devices": [
    {
      "device_id": "cisco-n9k-c93180yc",
      "name": "Cisco Nexus 9300 48-port",
      "category": "network",
      "ru_size": 1,
      "power_draw": 425,
      "power_ports_used": 2,
      "color": "#3498DB",
      "description": "48x25G + 6x100G switch"
    },
    {
      "device_id": "apc-srt10kxlt",
      "name": "APC Smart-UPS SRT 10kVA",
      "category": "power",
      "ru_size": 6,
      "power_draw": 150,
      "color": "#E74C3C",
      "description": "10kVA/10kW UPS with extended runtime"
    },
    {
      "device_id": "netapp-a250",
      "name": "NetApp AFF A250",
      "category": "storage",
      "ru_size": 2,
      "power_draw": 800,
      "power_ports_used": 2,
      "color": "#16A085",
      "description": "All-flash storage system"
    }
  ]
}
EOF

# Import each device
jq -c '.devices[]' custom_devices.json | while read device; do
  curl -X POST http://localhost:3000/api/devices \
    -H "Content-Type: application/json" \
    -d "$device"
done
```

### List All Devices

```bash
curl http://localhost:3000/api/devices | jq
```

## 2. Creating Device Groups

!!! info "Device Groups"
    Device groups are managed client-side via localStorage. The API provides device types with categories, which the UI groups automatically.

    To create custom groups, use the **Device Manager** in the UI or manage them via the Import/Export feature.

## 3. Creating a Site

Sites represent physical locations or datacenters. Each site gets a unique UUID for sharing.

### Create a Site

```bash
# Create a site
SITE_RESPONSE=$(curl -s -X POST http://localhost:3000/api/sites \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DataCenter East",
    "description": "Primary east coast facility"
  }')

# Extract site ID and UUID
SITE_ID=$(echo $SITE_RESPONSE | jq -r '.id')
SITE_UUID=$(echo $SITE_RESPONSE | jq -r '.uuid')

echo "Site ID: $SITE_ID"
echo "Site UUID: $SITE_UUID"
echo "Share URL: http://localhost:5173?site=$SITE_UUID"
```

### Response Format

```json
{
  "id": 1,
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "DataCenter East",
  "description": "Primary east coast facility",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List All Sites

```bash
curl http://localhost:3000/api/sites | jq
```

### Get Site by UUID

```bash
curl http://localhost:3000/api/sites/by-uuid/$SITE_UUID | jq
```

## 4. Creating Rack Configurations with Unracked Devices

Rack configurations store your complete rack layout, including unracked devices waiting for placement.

### Configuration Structure

```json
{
  "name": "Main Config",
  "description": "Primary rack configuration",
  "config_data": {
    "settings": {
      "totalPowerCapacity": 20000,
      "hvacCapacity": 68200,
      "ruPerRack": 42
    },
    "racks": [
      {
        "id": "rack-1",
        "name": "Rack A1",
        "devices": []
      }
    ],
    "unrackedDevices": [
      {
        "id": "dell-r750-custom",
        "name": "Dell PowerEdge R750",
        "category": "servers",
        "ruSize": 2,
        "powerDraw": 1400,
        "color": "#8E44AD",
        "instanceId": "server-001",
        "customName": "ESXi Host 1"
      }
    ]
  }
}
```

### Create Configuration with Unracked Devices

```bash
curl -X POST http://localhost:3000/api/sites/$SITE_ID/racks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Config",
    "description": "Production environment rack layout",
    "config_data": {
      "settings": {
        "totalPowerCapacity": 20000,
        "hvacCapacity": 68200,
        "ruPerRack": 42
      },
      "racks": [
        {
          "id": "rack-1",
          "name": "Rack A1",
          "devices": []
        },
        {
          "id": "rack-2",
          "name": "Rack A2",
          "devices": []
        }
      ],
      "unrackedDevices": [
        {
          "id": "dell-r750-custom",
          "ruSize": 2,
          "powerDraw": 1400,
          "instanceId": "esxi-01",
          "customName": "ESXi Host 1"
        },
        {
          "id": "dell-r750-custom",
          "ruSize": 2,
          "powerDraw": 1400,
          "instanceId": "esxi-02",
          "customName": "ESXi Host 2"
        },
        {
          "id": "cisco-n9k-c93180yc",
          "ruSize": 1,
          "powerDraw": 425,
          "instanceId": "sw-core-01",
          "customName": "Core Switch 1"
        }
      ]
    }
  }'
```

### Load Configuration in UI

Once created, users can:

1. **Visit share URL**: `http://localhost:5173?site=$SITE_UUID`
2. **Use Load dialog**: Click "Load" → Select site and configuration
3. **Drag unracked devices**: From the Unracked Devices panel into racks

## 5. Complete Workflow Example

### Python Script

```python
#!/usr/bin/env python3
import requests
import json

API_BASE = "http://localhost:3000/api"

def create_device_type(device):
    """Add a custom device type"""
    response = requests.post(f"{API_BASE}/devices", json=device)
    response.raise_for_status()
    return response.json()

def create_site(name, description=""):
    """Create a new site"""
    response = requests.post(
        f"{API_BASE}/sites",
        json={"name": name, "description": description}
    )
    response.raise_for_status()
    return response.json()

def create_rack_config(site_id, name, config_data, description=""):
    """Create a rack configuration for a site"""
    response = requests.post(
        f"{API_BASE}/sites/{site_id}/racks",
        json={
            "name": name,
            "description": description,
            "config_data": config_data
        }
    )
    response.raise_for_status()
    return response.json()

# Step 1: Add custom device types
print("Adding custom device types...")
devices = [
    {
        "device_id": "supermicro-sys-1029u",
        "name": "Supermicro 1029U-TN10RT",
        "category": "servers",
        "ru_size": 1,
        "power_draw": 750,
        "power_ports_used": 2,
        "color": "#9B59B6"
    },
    {
        "device_id": "arista-7050sx3",
        "name": "Arista 7050SX3-48YC8",
        "category": "network",
        "ru_size": 1,
        "power_draw": 350,
        "power_ports_used": 2,
        "color": "#3498DB"
    }
]

for device in devices:
    try:
        create_device_type(device)
        print(f"  ✓ Added {device['name']}")
    except Exception as e:
        print(f"  ✗ Failed to add {device['name']}: {e}")

# Step 2: Create a site
print("\nCreating site...")
site = create_site("DataCenter West", "West coast facility")
print(f"  ✓ Site created: {site['name']}")
print(f"  ✓ Site UUID: {site['uuid']}")
print(f"  ✓ Share URL: http://localhost:5173?site={site['uuid']}")

# Step 3: Create rack configuration with unracked devices
print("\nCreating rack configuration...")
config_data = {
    "settings": {
        "totalPowerCapacity": 30000,
        "hvacCapacity": 102300,
        "ruPerRack": 42
    },
    "racks": [
        {"id": "rack-1", "name": "Rack 1", "devices": []},
        {"id": "rack-2", "name": "Rack 2", "devices": []},
        {"id": "rack-3", "name": "Rack 3", "devices": []}
    ],
    "unrackedDevices": [
        {
            "id": "supermicro-sys-1029u",
            "ruSize": 1,
            "powerDraw": 750,
            "instanceId": f"compute-{i:02d}",
            "customName": f"Compute Node {i:02d}"
        } for i in range(1, 11)
    ] + [
        {
            "id": "arista-7050sx3",
            "ruSize": 1,
            "powerDraw": 350,
            "instanceId": f"switch-{i:02d}",
            "customName": f"Leaf Switch {i:02d}"
        } for i in range(1, 5)
    ]
}

rack_config = create_rack_config(
    site['id'],
    "Production",
    config_data,
    "Production environment with 10 compute nodes and 4 switches"
)

print(f"  ✓ Configuration created: {rack_config['name']}")
print(f"  ✓ Unracked devices: {len(config_data['unrackedDevices'])}")
print(f"\nUsers can now visit the share URL to plan rack placement!")
```

### Bash Script

```bash
#!/bin/bash
set -e

API_BASE="http://localhost:3000/api"

# Step 1: Add device types
echo "Adding device types..."
curl -s -X POST "$API_BASE/devices" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "hpe-dl360-gen10",
    "name": "HPE ProLiant DL360 Gen10",
    "category": "servers",
    "ru_size": 1,
    "power_draw": 500,
    "power_ports_used": 2,
    "color": "#2ECC71"
  }' > /dev/null
echo "  ✓ Added HPE DL360"

# Step 2: Create site
echo -e "\nCreating site..."
SITE=$(curl -s -X POST "$API_BASE/sites" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lab Environment",
    "description": "Testing and development lab"
  }')

SITE_ID=$(echo $SITE | jq -r '.id')
SITE_UUID=$(echo $SITE | jq -r '.uuid')
SITE_NAME=$(echo $SITE | jq -r '.name')

echo "  ✓ Site: $SITE_NAME"
echo "  ✓ UUID: $SITE_UUID"
echo "  ✓ URL:  http://localhost:5173?site=$SITE_UUID"

# Step 3: Create rack config with unracked devices
echo -e "\nCreating configuration..."
curl -s -X POST "$API_BASE/sites/$SITE_ID/racks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lab Config",
    "config_data": {
      "settings": {
        "totalPowerCapacity": 10000,
        "hvacCapacity": 34100,
        "ruPerRack": 42
      },
      "racks": [
        {"id": "rack-1", "name": "Lab Rack", "devices": []}
      ],
      "unrackedDevices": [
        {
          "id": "hpe-dl360-gen10",
          "ruSize": 1,
          "powerDraw": 500,
          "instanceId": "lab-server-01",
          "customName": "Lab Server 1"
        },
        {
          "id": "hpe-dl360-gen10",
          "ruSize": 1,
          "powerDraw": 500,
          "instanceId": "lab-server-02",
          "customName": "Lab Server 2"
        }
      ]
    }
  }' > /dev/null

echo "  ✓ Configuration created with 2 unracked devices"
echo -e "\nDone! Visit the share URL to start planning."
```

## 6. Advanced Patterns

### Bulk Import from Inventory System

```python
import requests
import csv

API_BASE = "http://localhost:3000/api"

# Read from CSV inventory
with open('inventory.csv', 'r') as f:
    reader = csv.DictReader(f)
    devices = []

    for row in reader:
        device = {
            "id": row['model'].lower().replace(' ', '-'),
            "name": row['model'],
            "ruSize": int(row['ru_size']),
            "powerDraw": int(row['power_watts']),
            "instanceId": row['serial_number'],
            "customName": row['hostname']
        }
        devices.append(device)

# Create site and config
site = requests.post(f"{API_BASE}/sites", json={
    "name": "Auto-Import Site"
}).json()

config_data = {
    "settings": {
        "totalPowerCapacity": 50000,
        "hvacCapacity": 170500,
        "ruPerRack": 42
    },
    "racks": [
        {"id": f"rack-{i}", "name": f"Rack {i}", "devices": []}
        for i in range(1, 6)
    ],
    "unrackedDevices": devices
}

requests.post(
    f"{API_BASE}/sites/{site['id']}/racks",
    json={"name": "Import", "config_data": config_data}
)
```

### Pre-populate Racks with Devices

```json
{
  "racks": [
    {
      "id": "rack-1",
      "name": "Network Rack",
      "devices": [
        {
          "id": "cisco-n9k-c93180yc",
          "position": 1,
          "ruSize": 1,
          "powerDraw": 425,
          "instanceId": "sw-01",
          "customName": "Core Switch 1"
        },
        {
          "id": "cisco-n9k-c93180yc",
          "position": 2,
          "ruSize": 1,
          "powerDraw": 425,
          "instanceId": "sw-02",
          "customName": "Core Switch 2"
        }
      ]
    }
  ]
}
```

## API Reference

For complete API documentation, see:

- [API Documentation](api.md) - Full endpoint reference
- [Swagger UI](http://localhost:3000/api/schema/swagger-ui/) - Interactive API explorer
- [OpenAPI Schema](http://localhost:3000/api/schema/) - Machine-readable spec

## Best Practices

1. **Unique Device IDs**: Use clear, consistent naming (e.g., `vendor-model-variant`)
2. **Realistic Power Values**: Include overhead for dual PSUs, redundancy
3. **Meaningful Names**: Use descriptive `customName` values for instances
4. **Power Port Tracking**: Set `power_ports_used` for dual-PSU equipment
5. **Color Coding**: Use consistent colors per category for visual clarity
6. **Batch Operations**: Use scripts for bulk imports rather than manual API calls

## Troubleshooting

### Device Already Exists

```bash
# Error: Device with this device_id already exists
# Solution: Use a different device_id or update the existing device
```

### Site Name Conflict

```bash
# Error: A site with this name already exists
# Solution: Use a unique site name or update the existing site
```

### Invalid Configuration

```bash
# Ensure config_data includes required fields:
# - settings.totalPowerCapacity
# - settings.hvacCapacity
# - settings.ruPerRack
# - racks (array with at least one rack)
```

## Next Steps

- [Usage Guide](usage.md) - Learn the UI features
- [Resource Providers](RESOURCE_PROVIDERS_GUIDE.md) - Configure power/cooling infrastructure
- [Custom Devices](CUSTOM_DEVICES_GUIDE.md) - UI-based device management
