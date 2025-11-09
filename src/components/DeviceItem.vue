<template>
  <div
    :draggable="true"
    @dragstart="handleDragStart"
    class="p-3 cursor-move transition-colors last:border-b-0"
    style="border-bottom: 1px solid var(--border-color);"
    @mouseover="$event.target.style.backgroundColor = 'var(--bg-secondary)'"
    @mouseout="$event.target.style.backgroundColor = 'transparent'"
  >
    <div class="flex items-center gap-3">
      <!-- Color indicator -->
      <div
        :style="{ backgroundColor: device.color }"
        class="w-4 h-4 rounded flex-shrink-0"
      ></div>

      <!-- Device info -->
      <div class="flex-1 min-w-0">
        <div class="font-medium text-sm truncate flex items-center gap-2" style="color: var(--text-primary);">
          {{ device.name }}
          <span
            v-if="device.custom"
            class="text-xs px-1.5 py-0.5 rounded"
            style="background-color: rgba(74, 144, 226, 0.2); color: var(--color-primary);"
            title="Custom device"
          >
            Custom
          </span>
        </div>
        <div class="text-xs" style="color: var(--text-secondary);">
          {{ device.ruSize }}U • {{ device.powerDraw }}W
        </div>
      </div>
    </div>

    <!-- Tooltip on hover -->
    <div v-if="showTooltip" class="text-xs mt-2" style="color: var(--text-secondary);">
      {{ device.description }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useDragDrop } from '../composables/useDragDrop'

const props = defineProps({
  device: {
    type: Object,
    required: true
  }
})

const showTooltip = ref(false)
const { startDrag } = useDragDrop()

const handleDragStart = (event) => {
  startDrag(event, props.device)
}
</script>