### Configuring .yaml File

1. Navigate to the `agentsConfig.yaml` file located at `src/openagi/config/agentsConfig.yaml`.
2. Follow the instructions provided in the file to configure it properly.
------------
### Configuring Tools

#### GitHub Tool

- In order to use the github tool, you'll require to create a github app with required permissions, or use this one [OpenAGI-github-app](https://github.com/apps/openagi-github-app)
- Add desired repositories you wanna give access to the app.
- Add private key in main directory of this repository.
- Follow to get [Github pem key](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps#generating-private-keys)

#### Gmail Tool

- Get gmail  `crendentials.json` from [here](https://developers.google.com/gmail/api/quickstart/python)
- Rename the file as crendentials.json and add it to main repository of openagi.

#### Document Compare

- Add all the files (pdf) you wanna use as Knowledge base to `documents/` directory. Create one in main directory.
- In order to run `usecases/ProfAgentJobSearch.py`, `usecases/ProfAgentDocument2.py`, `usecases/ProfAgentLegal.py` use sample files [here](https://drive.google.com/drive/folders/1fzC9nmtl0iE3WTpR_VlsIh9isjv0DI0p?usp=sharing) and place documents under `documents/` directory in main directory.  



### Note
Make sure to run `pip install -e .` in the main directory to make sure all the changes made in this directory persist.
