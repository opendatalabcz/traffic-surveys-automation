export enum OutputType {
  file = 'file',
  video = 'video',
}

export enum DetectionModel {
  efficientdet_d6 = 'efficientdet_d6',
  efficientdet_d5_adv_prop = 'efficientdet_d5_adv_prop',
}

export enum SourceFileStatus {
  new = 'new',
  processing = 'processing',
  processed = 'processed',
  deleted = 'deleted',
}

export enum TrackingModel {
  simple_sort = 'simple_sort',
  deep_sort = 'deep_sort',
}

export enum TaskStatus {
  created = 'created',
  processing = 'processing',
  completed = 'completed',
  failed = 'failed',
}
