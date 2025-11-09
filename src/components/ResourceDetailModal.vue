<template>
  <div v-if="visible" class="modal modal-open" @click.self="close">
    <div class="modal-box w-full max-w-4xl">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">Resource Usage Details</h2>
        <button @click="close" class="btn btn-ghost btn-sm btn-circle text-primary-content">
          <svg class="size-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <!-- Tab Navigation -->
        <div role="tablist" class="tabs tabs-border">
          <button
            role="tab"
            class="tab"
            :class="{ 'tab-active': activeTab === 'consumption' }"
            @click="activeTab = 'consumption'"
          >
            Device Consumption
          </button>
          <button
            role="tab"
            class="tab"
            :class="{ 'tab-active': activeTab === 'providers' }"
            @click="activeTab = 'providers'"
          >
            Resource Providers
          </button>
        </div>

        <!-- Summary Cards -->
        <div class="grid grid-cols-3 gap-4 mb-6">
          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Total Power</div>
            <div class="stat-value text-2xl">{{ powerUsed }}W</div>
            <div class="stat-desc">{{ powerPercentage }}% of {{ powerCapacity }}W</div>
          </div>
          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Total HVAC Load</div>
            <div class="stat-value text-2xl">{{ hvacLoad }} BTU/hr</div>
            <div class="stat-desc">{{ hvacPercentage }}% of {{ hvacCapacity }} BTU/hr</div>
          </div>
          <div class="stat bg-base-200 rounded-lg">
            <div class="stat-title">Total Rack Units</div>
            <div class="stat-value text-2xl">{{ ruUsed }}U</div>
            <div class="stat-desc">{{ ruPercentage }}% of {{ ruCapacity }}U</div>
          </div>
        </div>

        <!-- Device Consumption Tab -->
        <div v-if="activeTab === 'consumption'" class="overflow-auto" style="max-height: 500px;">
          <table class="table table-pin-rows">
            <thead>
              <tr>
                <th>Device</th>
                <th>Location</th>
                <th class="text-right">Power (W)</th>
                <th class="text-right">Power %</th>
                <th class="text-right">HVAC (BTU/hr)</th>
                <th class="text-right">HVAC %</th>
                <th class="text-right">RU</th>
                <th class="text-right">RU %</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in deviceList" :key="item.key" class="hover">
                <td>
                  <div class="flex items-center gap-2">
                    <div class="size-3 rounded-full" :style="{ backgroundColor: item.color }"></div>
                    <span class="text-sm font-medium">{{ item.name }}</span>
                  </div>
                </td>
                <td class="text-sm opacity-70">{{ item.location }}</td>
                <td class="text-sm text-right font-mono">{{ item.powerDraw }}</td>
                <td class="text-sm text-right opacity-70">
                  <div class="flex items-center justify-end gap-2">
                    <div class="size-2 rounded-full" :class="getStatusColor(item.powerPercentage)"></div>
                    {{ item.powerPercentage }}%
                  </div>
                </td>
                <td class="text-sm text-right font-mono">{{ item.hvacLoad }}</td>
                <td class="text-sm text-right opacity-70">
                  <div class="flex items-center justify-end gap-2">
                    <div class="size-2 rounded-full" :class="getStatusColor(item.hvacPercentage)"></div>
                    {{ item.hvacPercentage }}%
                  </div>
                </td>
                <td class="text-sm text-right font-mono">{{ item.ruSize }}</td>
                <td class="text-sm text-right opacity-70">
                  <div class="flex items-center justify-end gap-2">
                    <div class="size-2 rounded-full" :class="getStatusColor(item.ruPercentage)"></div>
                    {{ item.ruPercentage }}%
                  </div>
                </td>
              </tr>
              <tr v-if="deviceList.length === 0">
                <td colspan="8" class="p-8 text-center opacity-70">No devices found</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Resource Providers Tab -->
        <div v-if="activeTab === 'providers'">
          <div v-if="resourceProviders.length === 0" class="p-8 text-center text-base-content/60">
            <p class="text-sm mb-2">
              No resource providers configured
            </p>
            <p class="text-xs">
              Resource providers define what provides power, cooling, and network capacity to your site.
              Add them in the Device Manager under the "Resource Providers" tab.
            </p>
          </div>

          <div v-else class="space-y-6">
          <!-- Power Providers -->
          <div v-if="getPowerProviders.length > 0">
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
              </svg>
              Power Providers
            </h3>
            <div class="overflow-auto" style="max-height: 200px;">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th class="text-left">Provider</th>
                    <th class="text-left">Location</th>
                    <th class="text-right">Capacity (W)</th>
                    <th class="text-right">Used (W)</th>
                    <th class="text-right">Utilization</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="provider in getPowerProviders" :key="provider.id" class="hover">
                    <td class="font-medium">
                      {{ provider.name }}
                    </td>
                    <td class="opacity-70">
                      {{ provider.location || '-' }}
                    </td>
                    <td class="text-right font-mono">
                      {{ provider.powerCapacity.toLocaleString() }}
                    </td>
                    <td class="text-right font-mono">
                      {{ Math.round((powerUsed / totalPowerCapacity) * provider.powerCapacity).toLocaleString() }}
                    </td>
                    <td class="text-right">
                      <div class="flex items-center justify-end gap-2">
                        <div class="w-2 h-2 rounded-full" :class="getStatusColor(((powerUsed / totalPowerCapacity) * 100).toFixed(2))"></div>
                        <span class="opacity-70">
                          {{ ((powerUsed / totalPowerCapacity) * 100).toFixed(1) }}%
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr class="font-semibold bg-base-200">
                    <td colspan="2">Total Power Capacity</td>
                    <td class="text-right font-mono">
                      {{ totalPowerCapacity.toLocaleString() }}
                    </td>
                    <td class="text-right font-mono">
                      {{ powerUsed.toLocaleString() }}
                    </td>
                    <td class="text-right">
                      {{ powerPercentage }}%
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Cooling Providers -->
          <div v-if="getCoolingProviders.length > 0">
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
              </svg>
              Cooling Providers
            </h3>
            <div class="overflow-auto" style="max-height: 200px;">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th class="text-left">Provider</th>
                    <th class="text-left">Location</th>
                    <th class="text-right">Capacity (Tons)</th>
                    <th class="text-right">Load (Tons)</th>
                    <th class="text-right">Utilization</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="provider in getCoolingProviders" :key="provider.id" class="hover">
                    <td class="font-medium">
                      {{ provider.name }}
                    </td>
                    <td class="opacity-70">
                      {{ provider.location || '-' }}
                    </td>
                    <td class="text-right font-mono">
                      {{ (provider.coolingCapacity / 12000).toFixed(1) }}
                    </td>
                    <td class="text-right font-mono">
                      {{ (((hvacLoad / totalCoolingCapacity) * provider.coolingCapacity) / 12000).toFixed(1) }}
                    </td>
                    <td class="text-right">
                      <div class="flex items-center justify-end gap-2">
                        <div class="w-2 h-2 rounded-full" :class="getStatusColor(((hvacLoad / totalCoolingCapacity) * 100).toFixed(2))"></div>
                        <span class="opacity-70">
                          {{ ((hvacLoad / totalCoolingCapacity) * 100).toFixed(1) }}%
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr class="font-semibold bg-base-200">
                    <td colspan="2">Total Cooling Capacity</td>
                    <td class="text-right font-mono">
                      {{ (totalCoolingCapacity / 12000).toFixed(1) }}
                    </td>
                    <td class="text-right font-mono">
                      {{ (hvacLoad / 12000).toFixed(1) }}
                    </td>
                    <td class="text-right">
                      {{ hvacPercentage }}%
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Note if using legacy config -->
          <div v-if="!usingResourceProviders" class="alert alert-warning">
            <div>
              <div class="font-bold">ℹ️ Note</div>
              <div class="text-sm">
                You're currently using static capacity values from the configuration.
                Switch to Resource Providers for more flexible capacity management in the Device Manager.
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>

      <!-- Close Button -->
      <div class="flex justify-end gap-2 mt-6">
        <button @click="close" class="btn">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useUtilization } from '../composables/useUtilization'
