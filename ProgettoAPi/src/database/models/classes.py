from database.models import Database
from typing import Any

class Class(Database):
    def __init__(self, collection):
        super().__init__(collection)

    async def get(self, name: str, query: str) -> bool | dict | Any:
        data = await self.collection.find_one({"name": name})

        if data is None:
            return False

        return data.get(query)

    async def get_all_summaries(self) -> list[dict[str, Any]]:
        cursor = self.collection.find({}, {"_id": 0, "name": 1, "students": 1})
        docs = await cursor.to_list(length=None)

        return [
            {
                "id": class_doc["name"],
                "name": class_doc["name"],
                "students": len(class_doc.get("students", [])),
            }
            for class_doc in docs
        ]
