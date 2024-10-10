from config import (
    client as openai_client,
    DEFAULT_MODEL,
    DEFAULT_TTS_MODEL,
    DEFAULT_VOICE,
    DEFAULT_SPEECH_FILE,
)
import openai
import typing as tp
from pathlib import Path


def send_basic_prompt(
    user_prompt: str,
    system_prompt: tp.Optional[str] = None,
    model: str = DEFAULT_MODEL,
    client: openai.OpenAI = openai_client,
) -> str:

    messages = []
    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_prompt})

    completion = client.chat.completions.create(model=model, messages=messages)

    return completion.choices[0].message.content


def send_tts_prompt(
    input: str,
    voice: str = DEFAULT_VOICE,
    model: str = DEFAULT_TTS_MODEL,
    output_path: tp.Union[str, Path] = DEFAULT_SPEECH_FILE,
) -> Path:

    if isinstance(output_path, str):
        output_path = Path(output_path)

    response = openai_client.audio.speech.create(
        model=model,
        voice=voice,
        input=input,
    )
    response.write_to_file(output_path)

    return output_path
