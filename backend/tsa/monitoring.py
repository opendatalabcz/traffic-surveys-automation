from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

import neptune.new as neptune
import tensorflow as tf

from tsa.config import config, config_to_dict


class NoopMonitor:
    def __init__(self) -> None:
        self.monitor = {}
    
    def stop(self):
        pass

    def analysis(self, generator):
        yield from generator
    
    def duration(self, _, generator_function, *args, **kwargs):
        yield from generator_function(*args, **kwargs)


class NeptuneMonitor:
    def __init__(self, name: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        self.monitor = neptune.init_run(project=config.NEPTUNE_PROJECT, api_token=config.NEPTUNE_API_KEY, name=name)
        self.monitor["sys/tags"].add(tags)
        self.monitor["parameters"] = config_to_dict()
    
    def stop(self):
        self.monitor.stop()
    
    def analysis(self, generator):
        batch_counter = 1

        for batch in generator:
            self.monitor["count/frame"].log(batch_counter)
            self.monitor["count/detections"].log(tf.shape(batch[1])[0])

            yield batch

            batch_counter += 1
    
    def duration(self, name, generator_function, *args, **kwargs):
        generator_call = generator_function(*args, **kwargs)

        while True:
            try:
                start = datetime.now()
                generator_result = next(generator_call)
                duration = datetime.now() - start
                self.monitor[f"duration/{name}"].log(duration)
                yield generator_result
            except StopIteration:
                break


class Monitor:
    run = None

    @classmethod
    @contextmanager
    def neptune_monitor(cls, name: Optional[str] = None, tags: Optional[List[str]] = None):
        if config.NEPTUNE_API_KEY:
            cls.run = NeptuneMonitor(name, tags)
        else:
            cls.run = NoopMonitor()

        try:
            yield cls.run.monitor
        finally:
            cls.run.stop()

    @classmethod
    def monitor_analysis(cls, analysis_generator):
        return cls.run.analysis(analysis_generator)

    @classmethod
    def monitor_duration(cls, generator_function, name):
        def inner(*args, **kwargs):
            yield from cls.run.duration(name, generator_function, *args, **kwargs)

        return inner
