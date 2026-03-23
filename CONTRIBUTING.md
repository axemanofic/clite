# Contributing

Thank you for your interest in **clite**! We welcome new contributors and are always open to collaboration.

## How to Contribute

1.  Fork this repository.
2.  Create a branch for your changes
3.  Set up the environment — install dependencies using **uv**:
    ```bash
    uv sync --all-groups
    ```
4.  Make your changes.
5.  Check your code:
    ```bash
    task all-checks
    ```
6.  Commit your changes with a clear description:
    ```bash
    git commit -m "feat: add new command for ..."
    ```
7. Submit the changes to your fork and create a pull request to the main repository. Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification when setting the PR title.

## Validation Tools

Before creating a PR, please check your code and fix any formatting issues:

*   **Linting**:
    ```bash
    uv run ruff check .
    uv run mypy .
    # or
    task lint
    ```
*   **Formatting**:
    ```bash
    uv run black .
    uv run isort .
    uv run ruff format .
    # or
    task format
    ```

## Code Style

*   Use **black** for code formatting.
*   Use **ruff** for linting(check pyproject.toml).

## Reporting Issues

If you find a bug or have a suggestion for improvement, please create an issue in this repository. Describe the problem in as much detail as possible and provide a code example if applicable.

## LIcense

All contributions are accepted under the MIT License.
