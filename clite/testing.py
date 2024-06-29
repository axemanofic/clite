from clite import Clite


class Result:
    def __init__(self):
        pass


class CliRunner:
    def invoke(
        self,
        clite_instance: Clite,
        argv: list[str] | None = None,
        name: str | None = None,
        description: str | None = None,
    ):
        import sys

        clite_instance.run(
            argv,
            # name,
            # description,
        )
        print(sys.stdout)
        # for line in sys.stdout.read():
        #     print(line)
        return Result()
