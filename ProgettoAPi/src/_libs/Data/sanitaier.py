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
    async def check(lenght, name, max_size: int = 3750000) -> bool:
        """
        Docstring for check


        :param lenght: Description
        :param name: Description
        :param max_size: Description
        :return: Description
        :rtype: bool


        """

        #Ho modificato lievemente questa parte di codice perché da bloccava il caricamento di file
        #con nomi più lunghi di 10 caratteri, avevo visto un 256kbs così ho la lunghezza massima a 255 caratteri
        #Perfavore dimmi se ho fatto un errore
        if name is None or not isinstance(name, str) or not name.strip():
            return False
        if len(name) > 255:
            return False
        if lenght is not None and lenght >= max_size:
            return False
        return True
