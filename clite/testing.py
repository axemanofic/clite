from typing import Optional
from clite import Clite
from clite.types import Argv


class Result:
    def __init__(self):
        pass


class CliRunner:
    def invoke(
        self,
        clite_instance: Clite,
        argv: Argv = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        import sys

        result = clite_instance.run(
            argv,
            # name,
            # description,
        )

        for line in sys.stdout:
            print(line)
        return Result()
