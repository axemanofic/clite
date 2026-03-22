from clite import Clite, echo

app = Clite(
    name="myapp",
    description="A small package for creating command line interfaces",
)


@app.command()
def hello(name: str) -> None:
    echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
