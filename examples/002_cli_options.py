from clite import Clite, echo

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)


@app.command()
def hello(name: int, *, verbose: bool = False) -> None:
    if verbose:
        echo("Verbose mode is on")
    echo(f"Hello, {name}!")


@app.command()
def helloargs(name: str, second: str, *, verbose: bool = False) -> None:
    if verbose:
        echo("Verbose mode is on")
    echo(f"Hello, {name} {second}!")


@app.command()
def helloempty() -> None:
    echo("Hello, world!")


if __name__ == "__main__":
    app()
