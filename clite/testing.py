from clite import Clite
from clite.main import Result
from clite.types import Argv


class CliRunner:
    def invoke(self, clite_instance: Clite, argv: Argv = None) -> Result:
        result = clite_instance._run(argv)
        return result
