from clite import Clite

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)


@app.command()
def hello(name: int, *, verbose: bool = False) -> None:
    if verbose:
        print("Verbose mode is on")
    print(f"Hello, {name}!")


@app.command()
def helloargs(name: str, second: str, *, verbose: bool = False) -> None:
    if verbose:
        print("Verbose mode is on")
    print(f"Hello, {name} {second}!")


@app.command()
def helloempty() -> None:
    print("Hello, world!")


if __name__ == "__main__":
    app()
