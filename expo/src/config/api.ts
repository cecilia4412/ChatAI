import Constants from 'expo-constants';

const getApiUrl = () => {
  if (__DEV__) {
    const debuggerHost = Constants.expoConfig?.hostUri;
    if (debuggerHost) {
      const host = debuggerHost.split(':')[0];
      return `http://${host}:8000`;
    }
    return 'http://10.65.165.87:8000';
  }
  return 'https://your-production-api.com';
};

export const API_CONFIG = {
  BASE_URL: getApiUrl(),
};
