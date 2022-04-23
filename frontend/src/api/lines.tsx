import { HttpClient } from './http-client';
import { Counts } from '../types';

export class LinesClient extends HttpClient {
  public constructor() {
    super('/lines');
  }

  public getCounts = (linesId: number) => this.instance.get<Counts>(`${linesId}`).then(response => response.data);

  public delete = (linesId: number) => this.instance.delete(`${linesId}`).then(response => response.data);
}
