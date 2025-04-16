import random
import string

class Helpers:
    @staticmethod
    def random_key(size:int = 8) -> str:
        """
        Generates a random alphanumeric key of a specified size consisting of uppercase letters
        and digits. The generated key can be used where unique identifiers are needed or
        for simple token generation purposes. The default size is 8 characters.

        :param size: The desired length of the generated key.
        :type size: int
        :return: A randomly generated alphanumeric string.
        :rtype: str
        """
        __key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return __key