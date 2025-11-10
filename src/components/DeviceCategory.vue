<template>
  <div class="collapse collapse-arrow bg-base-200 border border-base-300">
    <input
      v-model="isOpen"
      type="checkbox"
    >
    <div class="collapse-title font-medium">
      {{ category.name }}
    </div>
    <div class="collapse-content">
      <DeviceItem
        v-for="device in category.devices"
        :key="device.id"
        :device="device"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DeviceItem from './DeviceItem.vue'

const props = defineProps({
  category: {
    type: Object,
    required: true
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

// Auto-open if there's a search query
const isOpen = ref(props.searchQuery ? true : false)
</script>