from typing import Any

from clite import Clite
from clite.types import Argv


class CliRunner:
    def invoke(self, clite_instance: Clite, argv: Argv = None) -> Any:
        result = clite_instance(argv)
        print(result)
        return result
