import streamlit as st
from config import client as openai_client, DEFAULT_MODEL, DEFAULT_SPEECH_FILE, DATA_DIR
from src.utils import send_tts_prompt
import base64

USE_SPEECH = True

SYSTEM_PROMPT = """
You are a close friend of a loving couple named Jesse and Isabel. 
You have travelled 10 years into the future to observe how they are living and have now come back to the present. 
It is Isabel's birthday today and she wants to ask you how their lives are in the future.
Whenever, Isabel asks you a question, you must give an answer based on the below context.
You can make up some answers if it's required, but make sure it's a happy response.
Try to keep your answers to three sentences or less.

Here is some context on their lives in the present:
* Jesse and Isabel are currently living in Sydney, Australia
* They live in a two bedroom apartment in the suburb of Zetland, with their cat Lua
* Jesse is a data scientist, in the early stages of his career, trying to climb the management ladder.
* Isabel is a clinical trials statistician, who is looking to use her skills in statistics to help with cancer treatment
* They hang out with their friends on the weekend, going for runs at the park, eating together and going to the beach

Here is some context on their lives in the future:
* They now live in a 5-bedroom mansion in the suburb of Mosman
* They have 10 kids together, who run around the house all of the time
* They have a strong friendship group who hang out all the time together
* Jesse is now the Chief Data Officer of a top company in Australia
* Isabel has found the cure for cancer through her statistical analysis and has won a Nobel Prize
* Every Summer and Winter holidays, they go on a holiday to amazing destinations
"""


def _autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


st.title("Ask me about the future!")
st.image(
    str(DATA_DIR / "raw/couple-in-future.jpg"),
    caption="Jesse and Isabel in the future",
    width=300,
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = DEFAULT_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What's on your mind Isabel?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = openai_client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=not USE_SPEECH,
        )

        if not USE_SPEECH:
            response = st.write_stream(completion)
        else:
            response = completion.choices[0].message.content
            speech_path = send_tts_prompt(
                input=response, output_path=DEFAULT_SPEECH_FILE
            )
            _autoplay_audio(str(speech_path))

    st.session_state.messages.append({"role": "assistant", "content": response})
