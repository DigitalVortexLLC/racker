<template>
  <div class="modal modal-open" @click.self="$emit('close')">
    <div class="modal-box w-full max-w-md">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">Infrastructure Settings</h2>
        <button @click="$emit('close')" class="btn btn-ghost btn-sm btn-circle text-primary-content">
          <svg class="size-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div>
        <p class="mb-4 text-sm opacity-70">
          Configure infrastructure-level settings. Use the + button to add racks.
        </p>

        <!-- RU per Rack -->
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Default RU per Rack</span>
            <span class="label-text-alt opacity-70">For new racks</span>
          </label>
          <input
            v-model.number="localSettings.ruPerRack"
            type="number"
            min="1"
            max="52"
            class="input input-bordered w-full"
          />
          <label class="label">
            <span class="label-text-alt opacity-70">
              💡 Use the gear icon on each rack to configure individually
            </span>
          </label>
        </div>

        <!-- Resource Providers Note -->
        <div class="alert alert-info mb-6">
          <div>
            <div class="font-bold">💡 Power & Cooling Capacity</div>
            <div class="text-xs mt-2">
              Capacity is now managed through <strong>Resource Providers</strong>.
              Open the Device Manager and go to the "Resource Providers" tab to add PDUs, HVAC units, and other infrastructure that provides capacity to your site.
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex gap-2">
          <button @click="saveSettings" class="btn btn-primary flex-1">
            Save
          </button>
          <button @click="$emit('close')" class="btn flex-1">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'

const emit = defineEmits(['close'])

const { config, updateSettings } = useRackConfig()
const { showSuccess } = useToast()

const localSettings = ref({
  ruPerRack: 42
})

onMounted(() => {
  localSettings.value = {
    ruPerRack: config.value.settings.ruPerRack
  }
})

const saveSettings = () => {
  updateSettings({
    ruPerRack: localSettings.value.ruPerRack
  })

  showSuccess('Settings saved', 'Infrastructure settings have been updated successfully')
  emit('close')
}
</script>
