from pathlib import Path

from konfetti import Konfig

CONFIG_DIR = Path(__file__).parent

config = Konfig.from_object("tsa.config.base")

config.extend_with_json(CONFIG_DIR / "efficientdet.config.json")
config.extend_with_json(CONFIG_DIR / "sort.config.json")
config.extend_with_json(CONFIG_DIR / "deep_sort.config.json")
