from clite import Clite, echo

app = Clite(
    name="playground",
    description="A playground for clite",
)


@app.command(
    name="hello",
    description="Prints Hello from playground!",
)
def hello(name: str) -> None:
    """Print Hello from playground."""
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
