# Clite - a small package for creating command line interfaces

> The name is inspired by the [SQLite](https://www.sqlite.org/)

## :warning: This package is currently under development. :warning:

## Installation

```bash
pip install clite
```

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

## Roadmap

### 0.1.0 - Create a library for creating command line interfaces
- [x] Make it possible to create a CLI application
- [x] Make it possible to create a command via a decorator
- [x] Make it possible to create command arguments
- [x] Make it possible to create optional command arguments

### 0.2.0
- [ ] Make it possible to create subcommands

### 0.3.0 - Echo message in the console
- [ ] Make it possible to echo a message in the console

---

Copyright 2024 - today, Roman Sotnikov. All rights reserved.
