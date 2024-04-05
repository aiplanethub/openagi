## Installation

1. Setup a virtual environment.

   #### Note: Use python3.11

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Clone the repository

   ```bash
   git clone https://github.com/aiplanethub/agents.git
   ```

3. Go to the project directory

   ```bash
   cd agents
   ```

4. Install the package

   ```bash
   pip install .
   ```

   OR,

   ```bash
   pip install -e .
   ```

   When using the `-e` flag, the package is installed in editable mode. This means that if you make changes to the source code, you do not need to reinstall the package for the changes to take effect.

5. Run the application

   ```bash
   export AZURE_OPENAI_API_KEY="<your key>" # required AZURE OPENAI USAGE
   export SERPER_API_KEY="<your key>" # required for Google Serper API
   python usecases/ProfAgent.py
   ```

Note:
install "python -m spacy download en_core_web_sm" for executing "usecases/ProfAgentFeedback_Review.py"

## Dependency Managements

Using Poetry for Python project management is a streamlined way to manage dependencies and packages in your projects. Poetry handles dependency resolution, packaging, and publishing. Here's a basic guide on how to use Poetry to add or update packages in your project.

### Installing Poetry

First, ensure that Poetry is installed on your system. If it's not, you can install it by running:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Or, for newer versions of Poetry that prefer installation via the new installer:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or, if you're using `pip`:

```bash
pip install poetry
```

### Adding a Package

To add a new package to your project, use the `add` command. Poetry will automatically find the latest compatible version, update your `pyproject.toml` file, and install the package to your project's virtual environment:

```bash
poetry add package-name
```

Replace `package-name` with the name of the package you wish to add. If you need to install a specific version or specify version constraints, you can do so like this:

```bash
poetry add package-name@^2.0.5
```

This command tells Poetry to install a version compatible with version `2.0.5` according to semantic versioning.

### Updating a Package

To update a specific package to the latest compatible version, use the `update` command:

```bash
poetry update package-name
```

If you want to update all packages within the constraints defined in your `pyproject.toml`, simply run:

```bash
poetry update
```

### Checking for Updates

To check which packages are outdated, run:

```bash
poetry show --outdated
```

This command will list all packages that have newer versions available within the constraints set in your `pyproject.toml`.

### Removing a Package

If you need to remove a package from your project, use the `remove` command:

```bash
poetry remove package-name
```

This will remove the package and update your `pyproject.toml` and `poetry.lock` files accordingly.

### Managing Virtual Environments

Poetry automatically manages virtual environments for your project. To activate the virtual environment that Poetry has created for your project, you can run:

```bash
poetry shell
```

And to deactivate it, simply exit the shell as you would normally (e.g., by typing `exit` or pressing `Ctrl+D`).

For more detailed information, refer to the [official Poetry documentation](https://python-poetry.org/docs/). It provides comprehensive guides and references for all of Poetry's features and commands.

To ensure your project's dependencies are precisely mirrored in production environments or when collaborating with others, managing the `poetry.lock` file and generating a `requirements.txt` are important steps. Here's how to manage these tasks using Poetry:

### Updating the `poetry.lock` File

The `poetry.lock` file ensures that your project uses specific versions of dependencies, maintaining consistency across all environments. Whenever you add, update, or remove a package, Poetry automatically updates this lock file. However, if you manually edit `pyproject.toml` or wish to refresh your lock file to the latest versions within your specified constraints, you can explicitly update the lock file without changing your dependencies by running:

```bash
poetry update --lock
```

This command updates the `poetry.lock` file with the latest compatible versions of your dependencies without actually updating the packages in your virtual environment. It's useful for testing the latest versions of your dependencies for compatibility purposes.

### Generating a `requirements.txt` File

While Poetry projects use the `pyproject.toml` and `poetry.lock` files for dependency management, some environments or tools still require a traditional `requirements.txt` file. To generate a `requirements.txt` from your Poetry-managed project, you can use the `export` command:

```bash
poetry export -f requirements.txt --output requirements.txt
```

This command creates a `requirements.txt` file with all of the project's dependencies, including transitive (sub-dependencies), at their locked versions. If you want to include only the main dependencies (excluding sub-dependencies), you can add the `--without-hashes` option:

```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

If you need the `requirements.txt` for development dependencies as well, you can include them with the `--dev` option:

```bash
poetry export -f requirements.txt --dev --output requirements-dev.txt
```

### Summary

- **Update the lock file**: Regularly update your `poetry.lock` by running `poetry update --lock` to keep your dependencies fresh within the constraints defined in `pyproject.toml`.
- **Generate `requirements.txt`**: Use `poetry export -f requirements.txt --output requirements.txt` to generate a `requirements.txt` file for compatibility with systems requiring this format.
- **Manage virtual environments**: Poetry automatically manages virtual environments for your project. Use `poetry shell` to activate the virtual environment and `exit` to deactivate it.
