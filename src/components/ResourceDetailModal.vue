<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="Resource Usage Details"
    :style="{ width: '900px' }"
    :closable="true"
  >
    <div class="space-y-4">
      <!-- Tab Navigation -->
      <div class="flex gap-2 mb-4" style="border-bottom: 2px solid var(--border-color);">
        <button
          @click="activeTab = 'consumption'"
          class="px-4 py-2 font-medium transition-colors"
          :style="{
            color: activeTab === 'consumption' ? 'var(--color-primary)' : 'var(--text-secondary)',
            borderBottom: activeTab === 'consumption' ? '2px solid var(--color-primary)' : '2px solid transparent',
            marginBottom: '-2px'
          }"
        >
          Device Consumption
        </button>
        <button
          @click="activeTab = 'providers'"
          class="px-4 py-2 font-medium transition-colors"
          :style="{
            color: activeTab === 'providers' ? 'var(--color-primary)' : 'var(--text-secondary)',
            borderBottom: activeTab === 'providers' ? '2px solid var(--color-primary)' : '2px solid transparent',
            marginBottom: '-2px'
          }"
        >
          Resource Providers
        </button>
      </div>

      <!-- Summary Cards -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="p-4 rounded-lg" style="background-color: var(--bg-secondary);">
          <div class="text-sm" style="color: var(--text-secondary);">Total Power</div>
          <div class="text-2xl font-bold mt-1" style="color: var(--text-primary);">
            {{ powerUsed }}W
          </div>
          <div class="text-xs mt-1" style="color: var(--text-secondary);">
            {{ powerPercentage }}% of {{ powerCapacity }}W
          </div>
        </div>
        <div class="p-4 rounded-lg" style="background-color: var(--bg-secondary);">
          <div class="text-sm" style="color: var(--text-secondary);">Total HVAC Load</div>
          <div class="text-2xl font-bold mt-1" style="color: var(--text-primary);">
            {{ hvacLoad }} BTU/hr
          </div>
          <div class="text-xs mt-1" style="color: var(--text-secondary);">
            {{ hvacPercentage }}% of {{ hvacCapacity }} BTU/hr
          </div>
        </div>
        <div class="p-4 rounded-lg" style="background-color: var(--bg-secondary);">
          <div class="text-sm" style="color: var(--text-secondary);">Total Rack Units</div>
          <div class="text-2xl font-bold mt-1" style="color: var(--text-primary);">
            {{ ruUsed }}U
          </div>
          <div class="text-xs mt-1" style="color: var(--text-secondary);">
            {{ ruPercentage }}% of {{ ruCapacity }}U
          </div>
        </div>
      </div>

      <!-- Device Consumption Tab -->
      <div v-if="activeTab === 'consumption'" class="overflow-auto" style="max-height: 500px;">
        <table class="w-full">
          <thead class="sticky top-0" style="background-color: var(--bg-primary); border-bottom: 2px solid var(--border-color);">
            <tr>
              <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Device</th>
              <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Location</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Power (W)</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Power %</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">HVAC (BTU/hr)</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">HVAC %</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">RU</th>
              <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">RU %</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in deviceList"
              :key="item.key"
              class="border-b transition-colors hover:bg-opacity-50"
              style="border-color: var(--border-color);"
              @mouseover="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
              @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
            >
              <td class="p-3">
                <div class="flex items-center gap-2">
                  <div
                    class="w-3 h-3 rounded-full"
                    :style="{ backgroundColor: item.color }"
                  ></div>
                  <span class="text-sm font-medium" style="color: var(--text-primary);">
                    {{ item.name }}
                  </span>
                </div>
              </td>
              <td class="p-3 text-sm" style="color: var(--text-secondary);">
                {{ item.location }}
              </td>
              <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                {{ item.powerDraw }}
              </td>
              <td class="p-3 text-sm text-right" style="color: var(--text-secondary);">
                <div class="flex items-center justify-end gap-2">
                  <div
                    class="w-2 h-2 rounded-full"
                    :class="getStatusColor(item.powerPercentage)"
                  ></div>
                  {{ item.powerPercentage }}%
                </div>
              </td>
              <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                {{ item.hvacLoad }}
              </td>
              <td class="p-3 text-sm text-right" style="color: var(--text-secondary);">
                <div class="flex items-center justify-end gap-2">
                  <div
                    class="w-2 h-2 rounded-full"
                    :class="getStatusColor(item.hvacPercentage)"
                  ></div>
                  {{ item.hvacPercentage }}%
                </div>
              </td>
              <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                {{ item.ruSize }}
              </td>
              <td class="p-3 text-sm text-right" style="color: var(--text-secondary);">
                <div class="flex items-center justify-end gap-2">
                  <div
                    class="w-2 h-2 rounded-full"
                    :class="getStatusColor(item.ruPercentage)"
                  ></div>
                  {{ item.ruPercentage }}%
                </div>
              </td>
            </tr>
            <tr v-if="deviceList.length === 0">
              <td colspan="8" class="p-8 text-center" style="color: var(--text-secondary);">
                No devices found
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Resource Providers Tab -->
      <div v-if="activeTab === 'providers'">
        <div v-if="resourceProviders.length === 0" class="p-8 text-center">
          <p class="text-sm mb-2" style="color: var(--text-secondary);">
            No resource providers configured
          </p>
          <p class="text-xs" style="color: var(--text-secondary);">
            Resource providers define what provides power, cooling, and network capacity to your site.
            Add them in the Device Manager under the "Resource Providers" tab.
          </p>
        </div>

        <div v-else class="space-y-6">
          <!-- Power Providers -->
          <div v-if="getPowerProviders.length > 0">
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2" style="color: var(--text-primary);">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
              </svg>
              Power Providers
            </h3>
            <div class="overflow-auto" style="max-height: 200px;">
              <table class="w-full">
                <thead style="background-color: var(--bg-secondary);">
                  <tr>
                    <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Provider</th>
                    <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Location</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Capacity (W)</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Used (W)</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Utilization</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="provider in getPowerProviders"
                    :key="provider.id"
                    class="border-b transition-colors"
                    style="border-color: var(--border-color);"
                    @mouseover="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
                    @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  >
                    <td class="p-3 text-sm font-medium" style="color: var(--text-primary);">
                      {{ provider.name }}
                    </td>
                    <td class="p-3 text-sm" style="color: var(--text-secondary);">
                      {{ provider.location || '-' }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ provider.powerCapacity.toLocaleString() }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ Math.round((powerUsed / totalPowerCapacity) * provider.powerCapacity).toLocaleString() }}
                    </td>
                    <td class="p-3 text-sm text-right">
                      <div class="flex items-center justify-end gap-2">
                        <div
                          class="w-2 h-2 rounded-full"
                          :class="getStatusColor(((powerUsed / totalPowerCapacity) * 100).toFixed(2))"
                        ></div>
                        <span style="color: var(--text-secondary);">
                          {{ ((powerUsed / totalPowerCapacity) * 100).toFixed(1) }}%
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr class="font-semibold" style="background-color: var(--bg-secondary);">
                    <td colspan="2" class="p-3 text-sm" style="color: var(--text-primary);">Total Power Capacity</td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ totalPowerCapacity.toLocaleString() }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ powerUsed.toLocaleString() }}
                    </td>
                    <td class="p-3 text-sm text-right" style="color: var(--text-primary);">
                      {{ powerPercentage }}%
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Cooling Providers -->
          <div v-if="getCoolingProviders.length > 0">
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2" style="color: var(--text-primary);">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
              </svg>
              Cooling Providers
            </h3>
            <div class="overflow-auto" style="max-height: 200px;">
              <table class="w-full">
                <thead style="background-color: var(--bg-secondary);">
                  <tr>
                    <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Provider</th>
                    <th class="text-left p-3 text-sm font-semibold" style="color: var(--text-primary);">Location</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Capacity (Tons)</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Load (Tons)</th>
                    <th class="text-right p-3 text-sm font-semibold" style="color: var(--text-primary);">Utilization</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="provider in getCoolingProviders"
                    :key="provider.id"
                    class="border-b transition-colors"
                    style="border-color: var(--border-color);"
                    @mouseover="$event.currentTarget.style.backgroundColor = 'var(--bg-secondary)'"
                    @mouseout="$event.currentTarget.style.backgroundColor = 'transparent'"
                  >
                    <td class="p-3 text-sm font-medium" style="color: var(--text-primary);">
                      {{ provider.name }}
                    </td>
                    <td class="p-3 text-sm" style="color: var(--text-secondary);">
                      {{ provider.location || '-' }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ (provider.coolingCapacity / 12000).toFixed(1) }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ (((hvacLoad / totalCoolingCapacity) * provider.coolingCapacity) / 12000).toFixed(1) }}
                    </td>
                    <td class="p-3 text-sm text-right">
                      <div class="flex items-center justify-end gap-2">
                        <div
                          class="w-2 h-2 rounded-full"
                          :class="getStatusColor(((hvacLoad / totalCoolingCapacity) * 100).toFixed(2))"
                        ></div>
                        <span style="color: var(--text-secondary);">
                          {{ ((hvacLoad / totalCoolingCapacity) * 100).toFixed(1) }}%
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr class="font-semibold" style="background-color: var(--bg-secondary);">
                    <td colspan="2" class="p-3 text-sm" style="color: var(--text-primary);">Total Cooling Capacity</td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ (totalCoolingCapacity / 12000).toFixed(1) }}
                    </td>
                    <td class="p-3 text-sm text-right font-mono" style="color: var(--text-primary);">
                      {{ (hvacLoad / 12000).toFixed(1) }}
                    </td>
                    <td class="p-3 text-sm text-right" style="color: var(--text-primary);">
                      {{ hvacPercentage }}%
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Note if using legacy config -->
          <div v-if="!usingResourceProviders" class="p-4 rounded border" style="background-color: rgba(251, 191, 36, 0.1); border-color: #fbbf24;">
            <p class="text-sm" style="color: var(--text-primary);">
              <strong>ℹ️ Note:</strong> You're currently using static capacity values from the configuration.
              Switch to Resource Providers for more flexible capacity management in the Device Manager.
            </p>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <Button
        label="Close"
        severity="secondary"
        @click="close"
        outlined
      />
    </template>
  </Dialog>
</template>

<script setup>
import { computed, ref } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
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
