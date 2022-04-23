import axios, { AxiosInstance } from 'axios';

export abstract class HttpClient {
  protected readonly instance: AxiosInstance;

  public constructor(baseURL: string) {
    const apiURL = window.__RUNTIME_CONFIG__.API_URL;

    this.instance = axios.create({
      baseURL: `${apiURL}${baseURL}`,
    });
  }
}
