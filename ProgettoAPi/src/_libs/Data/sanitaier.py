import re
import string


from .checker_base import IChecker


class Password(IChecker):
    """
    Docstring for Password

    Following: https://pages.nist.gov/800-63-4/sp800-63b/passwords/
    """

    @staticmethod
    async def check(password: str) -> bool:

        return all(
            (
                not (bool(len(password) < 16) or bool(len(password) > 64)),
                bool(re.search(f"[{string.ascii_lowercase}]", password)),
                bool(re.search(f"[{string.ascii_uppercase}]", password)),
                bool(re.search(r"[0-9]", password)),
            )
        )


class Username(IChecker):
    """
    Docstring for Username
    """

    @staticmethod
    async def check(username: str) -> bool:
        """
        Docstring for check

        :param username: Description
        :type username: str
        :return: Description
        :rtype: bool
        """

        return all(
            (
                not (bool(len(username) < 5) or bool(len(username) > 20)),
                not bool(re.search(r"[!\" <#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", username)),
            )
        )


class File(IChecker):
    @staticmethod
    async def check(type_, lenght, name) -> bool:
        """
        Docstring for check

        :param file: Description
        :return: Description
        :rtype: bool

        Source : https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html


        """

        return all(
            [
                not lenght >= 3750000,  # to 256 kbps
                not len(name) >= 10,
            ]
        )
