class DomainException(Exception):
    def __init__(self, message: str = "A domain error occurred."):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(DomainException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class UserAlreadyExistsException(DomainException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)


class FolderNotFoundException(DomainException):
    def __init__(self, message: str = "Folder not found"):
        super().__init__(message)


class FolderAlreadyExistsException(DomainException):
    def __init__(self, message: str = "Folder already exists"):
        super().__init__(message)


class NoteNotFoundException(DomainException):
    def __init__(self, message: str = "Note not found"):
        super().__init__(message)


class LabelNotFoundException(DomainException):
    def __init__(self, message: str = "Label not found"):
        super().__init__(message)


class LabelAlreadyExistsException(DomainException):
    def __init__(self, message: str = "Label already exists"):
        super().__init__(message)

