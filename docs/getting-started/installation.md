# Installation

To install OpenAGI, lets practice some best practice by creating a virtual environment and installing the package.&#x20;

#### Setup a virtual environment

> Note: Use python3.11 ONLY. Support for 3.10 and 3.9 will be coming in future releases.

```bash
# For Mac users
python3 -m venv venv
source venv/bin/activate

# For Windows users
python -m venv venv
venv/scripts/activate

# to create virtual env using particular python version (in Windows)
py -3.11 -m venv venv
```

#### Install the Package

```bash
pip install openagi
```

## Setup your credentials

### Export required keys

OpenAGI supports various tools integration and LLM support that requires few secret API keys and other credentials to setup. We provide support to directly configure it with a `config.yaml` path.&#x20;

Use `OPENAGI_CONFIG_PATH` variable with absolute path on where the config.yaml file exists.&#x20;

```
# For Mac or Bash or Linux users:

export OPENAGI_CONFIG_PATH="path/to/your/config/yaml/file" 

e.g., export OPENAGI_CONFIG_PATH = "agentsConfig.yaml" 

# For windows users (use command line in administration mode)

setx OPENAGI_CONFIG_PATH "agentsConfig.yaml"

# Note: Once you set the config path, restart the terminal. 
```

Note: For windows users you can directly use export command while using `git-bash`

### Sample Configuration

Please note that in your scenario, the agentsConfig.yaml file is new, so you may need to add the keys from scratch. Refer to the tools page to obtain the necessary key variables that need to be added in the config file.

{% code fullWidth="false" %}
```yaml
#configuration required to run basic use cases
BASE_URL: <your_base_url> # your azure openai api key marketplace
DEPLOYMENT_NAME: <your_deployment_name> # Name of your deployed instance
AZURE_DEPLOYMENT: <your_azure_deployment_name> # Name of your deployed azure instance
MODEL_NAME: <gpt_model_name> # Model name
OPENAI_API_VERSION: <openai_api_version> # Version of Model
#use case specific configuration
GMAIL_CREDS: <your_gmail_credentials> # Refer to note below
GITHUB_REPOSITORY: <your_github_repository> # Github repository you want to work with.
GITHUB_APP_PRIVATE_KEY: <your_github_private_key> # Refer to note below
xorbotsCSVFileName: <path_to_your_csv_file> # any csv file to perform using pandas and numpy
sqlLiteDBName: <path_to_your_sqllitedb> # Sqlite .db file
pdfFile: <path_to_your_pdf_document> # Directory where you have stored all your pdfs for Chat.
#change only when required

EXA_NUM_SEARCH_RESULTS: !!int 1 
#number of exa search results
MAX_NUMBER_OF_AGENTS: !!int 5
#defaulted for 5 agents


AZURE_OPENAI_API_KEY: <your_azure_openai_api_key>
SERPER_API_KEY: <your_serper_api_key>
OPENAI_API_KEY: <your_openai_key>
EXA_API_KEY: <your_exa_api_key>


TEMPERATURE: !!float 0.5
EMBEDDING_DEPLOYMENT: <your azure embedding deployment> # Embedding models deployment
```
{% endcode %}
