from src.transcribe import transcribe
import pytest

@pytest.mark.skip(reason="will call google speech API")
def test_transcribe():
    response_text = transcribe() 
    assert isinstance(response_text, str)

