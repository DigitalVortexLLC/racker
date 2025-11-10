<template>
  <div
    v-if="visible"
    class="modal modal-open"
    @click.self="close"
  >
    <div class="modal-box w-full max-w-xl">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          {{ mode === 'save' ? 'Save Rack Configuration' : 'Load Rack Configuration' }}
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle text-primary-content"
          @click="close"
        >
          <svg
            class="size-6"
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

      <div>
        <!-- Error Display -->
        <div
          v-if="error"
          class="alert alert-error mb-4"
        >
          <span>{{ error }}</span>
          <button
            class="btn btn-ghost btn-sm btn-circle"
            @click="error = null"
          >
            <svg
              class="size-4"
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

        <!-- Site Selection/Creation -->
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Site</span>
          </label>

          <div class="flex gap-2">
            <select
              v-model="selectedSite"
              class="select select-bordered flex-1"
              :disabled="loading"
            >
              <option :value="null">
                Select a site
              </option>
              <option
                v-for="site in sites"
                :key="site.id"
                :value="site"
              >
                {{ site.name }}
              </option>
            </select>

            <button
              class="btn btn-square"
              @click="showNewSiteDialog = true"
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
                  d="M12 4v16m8-8H4"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Save Mode: Rack Name Input -->
        <div
          v-if="mode === 'save'"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Rack Configuration Name</span>
          </label>
          <input
            v-model="rackName"
            type="text"
            placeholder="Enter configuration name (e.g., Production Rack)"
            class="input input-bordered w-full"
          >
        </div>

        <!-- Save Mode: Description -->
        <div
          v-if="mode === 'save'"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Description (Optional)</span>
          </label>
          <textarea
            v-model="description"
            placeholder="Enter description"
            rows="3"
            class="textarea textarea-bordered w-full resize-none"
          />
        </div>

        <!-- Load Mode: Rack Configuration Selection -->
        <div
          v-if="mode === 'load' && selectedSite"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Rack Configuration</span>
          </label>

          <div class="border border-base-300 rounded-lg overflow-hidden">
            <div
              v-if="loadingRacks"
              class="p-4 text-center opacity-70"
            >
              <span class="loading loading-spinner loading-md mr-2" />
              Loading configurations...
            </div>

            <div
              v-else-if="!availableRacks || availableRacks.length === 0"
              class="p-4 text-center opacity-70"
            >
              No saved configurations for this site.
            </div>

            <div
              v-else
              class="divide-y divide-base-300"
            >
              <div
                v-for="rack in availableRacks"
                :key="rack.id"
                class="p-3 cursor-pointer flex justify-between items-start hover:bg-base-200 transition-colors"
                :class="{ 'bg-primary/10': selectedRack?.id === rack.id }"
                @click="selectedRack = rack"
              >
                <div class="flex-1">
                  <div class="font-medium">
                    {{ rack.name }}
                  </div>
                  <div
                    v-if="rack.description"
                    class="text-sm mt-1 opacity-70"
                  >
                    {{ rack.description }}
                  </div>
                  <div class="text-xs mt-1 opacity-70">
                    Updated: {{ formatDate(rack.updated_at) }}
                  </div>
                </div>

                <button
                  class="btn btn-ghost btn-sm btn-square text-error"
                  @click.stop="confirmDelete(rack)"
                >
                  <svg
                    class="size-4"
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
        </div>

        <!-- Buttons -->
        <div class="flex gap-2 mt-6">
          <button
            class="btn flex-1"
            @click="close"
          >
            Cancel
          </button>

          <button
            v-if="mode === 'save'"
            :disabled="!canSave || saving"
            class="btn btn-primary flex-1"
            @click="handleSave"
          >
            <span v-if="saving">
              <span class="loading loading-spinner loading-sm mr-1" />
              Saving...
            </span>
            <span v-else>Save</span>
          </button>

          <button
            v-if="mode === 'load'"
            :disabled="!selectedRack || loading"
            class="btn btn-primary flex-1"
            @click="handleLoad"
          >
            <span v-if="loading">
              <span class="loading loading-spinner loading-sm mr-1" />
              Loading...
            </span>
            <span v-else>Load</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- New Site Dialog -->
  <div
    v-if="showNewSiteDialog"
    class="modal modal-open"
    @click.self="showNewSiteDialog = false"
  >
    <div class="modal-box w-full max-w-md">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          Create New Site
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle text-primary-content"
          @click="showNewSiteDialog = false"
        >
          <svg
            class="size-6"
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

      <div>
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Site Name</span>
          </label>
          <input
            v-model="newSiteName"
            type="text"
            placeholder="Enter site name"
            class="input input-bordered w-full"
          >
        </div>

        <div class="mb-4">
          <label class="label">
            <span class="label-text">Description (Optional)</span>
          </label>
          <textarea
            v-model="newSiteDescription"
            placeholder="Enter description"
            rows="3"
            class="textarea textarea-bordered w-full resize-none"
          />
        </div>

        <div class="flex gap-2 mt-6">
          <button
            class="btn flex-1"
            @click="showNewSiteDialog = false"
          >
            Cancel
          </button>

          <button
            :disabled="!newSiteName?.trim() || creating"
            class="btn btn-primary flex-1"
            @click="handleCreateSite"
          >
            <span v-if="creating">
              <span class="loading loading-spinner loading-sm mr-1" />
              Creating...
            </span>
            <span v-else>Create</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useDatabase } from '../composables/useDatabase';
