import { HttpClient } from './http-client';
import { SourceFile, SourceFileWithTasks, Task } from '../types';

export class SourceFileClient extends HttpClient {
  public constructor() {
    super('/source_file');
  }

  public getSourceFiles = () => this.instance.get<SourceFile[]>('').then(response => response.data);

  public discoverSourceFiles = () => this.instance.post<SourceFile[]>('/discover').then(response => response.data);

  public getSourceFile = (sourceFileId: number) =>
    this.instance.get<SourceFileWithTasks>(`${sourceFileId}`).then(response => response.data);

  public createTask = (
    sourceFileId: number,
    name: string,
    detectionModel: string,
    trackingModel: string,
    parameters: { [id: string]: string | number }
  ) =>
    this.instance
      .post<Task>(`${sourceFileId}`, {
        name: name,
        detection_model: detectionModel,
        tracking_model: trackingModel,
        parameters: parameters,
      })
      .then(response => response.data);
}
