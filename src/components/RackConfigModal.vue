<template>
  <div
    class="modal modal-open"
    @click.self="$emit('close')"
  >
    <div class="modal-box max-w-md">
      <!-- Header -->
      <div class="flex items-center gap-3 mb-4">
        <svg
          class="size-8 text-primary flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        <div class="flex-1">
          <h3 class="font-bold text-xl">
            Configure {{ rack.name }}
          </h3>
          <p class="text-sm opacity-70">
            Adjust rack specifications
          </p>
        </div>
        <button
          class="btn btn-sm btn-circle btn-ghost"
          type="button"
          @click="$emit('close')"
        >
          <svg
            class="size-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div class="divider my-2" />

      <!-- RU Size Setting -->
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text font-semibold">Rack Units (RU)</span>
          <span class="label-text-alt opacity-70">1U = 1.75"</span>
        </label>
        <input
          v-model.number="localRuSize"
          type="number"
          min="1"
          max="52"
          class="input input-bordered input-lg w-full"
          :class="{ 'input-error': hasDevices && localRuSize < maxUsedRU }"
          placeholder="42"
        >
        <label class="label">
          <span class="label-text-alt">
            <span
              v-if="hasDevices && localRuSize < maxUsedRU"
              class="text-error font-semibold"
            >
              ⚠️ Devices extend to RU {{ maxUsedRU }}
            </span>
            <span
              v-else
              class="opacity-70"
            >
              Standard: 42U, 45U, 48U, 52U
            </span>
          </span>
        </label>
      </div>

      <!-- Current Usage Info -->
      <div
        v-if="hasDevices"
        class="alert alert-info"
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
        <div class="text-sm">
          <div class="font-semibold">
            Current Usage
          </div>
          <div>{{ rack.devices.length }} device{{ rack.devices.length !== 1 ? 's' : '' }} • Highest RU: {{ maxUsedRU }}</div>
        </div>
      </div>

      <div class="modal-action">
        <button
          class="btn"
          type="button"
          @click="$emit('close')"
        >
          Cancel
        </button>
        <button 
          class="btn btn-primary" 
          :disabled="!canSave"
          type="button"
          @click="saveConfig"
        >
          Save Changes
        </button>
      </div>
    </div>
  </div>
</template><script setup>
import { ref, computed, onMounted } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'

const props = defineProps({
  rack: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const { config, updateRack } = useRackConfig()
const { showSuccess, showWarning } = useToast()

const localRuSize = ref(42)

const hasDevices = computed(() => props.rack.devices && props.rack.devices.length > 0)

const maxUsedRU = computed(() => {
  if (!hasDevices.value) return 0
  
  return Math.max(...props.rack.devices.map(device => {
    return device.position + device.ruSize - 1
  }))
})

const canSave = computed(() => {
  // Must have a valid RU size
  if (!localRuSize.value || localRuSize.value < 1 || localRuSize.value > 52) {
    return false
  }
  
  // If there are devices, RU size must accommodate them
  if (hasDevices.value && localRuSize.value < maxUsedRU.value) {
    return false
  }
  
  return true
})

onMounted(() => {
  // Use rack-specific RU size if available, otherwise use global default
  localRuSize.value = props.rack.ruSize || config.value.settings.ruPerRack || 42
})

const saveConfig = () => {
  if (!canSave.value) {
    showWarning('Invalid Configuration', `Rack size must be at least ${maxUsedRU.value}U to accommodate existing devices`)
    return
  }

  updateRack(props.rack.id, { ruSize: localRuSize.value })
  showSuccess('Rack Updated', `${props.rack.name} configured with ${localRuSize.value}U`)
  emit('close')
}
</script>
