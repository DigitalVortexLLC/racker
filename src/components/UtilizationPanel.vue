<template>
  <div
    class="card bg-base-200 shadow-2xl absolute top-4 right-4 z-10 transition-all duration-300 border border-base-300"
    :class="isExpanded ? 'w-80' : 'w-auto'"
  >
    <!-- Header with Toggle -->
    <div
      class="card-body p-4 cursor-pointer hover:bg-base-300/50 rounded-t-lg transition-colors"
      @click="isExpanded = !isExpanded"
    >
      <div class="flex items-center justify-between">
        <h3 class="card-title text-base font-semibold">
          {{ isExpanded ? 'Resource Utilization' : 'Resources' }}
        </h3>
        <button class="btn btn-ghost btn-xs btn-circle">
          <svg
            class="size-5 transition-transform duration-300"
            :class="{ 'rotate-180': isExpanded }"
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
    </div>

    <!-- Expandable Content -->
    <div
      v-show="isExpanded"
      class="px-4 pb-4 border-t border-base-300"
    >
      <!-- Power Utilization -->
      <div class="mb-4">
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium">Power</span>
          <span class="text-sm opacity-70">{{ powerUsed }}W / {{ powerCapacity }}W</span>
        </div>
        <progress
          class="progress"
          :class="powerBarColor"
          :value="powerPercentage"
          max="100"
        />
        <div class="text-xs mt-1 opacity-70">
          {{ powerPercentage }}%
        </div>
      </div>

      <!-- Power Ports Utilization -->
      <div
        v-if="powerPortsCapacity > 0"
        class="mb-4"
      >
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium">Power Ports</span>
          <span class="text-sm opacity-70">{{ powerPortsUsed }} / {{ powerPortsCapacity }} ports</span>
        </div>
        <progress
          class="progress"
          :class="powerPortsBarColor"
          :value="powerPortsPercentage"
          max="100"
        />
        <div class="text-xs mt-1 opacity-70">
          {{ powerPortsPercentage }}%
        </div>
      </div>

      <!-- HVAC Utilization -->
      <div class="mb-4">
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium">HVAC</span>
          <span class="text-sm opacity-70">{{ hvacLoadTons }} / {{ hvacCapacityTons }} Tons</span>
        </div>
        <progress
          class="progress"
          :class="hvacBarColor"
          :value="hvacPercentage"
          max="100"
        />
        <div class="text-xs mt-1 opacity-70">
          {{ hvacPercentage }}%
        </div>
      </div>

      <!-- RU Utilization -->
      <div>
        <div class="flex justify-between items-center mb-1">
          <span class="text-sm font-medium">Rack Units</span>
          <span class="text-sm opacity-70">{{ ruUsed }}U / {{ ruCapacity }}U</span>
        </div>
        <progress
          class="progress"
          :class="ruBarColor"
          :value="ruPercentage"
          max="100"
        />
        <div class="text-xs mt-1 opacity-70">
          {{ ruPercentage }}%
        </div>
      </div>

      <!-- Details Button -->
      <div class="mt-4">
        <button
          class="btn btn-block btn-sm"
          @click.stop="showDetailModal = true"
        >
          View Details
        </button>
      </div>
    </div>

    <!-- Compact View (when collapsed) -->
    <div
      v-show="!isExpanded"
      class="px-4 pb-4 flex flex-col gap-3"
    >
      <!-- Power Compact -->
      <div
        class="tooltip tooltip-left"
        data-tip="Power"
      >
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5">
            <svg
              class="size-5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                clip-rule="evenodd"
              />
            </svg>
            <div
              class="size-2 rounded-full"
              :class="powerBarColor"
            />
          </div>
          <span class="text-sm font-medium">{{ powerPercentage }}%</span>
        </div>
      </div>

      <!-- Power Ports Compact -->
      <div
        v-if="powerPortsCapacity > 0"
        class="tooltip tooltip-left"
        data-tip="Power Ports"
      >
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5">
            <svg
              class="size-5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                clip-rule="evenodd"
              />
            </svg>
            <div
              class="size-2 rounded-full"
              :class="powerPortsBarColor"
            />
          </div>
          <span class="text-sm font-medium">{{ powerPortsPercentage }}%</span>
        </div>
      </div>

      <!-- HVAC Compact -->
      <div
        class="tooltip tooltip-left"
        data-tip="HVAC"
      >
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5">
            <svg
              class="size-5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V9a1 1 0 11-2 0V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1zm-5 8.274l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L5 10.274zm10 0l-.818 2.552c.25.112.526.174.818.174.292 0 .569-.062.818-.174L15 10.274z"
                clip-rule="evenodd"
              />
            </svg>
            <div
              class="size-2 rounded-full"
              :class="hvacBarColor"
            />
          </div>
          <span class="text-sm font-medium">{{ hvacPercentage }}%</span>
        </div>
      </div>

      <!-- RU Compact -->
      <div
        class="tooltip tooltip-left"
        data-tip="Rack Units"
      >
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5">
            <svg
              class="size-5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zM3 16a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2z" />
            </svg>
            <div
              class="size-2 rounded-full"
              :class="ruBarColor"
            />
          </div>
          <span class="text-sm font-medium">{{ ruPercentage }}%</span>
        </div>
      </div>
    </div>

    <!-- Resource Detail Modal -->
    <ResourceDetailModal v-model="showDetailModal" />
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useUtilization } from '../composables/useUtilization'
import { btuToTons } from '../utils/calculations'
import ResourceDetailModal from './ResourceDetailModal.vue'

const isExpanded = ref(false)
const showDetailModal = ref(false)
const unrackedPanelExpanded = inject('unrackedPanelExpanded', ref(true))

const unrackedPanelOffset = computed(() => {
  const baseOffset = 16 // 1rem in pixels (right-4)
  const panelWidth = unrackedPanelExpanded.value ? 320 : 64
  return `${baseOffset + panelWidth}px`
})

const {
  powerUsed,
  powerCapacity,
  powerPercentage,
  powerPortsUsed,
  powerPortsCapacity,
  powerPortsPercentage,
  hvacLoad,
  hvacCapacity,
  hvacPercentage,
  ruUsed,
  ruCapacity,
  ruPercentage
} = useUtilization()

// Convert BTU/hr to Refrigeration Tons for display
const hvacLoadTons = computed(() => btuToTons(hvacLoad.value).toFixed(1))
const hvacCapacityTons = computed(() => btuToTons(hvacCapacity.value).toFixed(1))

const getBarColor = (percentage) => {
  if (percentage < 70) return 'progress-success'
  if (percentage < 90) return 'progress-warning'
  return 'progress-error'
}

const powerBarColor = computed(() => getBarColor(powerPercentage.value))
const powerPortsBarColor = computed(() => getBarColor(powerPortsPercentage.value))
const hvacBarColor = computed(() => getBarColor(hvacPercentage.value))
const ruBarColor = computed(() => getBarColor(ruPercentage.value))
</script>