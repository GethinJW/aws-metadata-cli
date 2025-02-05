class GenericError(Exception):
    msg: str

    def __init__(self, msg: str) -> None:
        self.msg = msg
        super()

class MissingCredentialsError(GenericError): pass
class InvalidCredentialsError(GenericError): pass