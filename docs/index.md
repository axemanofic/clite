<div align="center">
    <h1> Clite </h1> 
    <img alt="Clite" src="https://axemanofic.github.io/clite/assets/background.webp">
    <p>A zero-dependency package for building CLIs. Based on type hints.</p>
    <p>The name is inspired by the <a href="https://www.sqlite.org/">SQLite</a></p>
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/clite?pypiBaseUrl=https%3A%2F%2Fpypi.org&style=for-the-badge&color=dc8a78">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/clite?style=for-the-badge&color=dd7878">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/clite?style=for-the-badge&color=ea76cb">
</div>

---

**Documentation**: <a href="https://axemanofic.github.io/clite" target="_blank">https://axemanofic.github.io/clite</a>

**Source Code**: <a href="https://github.com/axemanofic/clite" target="_blank">https://github.com/axemanofic/clite</a>

---

!!! warning 
    This package is currently under development.

## Installation

=== "pip"
    ```sh
    pip install clite
    ```
=== "uv"
    ```sh
    uv add clite
    ```
=== "poetry"
    ```sh
    poetry add clite
    ```

## Usage

### Example

```python
from clite import Clite

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)

@app.command()
def hello(name: str = "world"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

### Run it

```sh
python main.py hello Alice
```

Output:

```sh
Hello, Alice!
```

## License

This project is licensed under the terms of the MIT license.
