<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="Resource Usage Details"
    :style="{ width: '900px' }"
    :closable="true"
  >
    <div class="space-y-4">
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

      <!-- Device List Table -->
      <div class="overflow-auto" style="max-height: 500px;">
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
import { computed } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import { useRackConfig } from '../composables/useRackConfig'
import { useUtilization } from '../composables/useUtilization'
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
  ruPercentage
} = useUtilization()

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
