export {};

declare global {
  // eslint-disable-next-line @typescript-eslint/consistent-type-definitions
  interface Window {
    __RUNTIME_CONFIG__: {
      API_URL: string;
    };
  }
}
