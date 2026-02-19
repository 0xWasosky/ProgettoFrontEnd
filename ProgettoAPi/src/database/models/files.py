import os
import hashlib
from database.models._model import IModel
from database.models._database import _Database


"""

The file will be 


the has of the user 

"""


class Files(IModel, _Database):

    def __init__(self, collection) -> None:
        super().__init__(collection)

    async def add(self, user_id: int) -> bool:
        filenmae = hashlib.sha1(str(user_id).encode()).hexdigest() + ".mp3"

        return filenmae in os.listdir()

    async def update(self):
        raise NotImplemented("THis function is not needed for the pourpuse of the code")

    async def delete(self):
        raise NotImplemented("THis function is not needed for the pourpuse of the code")

    async def get(self):
        raise NotImplemented("THis function is not needed for the pourpuse of the code")
