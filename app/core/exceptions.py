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


class TagNotFoundException(DomainException):
    def __init__(self, message: str = "Tag not found"):
        super().__init__(message)


class TagAlreadyExistsException(DomainException):
    def __init__(self, message: str = "Tag already exists"):
        super().__init__(message)


class CommentNotFoundException(DomainException):
    def __init__(self, message: str = "Comment not found"):
        super().__init__(message)