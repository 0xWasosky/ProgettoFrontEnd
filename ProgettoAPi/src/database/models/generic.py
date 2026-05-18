from database.models._model import IModel
from database.models._database import _Database

from typing import Any


class Database(IModel, _Database):
    def __init__(self, collection) -> None:
        super().__init__(collection)

    async def add(self, data: dict, master_key: str) -> bool:
        #ho aggiunto await
        return await self.insert_unique(data, master_key)

    async def update(
        self, master_key: str, master_value: Any, key: str, new_data: Any, option: str
    ) -> bool:
        #Anche qui ho messo await
        if not await self.collection.find_one({master_key: master_value}):
            return False

        await self.collection.update_one(
            {master_key: master_value}, {option: {key: new_data}}
        )

        return True

    async def delete(self, master_key: str, master_value: Any) -> bool:
        #Pure qui
        if not await self.collection.find_one({master_key: master_value}):
            return False

        #Anche qui
        await self.collection.delete_one({master_key: master_value})

        return True

    async def get(
        self, master_key: str, master_value: Any, queries: list = []
    ) -> bool | dict:
        data = await self.collection.find_one({master_key: master_value})

        if data is None:
            return False

        if queries == []:
            return data
        else:
            new = {}
            keys = data.keys()

            for key in queries:
                if key in keys:
                    new[key] = data.get(key)

        return new
