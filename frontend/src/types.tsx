export type Task = {
  id: number;
  source_file_id: number;
  output_method: string;
  output_path: string;
  status: string;
  models: string[];
  parameters: { [id: string]: string | number };
};

export type SourceFile = {
  id: number;
  name: string | undefined;
  path: string;
  status: string;
  file_exists: boolean;
};

export type SourceFileWithTasks = SourceFile & {
  tasks: Task[];
};
