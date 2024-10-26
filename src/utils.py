from config import (
    DEFAULT_MODEL,
    DEFAULT_TTS_MODEL,
    DEFAULT_VOICE,
    DEFAULT_SPEECH_FILE,
)
import openai
import typing as tp
from pathlib import Path
from openai import OpenAI


def create_openai_client(api_key: tp.Optional[str] = None, **kwargs) -> OpenAI:

    # If the API key is None, we use load dot env to add the key from the .env file
    if api_key is None:
        from dotenv import load_dotenv

        load_dotenv()

    return OpenAI(api_key=api_key)


def send_basic_prompt(
    user_prompt: str,
    system_prompt: tp.Optional[str] = None,
    model: str = DEFAULT_MODEL,
    client: tp.Optional[openai.OpenAI] = None,
) -> str:

    if client is None:
        client = create_openai_client()

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
    client: tp.Optional[openai.OpenAI] = None,
) -> Path:

    if client is None:
        client = create_openai_client()

    if isinstance(output_path, str):
        output_path = Path(output_path)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input,
    )
    response.write_to_file(output_path)

    return output_path
