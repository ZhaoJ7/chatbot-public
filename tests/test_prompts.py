from src.utils import send_basic_prompt


def test_connection():
    system_prompt = """
    Your role is to confirm that the API connection is working. Do one of the following:
    * If the user sends a "Test" message, reply "Success"
    * If the user sends any other message, reply "Invalid prompt"
    Don't reply with anything else.
    """

    response = send_basic_prompt(
        user_prompt="Test",
        system_prompt=system_prompt,
    )
    assert response == "Success"

    response = send_basic_prompt(
        user_prompt="What's the weather today?", system_prompt=system_prompt
    )
    assert response == "Invalid prompt"
