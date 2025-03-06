class UsageError(Exception):
    pass


class BadParameter(Exception):
    @classmethod
    def fomat_message(cls, param_hint: str, message: str) -> "BadParameter":
        return cls(f"Invalid value for {param_hint}: {message}")
