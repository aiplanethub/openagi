import json
import logging
import os
import warnings
from typing import Any
from openagi.exception import OpenAGIException
try:
    from dotenv import load_dotenv
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play
    from pydantic import Field
except ImportError:
    raise OpenAGIException("Please install the required dependencies by running 'pip install -r requirements.txt'.")


from openagi.actions.base import ConfigurableAction

# Load environment variables
load_dotenv()

class ElevenLabsTTS(ConfigurableAction):
    """Use this Action to generate lifelike speech using ElevenLabs' text-to-speech API."""

    text: Any = Field(
        default_factory=str,
        description="Text input that needs to be converted to speech.",
    )
    voice_id: str = Field(
        default="JBFqnCBsd6RMkjVDRZzb",
        description="The ID of the voice to be used for speech synthesis.",
    )
    model_id: str = Field(
        default="eleven_multilingual_v2",
        description="The model ID used for text-to-speech conversion.",
    )
    output_format: str = Field(
        default="mp3_44100_128",
        description="The output format of the generated audio.",
    )
    api_key: str = Field(
        default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""),
        description="API key for ElevenLabs' authentication.",
    )

    def execute(self):
        logging.info(f"Generating speech for text: {self.text}")
        
        if not self.api_key:
            warnings.warn(
                "ElevenLabs API key is missing. Please provide it as a parameter or set it in the .env file.",
                DeprecationWarning,
                stacklevel=2
            )
            return json.dumps({"error": "ElevenLabs API key is missing. Please provide it as a parameter or set it in the .env file."})
        
        client = ElevenLabs(api_key=self.api_key)
        try:
            audio = client.text_to_speech.convert(
                text=self.text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,
            )
            play(audio)
            return json.dumps({"success": "Audio played successfully."})
        
        except Exception as e:
            logging.error(f"Error generating speech: {str(e)}")
            return json.dumps({"error": f"Failed to generate speech: {str(e)}"})
