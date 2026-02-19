from database.models._model import IModel
from database.models._database import _Database

from argon2 import PasswordHasher

"""

Inserire policy per la gestione delle password:  argon2id

Implementare password policy: https://cybersecuritynews.com/nist-rules-password-security/


search index for id :)


Create a wrapper function to update_data


"""


hasher = PasswordHasher()


class User(IModel, _Database):
    ids = 1000

    def __init__(self, collection) -> None:
        super().__init__(collection)

    async def add(self, username: str, password: str) -> bool | int:
        local_id = self.ids
        document = {
            "username": username,
            "password": hasher.hash(password),
            "id": local_id,
            "school": "Eu",
        }

        insert = await self.insert_unique(
            document, "username"
        )  # to check even for id -> int max value

        if insert:
            self.ids += 1
            return local_id

        return False

    async def update(
        self, key: str, new_value: str, id_: int, _old_password: str = None
    ) -> bool:
        """
        Docstring for update

        :param self: Description
        :param key: Description
        :type key: str Must be "username" or "password"
        :return: Description
        :rtype: bool
        """

        data = await self.find_data("id", id_)

        if data is None:
            return False

        if key == "username":
            await self.collection.update_one({"id": id_}, {"$set": {key: new_value}})

        elif key == "password":
            password_hash = data.get("password")
            if hasher.verify(password_hash, _old_password):

                await self.collection.update_one(
                    {"id": id_}, {"$set": {"password": hasher.hash(new_value)}}
                )
            else:
                return False

        else:
            return False

        return True

    async def delete(self, id_: int, password: str) -> bool:
        """
        Docstring for delete

        :param self: Description
        :param id_: Description
        :type id_: int
        :param password: Description
        :type password: str
        :return: Description
        :rtype: bool
        """

        data = await self.find_data("id", id_)

        if data is None:
            return False

        if hasher.verify(data.get("password"), password):
            await self.collection.delete_one({"id": id_})

    async def get(self, username: str, password: str) -> dict | None:
        """
        Docstring for get

        :param self: Description
        :param username: Description
        :type username: str
        :param password: Description
        :type password: str
        :return: Description
        :rtype: dict | None
        """

        data = await self.find_data("username", username)

        if not hasher.verify(data.get("password"), password) or data is None:
            return None

        return data
