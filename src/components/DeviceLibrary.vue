<template>
  <aside class="shadow-lg overflow-y-auto transition-colors border-r" style="background-color: var(--bg-primary); border-color: var(--border-color);">
    <div class="px-6 flex items-center" style="background-color: var(--color-primary-dark); min-height: 68px;">
      <h2 class="text-2xl font-bold leading-none" style="color: #0c0c0d;">Library</h2>
    </div>

    <!-- Tabs -->
    <div class="flex border-b" style="border-color: var(--border-color);">
      <button
        class="flex-1 px-4 py-3 text-sm font-medium transition-colors"
        :style="{
          color: activeTab === 'devices' ? 'var(--color-primary)' : 'var(--text-secondary)',
          borderBottom: activeTab === 'devices' ? '2px solid var(--color-primary)' : '2px solid transparent',
          backgroundColor: activeTab === 'devices' ? 'var(--bg-secondary)' : 'transparent'
        }"
        @click="activeTab = 'devices'"
      >
        Devices
      </button>
      <button
        class="flex-1 px-4 py-3 text-sm font-medium transition-colors"
        :style="{
          color: activeTab === 'providers' ? 'var(--color-primary)' : 'var(--text-secondary)',
          borderBottom: activeTab === 'providers' ? '2px solid var(--color-primary)' : '2px solid transparent',
          backgroundColor: activeTab === 'providers' ? 'var(--bg-secondary)' : 'transparent'
        }"
        @click="activeTab = 'providers'"
      >
        Providers
      </button>
    </div>

    <!-- Devices Tab Content -->
    <div v-show="activeTab === 'devices'" class="p-4">
      <!-- Search bar -->
      <input
        v-model="deviceSearchQuery"
        type="text"
        placeholder="Search devices..."
        class="w-full px-3 py-2 rounded mb-4 focus:outline-none transition-colors"
        style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
        @focus="$event.target.style.borderColor = 'var(--color-primary)'"
        @blur="$event.target.style.borderColor = 'var(--border-color)'"
      />

      <!-- Device Categories -->
      <div v-for="category in filteredCategories" :key="category.id" class="mb-2">
        <DeviceCategory :category="category" :search-query="deviceSearchQuery" />
      </div>

      <div v-if="filteredCategories.length === 0" class="text-center py-8" style="color: var(--text-secondary);">
        No devices found
      </div>
    </div>

    <!-- Resource Providers Tab Content -->
    <div v-show="activeTab === 'providers'" class="p-4">
      <!-- Search bar -->
      <input
        v-model="providerSearchQuery"
        type="text"
        placeholder="Search providers..."
        class="w-full px-3 py-2 rounded mb-4 focus:outline-none transition-colors"
        style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
        @focus="$event.target.style.borderColor = 'var(--color-primary)'"
        @blur="$event.target.style.borderColor = 'var(--border-color)'"
      />

      <!-- No providers message -->
      <div v-if="resourceProviders.length === 0" class="text-center py-8">
        <p class="text-sm mb-2" style="color: var(--text-secondary);">
          No resource providers configured
        </p>
        <p class="text-xs" style="color: var(--text-secondary);">
          Add providers in Device Manager
        </p>
      </div>

      <!-- Provider Groups by Type -->
      <div v-for="providerGroup in filteredProviderGroups" :key="providerGroup.type" class="mb-4">
        <h3 class="text-sm font-semibold mb-2 px-2" style="color: var(--text-primary);">
          {{ providerGroup.name }}
        </h3>
        
        <div
          v-for="provider in providerGroup.providers"
          :key="provider.id"
          class="p-3 rounded border transition-colors mb-2 cursor-grab active:cursor-grabbing"
          style="background-color: var(--bg-secondary); border-color: var(--border-color);"
          draggable="true"
          @dragstart="handleDragStart($event, provider)"
          @dragend="handleDragEnd"
          @mouseover="$event.currentTarget.style.borderColor = 'var(--color-primary)'"
          @mouseout="$event.currentTarget.style.borderColor = 'var(--border-color)'"
        >
          <div class="flex items-start gap-3">
            <!-- Icon -->
            <div class="flex-shrink-0 mt-0.5">
              <svg v-if="provider.type === 'power'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="provider.type === 'cooling'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="provider.type === 'network'" class="w-5 h-5" style="color: var(--color-primary);" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
              </svg>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate" style="color: var(--text-primary);">
                {{ provider.name }}
              </div>
              <div class="text-xs" style="color: var(--text-secondary);">
                <span v-if="provider.powerCapacity > 0">{{ provider.powerCapacity.toLocaleString() }}W</span>
                <span v-if="provider.coolingCapacity > 0">{{ (provider.coolingCapacity / 12000).toFixed(1) }} Tons</span>
                <span v-if="provider.networkCapacity > 0">{{ provider.networkCapacity }} Gbps</span>
              </div>
              <div v-if="provider.location" class="text-xs mt-1 truncate" style="color: var(--text-secondary);">
                📍 {{ provider.location }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary -->
      <div
        v-if="resourceProviders.length > 0"
        class="mt-6 pt-4 border-t"
        style="border-color: var(--border-color);"
      >
        <div class="text-sm font-medium mb-3" style="color: var(--text-primary);">
          Total Capacity
        </div>
        <div class="space-y-2 text-xs" style="color: var(--text-secondary);">
          <div v-if="totalPowerCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            <span>{{ totalPowerCapacity.toLocaleString() }}W</span>
          </div>
          <div v-if="totalCoolingCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z" clip-rule="evenodd" />
            </svg>
            <span>{{ (totalCoolingCapacity / 12000).toFixed(1) }} Tons</span>
          </div>
          <div v-if="totalNetworkCapacity > 0" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
            <span>{{ totalNetworkCapacity }} Gbps</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDevices } from '../composables/useDevices'
