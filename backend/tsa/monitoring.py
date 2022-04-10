from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

import neptune.new as neptune
import tensorflow as tf

from tsa.config import config, config_to_dict


class Monitor:
    run = None

    @classmethod
    @contextmanager
    def neptune_monitor(cls, name: Optional[str] = None, tags: Optional[List[str]] = None):
        cls.run = neptune.init_run(project=config.NEPTUNE_PROJECT, api_token=config.NEPTUNE_API_KEY, name=name)
        cls.run["sys/tags"].add(tags)
        cls.run["parameters"] = config_to_dict()
        try:
            yield cls.run
        finally:
            cls.run.stop()

    @classmethod
    def monitor_analysis(cls, analysis_generator):
        batch_counter = 1

        for batch in analysis_generator:
            cls.run["count/frame"].log(batch_counter)
            cls.run["count/detections"].log(tf.shape(batch[1])[0])

            yield batch

            batch_counter += 1

    @classmethod
    def monitor_duration(cls, generator_function, name):
        def inner_with_monitor(*args, **kwargs):
            generator_call = generator_function(*args, **kwargs)

            while True:
                try:
                    start = datetime.now()
                    generator_result = next(generator_call)
                    duration = datetime.now() - start
                    cls.run[f"duration/{name}"].log(duration)
                    yield generator_result
                except StopIteration:
                    break

        return inner_with_monitor
