from contextlib import contextmanager
from typing import List, Optional

import neptune.new as neptune

from tsa.config import config, config_to_dict


@contextmanager
def neptune_monitor(name: Optional[str] = None, tags: Optional[List[str]] = None):
    run = neptune.init_run(project=config.NEPTUNE_PROJECT, api_token=config.NEPTUNE_API_KEY, name=name)
    run["sys/tags"].add(tags)
    run["parameters"] = config_to_dict()
    try:
        yield run
    finally:
        run.stop()