import { useToast } from '../composables/useToast';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'save', // 'save' or 'load'
    validator: (value) => ['save', 'load'].includes(value)
  },
  currentConfig: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'configLoaded']);

const {
  loading,
  error,
  sites,
  currentSite,
  fetchSites,
  createSite,
  setCurrentSite,
  setCurrentRackName,
  saveRackConfiguration,
  loadRacksBySite,
  loadRackConfiguration,
  deleteRackConfiguration
} = useDatabase();

const { showToast } = useToast();

// Dialog state
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// Site management
const selectedSite = ref(null);
const showNewSiteDialog = ref(false);
const newSiteName = ref('');
const newSiteDescription = ref('');
const creating = ref(false);

// Rack management
const rackName = ref('');
const description = ref('');
const selectedRack = ref(null);
const availableRacks = ref([]);
const loadingRacks = ref(false);
const saving = ref(false);

// Load sites when dialog opens
watch(visible, async (isVisible) => {
  if (isVisible) {
    try {
      await fetchSites();
      // Set current site if available
      if (currentSite.value) {
        selectedSite.value = sites.value.find(s => s.id === currentSite.value.id) || null;
      }
    } catch (err) {
      error.value = 'Failed to load sites';
    }
  } else {
    // Reset form when closing
    resetForm();
  }
});

// Load racks when site is selected
watch(selectedSite, async (site) => {
  if (site && props.mode === 'load') {
    loadingRacks.value = true;
    try {
      availableRacks.value = await loadRacksBySite(site.id);
    } catch (err) {
      error.value = 'Failed to load rack configurations';
    } finally {
      loadingRacks.value = false;
    }
  }
});

// Computed
const canSave = computed(() => {
  return selectedSite.value && rackName.value?.trim().length > 0;
});

// Methods
function resetForm() {
  rackName.value = '';
  description.value = '';
  selectedRack.value = null;
  availableRacks.value = [];
  error.value = null;
}

function close() {
  visible.value = false;
}

async function handleCreateSite() {
  if (!newSiteName.value?.trim()) return;

  creating.value = true;
  error.value = null;

  try {
    const site = await createSite(newSiteName.value.trim(), newSiteDescription.value?.trim() || null);
    selectedSite.value = site;
    setCurrentSite(site);
    showNewSiteDialog.value = false;
    newSiteName.value = '';
    newSiteDescription.value = '';
    showToast('success', 'Site created successfully');
  } catch (err) {
    error.value = err.message;
  } finally {
    creating.value = false;
  }
}

async function handleSave() {
  if (!canSave.value) return;

  saving.value = true;
  error.value = null;

  try {
    await saveRackConfiguration(
      selectedSite.value.id,
      rackName.value.trim(),
      props.currentConfig,
      description.value?.trim() || null
    );

    setCurrentSite(selectedSite.value);
    setCurrentRackName(rackName.value.trim()); // Set rack name for auto-save
    showToast('success', `Rack configuration "${rackName.value}" saved successfully`);
    close();
  } catch (err) {
    error.value = err.message;
  } finally {
    saving.value = false;
  }
}

async function handleLoad() {
  if (!selectedRack.value) return;

  try {
    const rack = await loadRackConfiguration(selectedSite.value.id, selectedRack.value.name);

    if (rack && rack.config_data) {
      setCurrentSite(selectedSite.value);
      setCurrentRackName(rack.name); // Set rack name for auto-save
      emit('configLoaded', rack.config_data);
      showToast('success', `Loaded "${rack.name}"`);
      close();
    }
  } catch (err) {
    error.value = err.message;
  }
}

async function confirmDelete(rack) {
  if (!confirm(`Are you sure you want to delete "${rack.name}"?`)) {
    return;
  }

  try {
    await deleteRackConfiguration(rack.id);
    availableRacks.value = availableRacks.value.filter(r => r.id !== rack.id);
    showToast('success', 'Configuration deleted');
  } catch (err) {
    error.value = err.message;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString();
}
</script>

<style scoped>
/* Divide-y utility for borders between rack items */
.divide-y > * + * {
  border-top-width: 1px;
  border-color: var(--border-color);
}
</style>
