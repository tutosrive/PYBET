import random
import string

class Helpers:
    @staticmethod
    def random_key(size: int = 8) -> str:
        """
        Generates a random alphanumeric key of a specified size
        consisting of uppercase letters and digits.

        Args:
            size (int): Desired length of the generated key.

        Returns:
            str: A randomly generated alphanumeric string.
        """
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return key