// @ohos.settings Pure-ABC stub for ArkUI-X/Android
// Provides in-memory key-value store for settings API compatibility.
// Loaded from systemres/abc/settings.abc when dlopen("libsettings_napi.z.so") fails.

var store = {};

function getValueSync(context, name, defValue) {
  if (name in store) {
    return store[name];
  }
  return defValue !== undefined ? defValue : '';
}

function setValueSync(context, name, value) {
  if (!name || typeof name !== 'string' || name.length === 0) {
    return false;
  }
  store[name] = String(value);
  return true;
}

var display = {
  FONT_SCALE: 'FONT_SCALE',
  SCREEN_BRIGHTNESS_STATUS: 'SCREEN_BRIGHTNESS_STATUS',
};

var date = {
  DATE_FORMAT: 'DATE_FORMAT',
  TIME_FORMAT: 'TIME_FORMAT',
};

var domainName = {
  DEVICE_SHARED: 'DEVICE_SHARED',
  USER_PROPERTY: 'USER_PROPERTY',
};

var wireless = {
  WIFI_STATUS: 'WIFI_STATUS',
  BLUETOOTH_STATUS: 'BLUETOOTH_STATUS',
};

var usb = {
  USB_DEVICE_LIST: 'USB_DEVICE_LIST',
};

export default {
  getValueSync: getValueSync,
  setValueSync: setValueSync,
  display: display,
  date: date,
  domainName: domainName,
  wireless: wireless,
  usb: usb,
};
