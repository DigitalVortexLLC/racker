<template>
  <div
    class="modal modal-open"
    @click.self="$emit('close')"
  >
    <div class="modal-box">
      <div class="flex items-center justify-between mb-4 -mx-6 -mt-6 px-6 py-4 rounded-t-2xl bg-error">
        <h2 class="text-2xl font-bold text-error-content">Delete Rack</h2>
        <button
          @click="$emit('close')"
          class="btn btn-ghost btn-sm btn-square text-error-content"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div>
        <p class="mb-4">
          Are you sure you want to delete <strong>{{ rack.name }}</strong>?
        </p>

        <div v-if="rack.devices.length > 0" class="mb-6 p-4 rounded bg-base-200">
          <p class="mb-3 font-medium">
            This rack contains {{ rack.devices.length }} device{{ rack.devices.length > 1 ? 's' : '' }}.
          </p>

          <div class="space-y-2">
            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                v-model="deleteOption"
                value="move"
                class="radio radio-primary mr-3"
              />
              <span>Move devices to unracked pane</span>
            </label>

            <label class="flex items-center cursor-pointer">
              <input
                type="radio"
                v-model="deleteOption"
                value="delete"
                class="radio radio-primary mr-3"
              />
              <span>Delete all devices with rack</span>
            </label>
          </div>
        </div>

        <div v-else class="alert mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span>This rack is empty.</span>
        </div>

        <!-- Buttons -->
        <div class="flex gap-2">
          <button
            @click="$emit('close')"
            class="btn flex-1"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="btn btn-error flex-1"
          >
            Delete Rack
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'confirm'])

// Default to moving devices to unracked
const deleteOption = ref('move')

const confirmDelete = () => {
  const moveDevicesToUnracked = deleteOption.value === 'move'
  emit('confirm', moveDevicesToUnracked)
}
</script>
