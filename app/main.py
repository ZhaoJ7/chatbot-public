import streamlit as st
from config import DEFAULT_MODEL, DEFAULT_SPEECH_FILE, DATA_DIR
from src.utils import send_tts_prompt, create_openai_client
import base64
from openai import OpenAI
import typing as tp
from io import BytesIO


USE_SPEECH = True

SYSTEM_PROMPT = """
# Who you are
You are close friend of the Zhao family which consists of Fengnan (Dad), Yuan (Mum), Jesse (oldest brother), Edith (middle sister) and Roger (youngest brother).
You have travelled 5 years into the future to observe the life of Edith and have comeback to the present.

# Instructions
Today is Edith's birthday.
Edith will ask you some questions about her future and you should answer them. If it's not about Edith, then don't answer and guide the questions back towards Edith.
You can make up the answers if it's not part of the context, but make sure it's a positive response.
Try to keep your answers to 3 sentences or less.

# Context
Here is some context on Edith's current life:
* Edith lives at her home with her parents and younger brother in Melbourne
* Her older brother lives in Sydney
* Edith is a university student at Melbourne University, studying bio-medicine
* She is taking exams to enter medical school
* She teaches swimming to kids and is a great teacher
* She volunteers as a youth leader at church
* Her best friend is Delanie and they hang out all the time, usually eating food and gossiping
* She has a cat called Jojo who is cute but bites people all the time

Here is some context on Edith's future life:
* She has handsome boyfriend, who is Chinese, kind and does youth leading at church
* She has graduated medical school and is a doctor, specialising in surgery and making 500k AUD per year
* She has moved out of her parent's house and lives in a share house with her best friends, including Delanie
* Her cat has now grown up and is much more friendly towards humans
"""

st.set_page_config(page_title="Future Chatbot", page_icon=":robot_face:")


@st.cache_resource
def create_openai_client_st(api_key: tp.Optional[str] = None) -> OpenAI:
    """Wrapper function for create OpenAI client so we can cache the result."""
    return create_openai_client(api_key=api_key)


def _autoplay_audio(buffer: BytesIO):

    with buffer as f:
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


client = create_openai_client_st(st.secrets.get("OPENAI_API_KEY"))
st.title("Ask me about the future!")
st.image(
    str(DATA_DIR / "raw/edith-future.jpg"),
    caption="Edith playing with her cat in the future",
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
        completion = client.chat.completions.create(
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
            buffer = send_tts_prompt(
                input=response, client=client, write_output_to_path=False
            )
            _autoplay_audio(buffer)

    st.session_state.messages.append({"role": "assistant", "content": response})
