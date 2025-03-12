# Get Started

## Installation

::: code-group

```sh [pip]
$ pip install clite
```

```sh [poetry]
$ poetry add clite
```

```sh [uv]
$ uv add clite
```

:::

## Usage

```python
from clite import Clite

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)

@app.command()
def hello():
    print("Hello, world!")

if __name__ == "__main__":
    app()
```

```python:line-numbers
from clite import Clite

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)

@app.command()
def hello():
    print("Hello, world!")

if __name__ == "__main__":
    app()
```
<Editor id="i-should-be-unique" />
