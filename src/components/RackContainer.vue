<template>
  <div class="rack-container">
    <div class="flex gap-6 overflow-x-auto pb-4">
      <Rack
        v-for="(rack, index) in racks"
        :key="rack.id"
        :rack="rack"
        :index="index"
        @reorder="handleReorder"
        @configure="handleConfigure"
      />

      <!-- Add Rack Button -->
      <button
        @click="handleAddRack"
        class="card shadow-lg p-4 flex-shrink-0 w-[250px] border-2 border-dashed border-base-300 bg-base-200 hover:border-primary hover:bg-base-300 transition-all duration-200 flex items-center justify-center"
        title="Add new rack"
      >
        <svg class="w-12 h-12 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>

    <div v-if="racks.length === 0" class="text-center py-20 text-base-content/60">
      <p class="text-xl mb-2">No racks configured</p>
      <p class="text-sm">Click the + button to add your first rack</p>
    </div>

    <!-- Rack Config Modal -->
    <RackConfigModal
      v-if="configRack"
      :rack="configRack"
      @close="configRack = null"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRackConfig } from '../composables/useRackConfig'
import { useToast } from '../composables/useToast'
import { useDatabase } from '../composables/useDatabase'
import Rack from './Rack.vue'
import RackConfigModal from './RackConfigModal.vue'

const { racks, addRack, reorderRacks } = useRackConfig()
const { showSuccess } = useToast()
const { currentSite } = useDatabase()

const configRack = ref(null)

const handleAddRack = () => {
  const newRack = addRack()
  showSuccess('Rack Added', `${newRack.name} has been created`)
}

const handleReorder = (fromIndex, toIndex) => {
  reorderRacks(fromIndex, toIndex)
  showSuccess('Racks Reordered', 'Rack order updated')
}

const handleConfigure = (rack) => {
  configRack.value = rack
}
</script>