import { useResourceProviders } from '../composables/useResourceProviders'
import DeviceCategory from './DeviceCategory.vue'

const activeTab = ref('devices')
const deviceSearchQuery = ref('')
const providerSearchQuery = ref('')

// Devices
const { categories } = useDevices()

const filteredCategories = computed(() => {
  if (!deviceSearchQuery.value) return categories.value

  return categories.value
    .map(category => ({
      ...category,
      devices: category.devices.filter(device =>
        device.name.toLowerCase().includes(deviceSearchQuery.value.toLowerCase()) ||
        device.description.toLowerCase().includes(deviceSearchQuery.value.toLowerCase())
      )
    }))
    .filter(category => category.devices.length > 0)
})

// Resource Providers
const {
  resourceProviders,
  totalPowerCapacity,
  totalCoolingCapacity,
  totalNetworkCapacity
} = useResourceProviders()

const filteredProviderGroups = computed(() => {
  const groups = [
    {
      type: 'power',
      name: 'Power Providers',
      providers: resourceProviders.value.filter(p => p.type === 'power')
    },
    {
      type: 'cooling',
      name: 'Cooling Providers',
      providers: resourceProviders.value.filter(p => p.type === 'cooling')
    },
    {
      type: 'network',
      name: 'Network Providers',
      providers: resourceProviders.value.filter(p => p.type === 'network')
    }
  ].filter(group => group.providers.length > 0)

  if (!providerSearchQuery.value) return groups

  const query = providerSearchQuery.value.toLowerCase()
  return groups
    .map(group => ({
      ...group,
      providers: group.providers.filter(provider =>
        provider.name.toLowerCase().includes(query) ||
        (provider.location && provider.location.toLowerCase().includes(query)) ||
        (provider.description && provider.description.toLowerCase().includes(query))
      )
    }))
    .filter(group => group.providers.length > 0)
})

// Drag and drop handlers for providers
const handleDragStart = (event, provider) => {
  event.dataTransfer.effectAllowed = 'copy'
  event.dataTransfer.setData('text/plain', JSON.stringify({
    type: 'resource-provider',
    provider: provider
  }))
  event.target.style.opacity = '0.5'
}

const handleDragEnd = (event) => {
  event.target.style.opacity = '1'
}
</script>