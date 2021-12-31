from konfetti import env, Konfig

MODELS_PATH = env("MODELS_PATH")

config = Konfig.from_object(__name__)
