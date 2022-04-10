import { SourceFileStatus, TaskStatus } from './enums';

export type Line = {
  name: string;
  start: Point;
  end: Point;
};

export type Lines = {
  id: number;
  task_id: number;
  lines: Line[];
};

export type Point = {
  x: number;
  y: number;
  displayX?: number;
  displayY?: number;
};

export type Counts = {
  names: string[];
  counts: number[][];
};

export type SourceFile = {
  id: number;
  name: string | undefined;
  path: string;
  status: SourceFileStatus;
  file_exists: boolean;
};

export type SourceFileWithTasks = SourceFile & {
  tasks: Task[];
};

export type Task = {
  id: number;
  source_file_id: number;
  output_path: string;
  status: TaskStatus;
  models: string[];
  parameters: { [id: string]: number };
  lines: Lines[];
};

export type TaskConfiguration = { [id: string]: number | null };
