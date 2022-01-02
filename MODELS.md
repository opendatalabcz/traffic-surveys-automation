# Deep learning models

This document briefly introduces deep learning models used in this project, including information about how we
created these models.

## Efficientdet models

These are built from Google's AutoML implementation located at https://github.com/google/automl/tree/0b0ba5ebd0860edd939465fc4152da4ff9f79b44/efficientdet.

These models perform a non-max suppression as a part of their pipeline. Our configuration of NMS parameters minimizes
the effect of this operation to minimum so that our own version of NMS can affect the results.

### Efficientdet-d5-advprop-aa

D5 version is trained with AdvProp and AutoAugmentation which should improve model's robustness and ability to generalize
on images that are blured.

It is converted from the original checkpoint (https://storage.googleapis.com/cloud-tpu-checkpoints/efficientdet/advprop/efficientdet-d5.tar.gz) using the following command:

```bash
python efficientdet/model_inspect.py \
    --runmode=saved_model \
    --model_name=efficientdet-d5 \
    --ckpt_path=original_models/efficientdet-d5 \
    --saved_model_dir=traffic_survey_automation/models/efficientdet-d5-advprop-aa \
    --batch_size=0 \
    --hparams=params.yaml \
    --max_boxes_to_draw=512 \
    --min_score_thresh=0.05 \
    --nms_method=gaussian
```

### Efficientdet-d6

This is a standard version of the architecture extracted from checkpoint (https://storage.googleapis.com/cloud-tpu-checkpoints/efficientdet/coco2/efficientdet-d6.tar.gz) using:

```bash
python efficientdet/model_inspect.py \
    --runmode=saved_model \
    --model_name=efficientdet-d6 \
    --ckpt_path=original_models/efficientdet-d6 \
    --saved_model_dir=traffic_survey_automation/models/efficientdet-d6 \
    --batch_size=0 \
    --hparams=params.yaml \
    --max_boxes_to_draw=512 \
    --min_score_thresh=0.05 \
    --nms_method=gaussian
```

The `params.yaml` file is configured as follows:
```yaml
image_size: "1280x720"
nms_configs:
  sigma: 0.6
  iou_thresh: 0.97
```

We made a slight adjustment to the code of `efficientdet/tf2/postprocess.py:186` to allow configuration of other
than `1.0` value for `iou_threshold` to:
```python
iou_thresh = nms_configs['iou_thresh'] or 1.0
```
