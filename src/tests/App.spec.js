import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import App from '../App.vue';

// Mock composables
vi.mock('../composables/useDarkMode', () => ({
  useDarkMode: () => ({
    isDark: { value: false },
    toggle: vi.fn(),
  }),
}));

vi.mock('../composables/useRackConfig', () => ({
  useRackConfig: () => ({
    config: { value: {} },
    loadConfiguration: vi.fn(),
  }),
}));

vi.mock('../composables/useDatabase', () => ({
  useDatabase: () => ({
    currentSite: { value: null },
    loadCurrentSite: vi.fn(),
    updateSite: vi.fn(),
    createSite: vi.fn(),
    setCurrentSite: vi.fn(),
    fetchSiteByUuid: vi.fn(),
  }),
}));

vi.mock('../composables/usePasskey', () => ({
  usePasskey: () => ({
    getAuthConfig: vi.fn().mockResolvedValue({
      require_auth: false,
      passkey_supported: false,
    }),
  }),
}));

vi.mock('../composables/useToast', () => ({
  useToast: () => ({
    showToast: vi.fn(),
  }),
}));

describe('App.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the application', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          ToastContainer: true,
          DeviceLibrary: true,
          RackContainer: true,
          UtilizationPanel: true,
          UnrackedDevices: true,
          ConfigMenu: true,
          ImportExport: true,
          DeviceManager: true,
          SaveLoadDialog: true,
          PasskeyAuth: true,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it('displays the app title', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          ToastContainer: true,
          DeviceLibrary: true,
          RackContainer: true,
          UtilizationPanel: true,
          UnrackedDevices: true,
          ConfigMenu: true,
          ImportExport: true,
          DeviceManager: true,
          SaveLoadDialog: true,
          PasskeyAuth: true,
        },
      },
    });

    expect(wrapper.text()).toContain('Racker');
  });
});
