from typing import Any

class OperationResult:
    """
    Standard result wrapper for operations.

    Attributes:
        ok (bool): True if operation succeeded.
        data (Any): Result data on success.
        error (Optional[Any]): Error message or exception on failure.
    """

    def __init__(self, ok: bool = False, data: Any = None, error: Any = None) -> None:
        """
        Initializes an OperationResult.

        Args:
            ok (bool): Whether the operation succeeded.
            data (Any, optional): The data returned by the operation.
            error (Any, optional): The error if the operation failed.
        """
        self.ok: bool = ok
        self.data: Any = data
        self.error: Any = error

    @property
    def success(self) -> bool:
        """
        Alias for .ok to support legacy or alternate naming.
        """
        return self.ok

    def to_dict(self) -> dict:
        """
        Converts the OperationResult to a dictionary.

        Returns:
            dict: A dictionary representation of the result.
        """
        return {
            "ok": self.ok,
            "data": self.data,
            "error": self.error
        }