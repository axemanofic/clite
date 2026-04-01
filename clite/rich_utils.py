from rich.console import Console, ConsoleRenderable


def _to_ansi(console: Console, rich_obj: ConsoleRenderable) -> str:
    with console.capture() as cap:
        console.print(rich_obj)
    return cap.get()
