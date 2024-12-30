from openagi.actions.base import ConfigurableAction
from pydantic import Field
import json

try:
    from huggingface_hub import HfApi
except ImportError:
    raise Exception("Install huggingface_hub with cmd `pip install huggingface`")

class HuggingFaceTool(ConfigurableAction):
    """
    Tool for exploring Hugging Face models and datasets.
    """
    query: str = Field(..., description="Dataset or model name to search on Hugging Face.")

    def execute(self) -> str:
        api = HfApi()
        results_dict = {}

        models = api.list_models(search=self.query, limit=15)
        datasets = api.list_datasets(search=self.query, limit=15)

        for model in models:
            results_dict[model.modelId] = f"https://huggingface.co/{model.modelId}"

        for dataset in datasets:
            results_dict[dataset.id] = f"https://huggingface.co/datasets/{dataset.id}"

        return json.dumps(results_dict)