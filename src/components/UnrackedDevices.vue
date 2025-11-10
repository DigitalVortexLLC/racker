<template>
  <aside
    class="shadow-lg transition-all duration-300 flex flex-col bg-base-100 border-t border-base-300"
    :class="[isExpanded ? 'h-64' : 'h-16', { 'drop-zone-active': isDragOver }]"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <!-- Header with Toggle -->
    <div
      class="px-6 border-b border-base-300 transition-colors relative flex items-center bg-primary h-16"
      :class="{ 'cursor-pointer hover:opacity-90': isExpanded }"
      @click="isExpanded ? isExpanded = false : null"
    >
      <div
        v-if="isExpanded"
        class="flex items-center justify-between w-full"
      >
        <div class="flex items-center gap-4">
          <h2 class="text-xl font-bold text-primary-content">
            Unracked Devices
          </h2>
          <p class="text-sm text-primary-content/70">
            {{ unrackedDevices.length }} device{{ unrackedDevices.length !== 1 ? 's' : '' }}
          </p>
        </div>
        <button class="btn btn-ghost btn-sm btn-square text-primary-content/70 hover:text-primary-content">
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
      </div>

      <!-- Collapsed View - Just Icon and Count -->
      <div
        v-else
        class="flex items-center justify-between w-full"
      >
        <div class="flex items-center gap-3">
          <svg
            class="w-6 h-6 text-primary-content"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
            />
          </svg>
          <span class="text-primary-content font-semibold">Unracked Devices</span>
          <span
            v-if="unrackedDevices.length > 0"
            class="badge badge-error text-xs font-bold"
          >
            {{ unrackedDevices.length }}
          </span>
        </div>
        <button 
          class="btn btn-ghost btn-sm btn-square text-primary-content/70 hover:text-primary-content"
          @click.stop="isExpanded = true"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 15l7-7 7 7"
            />
          </svg>
        </button>
      </div>
    </div>

    <div
      v-show="isExpanded"
      class="p-4 flex-1 overflow-y-auto overflow-x-auto"
    >
      <div
        v-if="unrackedDevices.length === 0"
        class="text-center py-8 text-base-content/60"
      >
        <svg
          class="w-12 h-12 mx-auto mb-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 13l4 4L19 7"
          />
        </svg>
        <p class="text-sm">
          All devices racked
        </p>
      </div>

      <div
        v-else
        class="flex gap-2 flex-wrap"
      >
        <div
          v-for="device in unrackedDevices"
          :key="device.instanceId"
          :draggable="true"
          class="p-3 rounded cursor-move transition-colors border border-base-300 bg-primary/10 hover:bg-primary/20 flex items-center gap-3 min-w-[200px]"
          @dragstart="handleDragStart($event, device)"
        >
          <div class="flex items-center gap-3">
            <!-- Color indicator -->
            <div
              :style="{ backgroundColor: device.color }"
              class="w-4 h-4 rounded flex-shrink-0"
            />

            <!-- Device info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">
                {{ device.customName || device.name }}
              </div>
              <div class="text-xs text-base-content/60">
                {{ device.ruSize }}U • {{ device.powerDraw }}W
              </div>
            </div>

            <!-- Remove button -->
            <button
              class="btn btn-ghost btn-xs btn-square text-error hover:text-error flex-shrink-0"
              title="Remove device"
              @click="removeDevice(device.instanceId)"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Helper text -->
      <div
        v-if="unrackedDevices.length > 0"
        class="alert alert-info mt-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          class="stroke-current shrink-0 w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span class="text-xs">Drag devices from here into racks to assign them positions.</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useDragDrop } from '../composables/useDragDrop'
import { useToast } from '../composables/useToast'

const isExpanded = ref(false)
const isDragOver = ref(false)
const unrackedPanelExpanded = inject('unrackedPanelExpanded', ref(true))

// Sync with parent
watch(isExpanded, (newValue) => {
  unrackedPanelExpanded.value = newValue
})

const { unrackedDevices, removeUnrackedDevice } = useRackConfig()
const { startDrag, handleDropToUnracked, dragSource } = useDragDrop()
const { showSuccess, showInfo } = useToast()

const handleDragStart = (event, device) => {
  startDrag(event, device, { type: 'unracked' })
}

const handleDragOver = (event) => {
  // Only show drop zone if dragging from a rack
  if (dragSource.value?.type === 'rack') {
    isDragOver.value = true
  }
}

const handleDragLeave = (event) => {
  isDragOver.value = false
}

const handleDrop = (event) => {
  isDragOver.value = false
  handleDropToUnracked(event)
}

const removeDevice = (instanceId) => {
  const device = unrackedDevices.value.find(d => d.instanceId === instanceId)
  if (confirm('Remove this device permanently?')) {
    removeUnrackedDevice(instanceId)
    showSuccess('Device removed', `${device?.customName || device?.name || 'Device'} has been removed`)
  }
}
</script>

<style scoped>
.drop-zone-active {
  box-shadow: inset 0 0 0 3px oklch(var(--p));
  transition: box-shadow 0.2s ease;
}
</style>