import { useResourceProviders } from '../composables/useResourceProviders'
import { calculateHeatLoad } from '../utils/calculations'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const activeTab = ref('consumption')

const { config } = useRackConfig()
const {
  powerUsed,
  powerCapacity,
  powerPercentage,
  hvacLoad,
  hvacCapacity,
  hvacPercentage,
  ruUsed,
  ruCapacity,
  ruPercentage,
  usingResourceProviders
} = useUtilization()

const {
  resourceProviders,
  totalPowerCapacity,
  totalCoolingCapacity,
  getPowerProviders,
  getCoolingProviders
} = useResourceProviders()

// Build device list with all devices from racks and unracked
const deviceList = computed(() => {
  const devices = []

  // Add devices from racks
  config.value.racks.forEach((rack) => {
    rack.devices.forEach((device) => {
      const devicePower = device.powerDraw || 0
      const deviceHvac = Math.round(calculateHeatLoad(devicePower))
      const deviceRu = device.ruSize || 0

      devices.push({
        key: device.instanceId,
        name: device.customName || device.name,
        location: `${rack.name} (U${device.position})`,
        color: device.color,
        powerDraw: devicePower,
        powerPercentage: powerCapacity.value > 0
          ? ((devicePower / powerCapacity.value) * 100).toFixed(2)
          : '0.00',
        hvacLoad: deviceHvac,
        hvacPercentage: hvacCapacity.value > 0
          ? ((deviceHvac / hvacCapacity.value) * 100).toFixed(2)
          : '0.00',
        ruSize: deviceRu,
        ruPercentage: ruCapacity.value > 0
          ? ((deviceRu / ruCapacity.value) * 100).toFixed(2)
          : '0.00'
      })
    })
  })

  // Add unracked devices
  if (config.value.unrackedDevices) {
    config.value.unrackedDevices.forEach((device) => {
      const devicePower = device.powerDraw || 0
      const deviceHvac = Math.round(calculateHeatLoad(devicePower))
      const deviceRu = device.ruSize || 0

      devices.push({
        key: device.instanceId,
        name: device.customName || device.name,
        location: 'Unracked',
        color: device.color,
        powerDraw: devicePower,
        powerPercentage: powerCapacity.value > 0
          ? ((devicePower / powerCapacity.value) * 100).toFixed(2)
          : '0.00',
        hvacLoad: deviceHvac,
        hvacPercentage: hvacCapacity.value > 0
          ? ((deviceHvac / hvacCapacity.value) * 100).toFixed(2)
          : '0.00',
        ruSize: deviceRu,
        ruPercentage: ruCapacity.value > 0
          ? ((deviceRu / ruCapacity.value) * 100).toFixed(2)
          : '0.00'
      })
    })
  }

  // Sort by power draw (descending)
  return devices.sort((a, b) => b.powerDraw - a.powerDraw)
})

const getStatusColor = (percentage) => {
  const num = parseFloat(percentage)
  if (num < 1) return 'bg-green-500'
  if (num < 3) return 'bg-yellow-500'
  return 'bg-red-500'
}

const close = () => {
  visible.value = false
}
</script>

<style scoped>
.space-y-4 > * + * {
  margin-top: 1rem;
}

.grid {
  display: grid;
}

.grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.gap-4 {
  gap: 1rem;
}
</style>
