from motor.motor_asyncio import AsyncIOMotorCollection  # to check


"""


Improve code efficency using pymongo indexes : https://www.mongodb.com/docs/languages/python/pymongo-driver/current/indexes/


CHange with the motor lib 

from motor.motor_asyncio import AsyncIOMotorClient




"""


class _Database:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def insert_unique(self, data: dict, key: str) -> bool:
        """
        Docstring for insert_unique

        :param self: Description
        :param data: Description
        :type data: dict
        :param key: Description
        :type key: str
        :param options: Description
        :type options: dict
        :return: Description
        :rtype: bool

        ::True: Inserted
        ::Flase: Not inserted


        """

        if await self.collection.find_one({key: data.get(key)}):
            return False

        await self.collection.insert_one(data)

        return True
