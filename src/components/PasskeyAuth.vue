<template>
  <div
    v-if="visible"
    class="modal modal-open"
    @click.self="close"
  >
    <div class="modal-box w-full max-w-md">
      <div class="flex items-center justify-between mb-6 p-6 -mt-6 -mx-6 rounded-t-xl bg-primary">
        <h2 class="text-2xl font-bold text-primary-content">
          {{ isRegistering ? 'Register Passkey' : 'Login with Passkey' }}
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
        <!-- Current User Display -->
        <div
          v-if="currentUser"
          class="alert alert-success mb-4"
        >
          <div class="flex items-center justify-between w-full">
            <div>
              <div class="font-medium">
                Welcome, {{ currentUser.username }}!
              </div>
              <div class="text-sm opacity-70">
                {{ currentUser.email }}
              </div>
            </div>
            <button
              class="btn btn-accent btn-sm"
              @click="handleLogout"
            >
              Logout
            </button>
          </div>
        </div>

        <!-- Error Display -->
        <div
          v-if="error"
          class="alert alert-error mb-4"
        >
          <span>{{ error }}</span>
        </div>

        <!-- Passkey not supported warning -->
        <div
          v-if="!passkeySupported"
          class="alert alert-warning mb-4"
        >
          <span>Passkeys are not supported on this device or browser. Please use a modern browser with WebAuthn support.</span>
        </div>

        <!-- Username Input (for registration or username-based login) -->
        <div
          v-if="!currentUser"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Username</span>
          </label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            class="input input-bordered w-full"
            @keyup.enter="isRegistering ? handleRegister() : handleLogin()"
          >
        </div>

        <!-- Passkey Name Input (for registration only) -->
        <div
          v-if="!currentUser && isRegistering"
          class="mb-4"
        >
          <label class="label">
            <span class="label-text">Passkey Name (Optional)</span>
          </label>
          <input
            v-model="passkeyName"
            type="text"
            placeholder="e.g., My MacBook, iPhone, etc."
            class="input input-bordered w-full"
          >
        </div>

        <!-- Info Text -->
        <div
          v-if="!currentUser"
          class="mb-6 text-sm opacity-70"
        >
          {{ isRegistering 
            ? 'Create a new passkey for passwordless authentication. You\'ll use your device\'s biometric sensor or PIN.' 
            : 'Use your passkey to sign in securely without a password.' 
          }}
        </div>

        <!-- Action Buttons -->
        <div
          v-if="!currentUser"
          class="flex flex-col gap-3"
        >
          <button
            v-if="isRegistering"
            :disabled="!username.trim() || loading || !passkeySupported"
            class="btn btn-primary w-full"
            @click="handleRegister"
          >
            <span v-if="loading">
              <span class="loading loading-spinner loading-sm mr-2" />
              Creating Passkey...
            </span>
            <span v-else>Create Passkey</span>
          </button>

          <button
            v-else
            :disabled="loading || !passkeySupported"
            class="btn btn-primary w-full"
            @click="handleLogin"
          >
            <span v-if="loading">
              <span class="loading loading-spinner loading-sm mr-2" />
              Authenticating...
            </span>
            <span v-else>Sign In with Passkey</span>
          </button>

          <!-- Toggle between login and register -->
          <div class="text-center text-sm opacity-70">
            {{ isRegistering ? 'Already have a passkey?' : 'Need to create a passkey?' }}
            <button
              class="link link-primary font-medium ml-1"
              @click="isRegistering = !isRegistering; error = null"
            >
              {{ isRegistering ? 'Sign In' : 'Register' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { usePasskey } from '../composables/usePasskey';
import { useToast } from '../composables/useToast';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'authenticated']);

const { loading, error, currentUser, isSupported, register, login, getCurrentUser, logout } = usePasskey();
const { showToast } = useToast();

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const username = ref('');
const passkeyName = ref('');
const isRegistering = ref(false);
const passkeySupported = ref(false);

onMounted(async () => {
  passkeySupported.value = isSupported();
  await getCurrentUser();
});

watch(visible, (isVisible) => {
  if (!isVisible) {
    username.value = '';
    passkeyName.value = '';
    error.value = null;
  }
});

function close() {
  visible.value = false;
}

async function handleRegister() {
  if (!username.value.trim()) return;

  try {
    await register(username.value.trim(), passkeyName.value.trim() || 'My Passkey');
    showToast('success', 'Passkey created successfully!');
    emit('authenticated', currentUser.value);
    close();
  } catch (err) {
    // Error already set in composable
    showToast('error', 'Failed to create passkey');
  }
}

async function handleLogin() {
  try {
    await login(username.value.trim() || null);
    showToast('success', 'Signed in successfully!');
    emit('authenticated', currentUser.value);
    close();
  } catch (err) {
    // Error already set in composable
    showToast('error', 'Failed to sign in');
  }
}

async function handleLogout() {
  await logout();
  showToast('success', 'Logged out successfully');
  close();
}
</script>
