from typing import List, Optional

from typing_extensions import TypeAlias

Argv: TypeAlias = Optional[List[str]]


from argparse import ArgumentParser

parser = ArgumentParser()
