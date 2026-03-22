<div align="center">
    <img alt="Clite" src="https://axemanofic.github.io/clite/assets/background.webp">
    <p>A zero-dependency package for building CLIs. Based on type hints.</p>
    <p>The name is inspired by the <a href="https://www.sqlite.org/">SQLite</a></p>
</div>

<div align="center">
![PyPI - Downloads](https://img.shields.io/pypi/dm/clite?style=for-the-badge&color=89dceb)
![PyPI - Version](https://img.shields.io/pypi/v/clite?style=for-the-badge&color=b4befe)
![PyPI - Status](https://img.shields.io/pypi/status/clite?style=for-the-badge&color=89dceb)
![PyPI - License](https://img.shields.io/pypi/l/clite?style=for-the-badge&color=74c7ec)
![PyPI - Types](https://img.shields.io/pypi/types/clite?style=for-the-badge&color=94e2d5)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clite?style=for-the-badge&color=f9e2af)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/axemanofic/clite/test.yml?branch=master&event=push&style=for-the-badge&color=a6e3a1)
</div>

---

**Documentation**: <a href="https://axemanofic.github.io/clite" target="_blank">https://axemanofic.github.io/clite</a>

**Source Code**: <a href="https://github.com/axemanofic/clite" target="_blank">https://github.com/axemanofic/clite</a>

---

## Installation

```sh
pip install clite
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

```
Hello, Alice!
```

## License

This project is licensed under the terms of the MIT license.
