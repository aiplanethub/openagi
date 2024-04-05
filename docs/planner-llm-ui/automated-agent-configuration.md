# Automated Agent Configuration

## Agent Configuration Planner

Agent configuration is prototype interface provided for the users to generate the configuration for various agents for solving a particular objective using either `Azure-OpenAI` or `OpenAI` as a `Planner LLM`. The resultant configuration need to be modified by the user to make it as executable program after thorough review of the tools, configurations.&#x20;

Command for strarting the planner LLM `python UI/OpenAGI.py`

### Planner LLM Execution

<figure><img src="../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

To view the interface, click on the URL depicted in the above figure, which begins with `http://127.0.0.1:8000`.&#x20;

Before entering your objective, adjust your browser's zoom to less than 70%. Clearly define your objective, such as `Provide  recommendations on Reliance Stock` in as much detail as possible, and then click the `Generate Config` button. Should you encounter any errors in the command line or an Internal Server Error, attempt to click the button again to regenerate the configuration. Typically, successful configuration generation takes about 30 seconds.

Users are advised to rename the tools and supply any additional configurations necessary for downloading and running the program.&#x20;

<figure><img src="../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

Enter the Objective as shown in the figure and Click Generate Config button.

<figure><img src="../.gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

Generated Config Code

If the configuration incorrectly generates the tool names, users are expected to replace with actual tools.

<figure><img src="../.gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>

#### Modified configuration code

The modified configuration can be viewed in the UI shown below. The generated tools are replaced with correct tool name.

<figure><img src="../.gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

Additionally, an example of the 'Human Tool' for use is provided, as detailed in the relevant section.

#### Download and Execute

Use the download button to obtain the file, then copy it from downloads folder into the usecases folder. To execute, run the command `python usecases/<generatedfile.py>`

