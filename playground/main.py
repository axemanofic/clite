from clite import Clite, echo

app = Clite(
    name="playground",
    description="A playground for clite",
)


@app.root()
def root() -> None:
    """Print hello world from root."""
    echo("Hello world")


@app.command(
    name="hello",
    description="Prints Hello from playground!",
)
def hello(name: str, flag: int = 1) -> None:
    """Print Hello from playground."""
    echo(f"Hello {flag}")
    echo(f"Hello from playground, {name}!")


@app.command(
    name="start",
    description="Start playground",
)
def start() -> None:
    """Start playground."""
    echo("Start playground")


if __name__ == "__main__":
    app()
