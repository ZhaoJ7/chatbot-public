import pathlib

HOME_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = HOME_DIR / "data"
DEFAULT_SPEECH_FILE = DATA_DIR / "tmp/speech.mp3"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_VOICE = "nova"
