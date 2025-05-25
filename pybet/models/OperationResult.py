class OperationResult:
    """
    Encapsulates the result of an operation, indicating success or failure and carrying data or error information.

    Attributes:
        success (bool): True if the operation succeeded, False otherwise.
        data (any): The data returned by the operation, if any.
        error (any): The error information if the operation failed.
    """

    def __init__(self, success: bool = True, data: any = None, error: any = None) -> None:
        self.success: bool = success
        self.data: any = data
        self.error: any = error

    def to_dict(self) -> dict:
        """
        Converts the OperationResult to a dictionary.

        Returns:
            dict: A dictionary representation of the result.
        """
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }