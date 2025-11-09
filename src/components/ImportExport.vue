<template>
  <div class="modal modal-open" @click.self="$emit('close')">
    <div class="modal-box w-full max-w-2xl">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">Import / Export Configuration</h2>
        <button @click="$emit('close')" class="btn btn-ghost btn-sm btn-circle text-primary-content">
          <svg class="size-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div>

      <!-- Tabs -->
      <div role="tablist" class="tabs tabs-border mb-4">
        <button
          role="tab"
          class="tab"
          :class="{ 'tab-active': activeTab === 'export' }"
          @click="activeTab = 'export'"
        >
          Export
        </button>
        <button
          role="tab"
          class="tab"
          :class="{ 'tab-active': activeTab === 'import' }"
          @click="activeTab = 'import'"
        >
          Import
        </button>
      </div>

      <!-- Export Tab -->
      <div v-if="activeTab === 'export'" class="space-y-4">
        <div>
          <label class="label">
            <span class="label-text">Configuration JSON</span>
          </label>
          <textarea
            :value="exportJson"
            readonly
            class="textarea textarea-bordered w-full h-64 font-mono text-xs"
          ></textarea>
        </div>
        <div class="flex gap-2">
          <button @click="copyToClipboard" class="btn btn-primary">
            {{ copyButtonText }}
          </button>
          <button @click="downloadJson" class="btn btn-accent">
            Download File
          </button>
        </div>
      </div>

      <!-- Import Tab -->
      <div v-if="activeTab === 'import'" class="space-y-4">
        <div>
          <label class="label">
            <span class="label-text">Paste Configuration JSON</span>
          </label>
          <textarea
            v-model="importJson"
            placeholder="Paste your configuration JSON here..."
            class="textarea textarea-bordered w-full h-64 font-mono text-xs"
          ></textarea>
        </div>
        <div class="flex gap-2">
          <button @click="loadFromJson" class="btn btn-primary">
            Load Configuration
          </button>
          <label class="btn btn-accent">
            Upload File
            <input
              type="file"
              accept=".json"
              @change="handleFileUpload"
              class="hidden"
            />
          </label>
        </div>
        <div v-if="importError" class="alert alert-error">
          <span>{{ importError }}</span>
        </div>
        <div v-if="importSuccess" class="alert alert-success">
          <span>Configuration loaded successfully!</span>
        </div>
      </div>

        <!-- Close Button -->
        <div class="mt-6 flex justify-end">
          <button @click="$emit('close')" class="btn">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'

const emit = defineEmits(['close'])

const { config, loadConfiguration } = useRackConfig()
const { showSuccess, showError } = useToast()

const activeTab = ref('export')
const importJson = ref('')
const importError = ref('')
const importSuccess = ref(false)
const copyButtonText = ref('Copy to Clipboard')

const exportJson = computed(() => {
  return JSON.stringify(config.value, null, 2)
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(exportJson.value)
    copyButtonText.value = 'Copied!'
    showSuccess('Copied to clipboard', 'Configuration JSON copied successfully')
    setTimeout(() => {
      copyButtonText.value = 'Copy to Clipboard'
    }, 2000)
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Copy failed', 'Failed to copy configuration to clipboard')
  }
}

const downloadJson = () => {
  const blob = new Blob([exportJson.value], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `racker-config-${Date.now()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  showSuccess('Download started', 'Configuration file download initiated')
}

const loadFromJson = () => {
  importError.value = ''
  importSuccess.value = false

  try {
    const parsed = JSON.parse(importJson.value)
    loadConfiguration(parsed)
    importSuccess.value = true
    showSuccess('Configuration imported', 'Your configuration has been loaded successfully')
    setTimeout(() => {
      emit('close')
    }, 1500)
  } catch (error) {
    importError.value = 'Invalid JSON: ' + error.message
    showError('Import failed', error.message)
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    importJson.value = e.target.result
    loadFromJson()
  }
  reader.readAsText(file)
}
</script>