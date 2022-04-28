# Traffic survey automator

Traffic survey automator is a software that analyses traffic recordings using deep learning and statistical algorithms.
It outputs the numbers of vehicles passing through the defined regions of interest.

It was developed as a part of a master's thesis at Faculty of Information Technology at Czech Technical University in
Prague in Spring 2022.

The application consists of a backend and a frontend. The frontend displays information about existing source videos,
performed analyses, shows visualizations and results and enables a user to create new task for analysis, including
parameters customization.

Backend servers responses to the requests from frontend, schedules the analysis tasks which are executed by `celery`
workers asynchronously.

**Models:**

- EfficientDet D6
- EfficientDet D5 Adv-Prop

**Algorithms:**

- Simple Online and Realtime Tracking with constant acceleration Kalman filter modelling
- Deep Online and Realtime Tracking with the same Kalman filter model, VGG16 feature embedding

**Technologies:**

- tensorflow
- OpenCV
- FastAPI, pydantic, SQLAlchemy
- ReactJS

## Download models

The common pre-requirement is to download the pre-trained deep learning models for object detection. How we created
these checkpoints is described in section _Exporting models_ below. The models have to be downloaded and stored in the
`MODELS_PATH`.

- EfficientDet D5 Adv-prop: https://owncloud.cesnet.cz/index.php/s/IUnmEK9iFol9NaF
- EfficientDet D6: https://owncloud.cesnet.cz/index.php/s/KPeGv4rl3cJKLDj

## Running via Docker

We provide `Dockerfile`s for both backend and frontend, plus a `docker-compose` to bring everything together.
The `docker-compose` configuration describes well what is needed to run the whole application.

`PostgreSQL` and `redis` are included for simple and fast start-up. Both can be replaced by an online alternative by
changing the environment variables **DATABASE_NAME**, **DATABASE_URL** and **CELERY_BROKER** on `tsa-backend`.
The database URL should be without `postgresql://` prefix. This is added automatically by the application as
`postgresql+asyncpg://`.

Four folders are necessary:

- **source_files:** the source video recordings
- **output_analysis:** the output JSON analysis data are stored here
- **models:** source of the deep learning models checkpoints
- **postgres_data:** place where the docker-composed PostgreSQL stores its data

All of these locations are mounted from the local system and the necessary environment variables are set up. Please,
adjust those, if needed.

By default, backend is available on `http://localhost:8000` and frontend on `http://localhost:3000`. You can adjust the
ports.

## Running on local machine

The application's backend runs on **Python 3.8** and **3.9** using `poetry` dependency manager. First, you have to have
one of the required versions of Python and poetry installed. Then, follow the steps below.

1. Run `poetry install` inside the `backend/` folder.
2. Download the deep learning models and place them into the `models/` folder.
3. Export the necessary environment variables and create the required folders to store data. It is the set of 6
   variables defined in the `docker-compose.yaml`, `tsa-backend`.
4. Optionally, `neptune.ai` project name and api key can be set up to monitor the experiments via Neptune. See
   `tsa.config.base` how to set these.
5. Activate the virtual environment `poetry shell`.
6. Apply migrations through `alembic upgrade head`, if necessary.
7. Run a CLI utility command located in `cli/` package. Refer to the documentation of those commands by running
   `python cli/*.py --help`.
8. Start the **uvicorn** server `uvicorn --port 8000 tsa.app.app:fast_app`
9. There is a set of `poe-the-poet` commands predefined for quick execution:
   - `poe black` to format the code,
   - `poe sort` to sort imports,
   - `poe test` to run those few tests,
   - `poe run` to **start the backend application** on port `8000`,
   - `poe worker` to start the celery worker that processes the analyses queue.

To run the application's frontend:

1. Make sure you have `node` and `npm` installed on your machine.
2. Create a copy of `.env.example` named `.env` and set the API URL according to where backend is located.
3. Run `npm install` to install all the dependencies.
4. Run `npm start` to start the frontend application on port `4000`.

## Exporting models

The models that we use are pretrained on `COCO` dataset. These are built from Google's AutoML implementation located at
https://github.com/google/automl/tree/0b0ba5ebd0860edd939465fc4152da4ff9f79b44/efficientdet.

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
