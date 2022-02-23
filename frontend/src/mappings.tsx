import { DetectionModel, TrackingModel } from './enums';

export const DetectionModelMapping = {
  [DetectionModel.efficientdet_d6.toString()]: 'EfficientDet D6',
  [DetectionModel.efficientdet_d5_adv_prop.toString()]: 'EfficientDet D5 Adv Prop',
};

export const TrackingModelMapping = {
  [TrackingModel.simple_sort.toString()]: 'Simple SORT',
  [TrackingModel.deep_sort.toString()]: 'Deep SORT',
};
