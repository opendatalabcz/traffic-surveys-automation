import { HttpClient } from './http-client';
import { SourceFile, SourceFileWithTasks, Task } from '../types';

export class SourceFileClient extends HttpClient {
  public constructor() {
    super('http://localhost:8000/source_file');
  }

  public getSourceFiles = () => this.instance.get<SourceFile[]>('').then(response => response.data);

  public discoverSourceFiles = () => this.instance.post<SourceFile[]>('/discover').then(response => response.data);

  public getSourceFile = (sourceFileId: number) =>
    this.instance.get<SourceFileWithTasks>(`${sourceFileId}`).then(response => response.data);

  public createTask = (
    sourceFileId: number,
    detectionModel: string,
    trackingModel: string,
    method: string,
    parameters: { [id: string]: string | number }
  ) =>
    this.instance
      .post<Task>(`${sourceFileId}`, {
        detection_model: detectionModel,
        tracking_model: trackingModel,
        method: method,
        parameters: parameters,
      })
      .then(response => response.data);
}
