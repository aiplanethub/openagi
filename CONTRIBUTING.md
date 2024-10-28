# Contributing to OpenAGI

Thank you for your interest in contributing to OpenAGI! We appreciate your efforts in helping us make human-like agents accessible to everyone. This guide outlines the steps to start contributing effectively.


## Forking the Repository
To contribute to OpenAGI, you need to fork the repository and clone it locally. Follow these steps:

1. Navigate to the [OpenAGI repository](https://github.com/aiplanethub/openagi.git).
2. Click the **Fork** button in the top-right corner to create a personal copy of the repository.
3. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/your-username/OpenAGI.git
    cd OpenAGI
    ```

## Setting up Your Environment
Once you have cloned the repository, set up a development environment to work on the code. Follow the instructions below to create and activate a virtual environment.

## Installation

1. Setup a virtual environment.

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

2. Install the openagi

   ```bash
   pip install openagi
   ```

## To setup your credentials

Follow this quick [installation guide](https://openagi.aiplanet.com/getting-started/installation) to complete the setup.

## Documentation

For more queries find documentation for OpenAGI at [openagi.aiplanet.com](https://openagi.aiplanet.com/)

## Understand OpenAGI

![Thumbnails](https://github.com/aiplanethub/openagi/blob/dev/assets/openagi.png)


## Making Changes
Before making any changes to the codebase, follow these steps:

    # Ensure you are on the correct branch:
    git checkout main
    
    # Create a new branch for your changes:
    git checkout -b feature-branch-name
   
Make your changes in the relevant directories (e.g., src, docs, cookbook, etc.). Be sure to follow the coding guidelines and maintain consistency with the project’s code style.

## Testing Your Changes

Before submitting your changes, it is crucial to ensure that your modifications work as expected. Follow these steps to test your changes locally:
1. Run the necessary tests or manually check the functionality you have worked on.
2. Ensure that no other features are broken due to your changes.

## Submitting Your Pull Request
Once you have tested your changes and everything is working correctly, submit your contribution by following these steps:

    # Stage your changes:
    git add .
    
    # Commit your changes with a meaningful commit message:
    git commit -m "Brief description of the changes made"
    
    # Push your changes to your forked repository:
    git push origin feature-branch-name
    
## Open a Pull Request (PR):

1. Navigate to the OpenAGI repository on GitHub.
2. Click the Pull Requests tab, then click New Pull Request.
3. Select the branch you pushed from the dropdown menu.
4. Add a title and a detailed description of your changes.
5. Click Submit Pull Request.

