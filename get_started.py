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
