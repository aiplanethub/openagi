from openagi.actions.base import ConfigurableAction
from pydantic import Field
from openagi.exception import OpenAGIException
import warnings
import os
import time

try:
    from lumaai import LumaAI
    import requests
except ImportError:
    raise OpenAGIException("Install required packages with cmd `pip install lumaai requests`")

class LumaLabsTool(ConfigurableAction):
    """Luma Labs Tool for generating AI images and videos.
    
    This action uses the Luma Labs API to generate images or videos based on text prompts.
    Supports various features including image generation, video generation, and camera motions.
    Requires an API key to be configured before use.
    """
    
    prompt: str = Field(..., description="Text prompt to generate image or video content")
    mode: str = Field(
        default="image",
        description="Mode of operation: 'image' or 'video'"
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="Aspect ratio (1:1, 3:4, 4:3, 9:16, 16:9, 9:21, 21:9)"
    )
    model: str = Field(
        default="photon-1",
        description="Model to use (photon-1, photon-flash-1, ray-2 for video)"
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        self._check_deprecated_usage()
    
    def _check_deprecated_usage(self):
        if 'LUMAAI_API_KEY' in os.environ and not self.get_config('api_key'):
            warnings.warn(
                "Using environment variables for API keys is deprecated. "
                "Please use LumaLabsTool.set_config(api_key='your_key') instead.",
                DeprecationWarning,
                stacklevel=2
            )
            self.set_config(api_key=os.environ['LUMAAI_API_KEY'])

    def execute(self) -> str:
        api_key: str = self.get_config('api_key')
        if not api_key:
            if 'LUMAAI_API_KEY' in os.environ:
                api_key = os.environ['LUMAAI_API_KEY']
                warnings.warn(
                    "Using environment variables for API keys is deprecated. "
                    "Please use LumaLabsTool.set_config(api_key='your_key') instead.",
                    DeprecationWarning,
                    stacklevel=2
                )
            else:
                raise OpenAGIException("API KEY NOT FOUND. Use LumaLabsTool.set_config(api_key='your_key') to set the API key.")

        client = LumaAI(auth_token=api_key)

        try:
            if self.mode == "image":
                generation = client.generations.image.create(
                    prompt=self.prompt,
                    aspect_ratio=self.aspect_ratio,
                    model=self.model
                )
            else:
                generation = client.generations.create(
                    prompt=self.prompt,
                    aspect_ratio=self.aspect_ratio,
                    model="ray-2" if self.model == "ray-2" else "photon-1"
                )

            completed = False
            while not completed:
                generation = client.generations.get(id=generation.id)
                if generation.state == "completed":
                    completed = True
                elif generation.state == "failed":
                    raise OpenAGIException(f"Generation failed: {generation.failure_reason}")
                time.sleep(2)

            if self.mode == "image":
                result_url = generation.assets.image
                file_extension = "jpg"
            else:
                result_url = generation.assets.video
                file_extension = "mp4"

            response = requests.get(result_url, stream=True)
            file_name = f'{generation.id}.{file_extension}'
            with open(file_name, 'wb') as file:
                file.write(response.content)

            return f"""Generation completed successfully!
                   Mode: {self.mode}
                   File saved as: {file_name}
                   Prompt: {self.prompt}
                   URL: {result_url}"""

        except Exception as e:
            raise OpenAGIException(f"Error in Luma Labs generation: {str(e)}")
