from motor.motor_asyncio import AsyncIOMotorClient
from database import Database, Class


database_client = AsyncIOMotorClient("mongodb://localhost:27017/")
database = database_client["Progetto_API"]
user_collection = database["test"]
classes_collection = database["classes"]

user_db = Database(user_collection)
classes_db = Class(classes_collection)

TTL = 100 * 60


SECRET = b"\xc5e\xd6\xa44\xaa\xbaV\xce\x00\xab\xe4\x7f\xa2+;\xb9\xab\x9f\x95\xac6\xad\xe5\x87x\xcb\x01]\xf8\xcc5uk\xa9~N\xbel\x13\xd5\xc9\xdeC9\xbd +skaG\xdf*\xb0\xbdfm'\xf6\xf7\xae\xc8\xd4q'\xac\xea\x86\xa3(\r\xa3&\xd7+laM\x0f\xdf\x94\xe0\":\x03\xba\xd9\xdd\xed\n\x9d\x8d\xb5\xd0^\x93\xf3-zs\xb3\xd4\xd6jj{\xe9\x80\x9e<k\xba\x8di\xb1\x9c,\xe1\x8f1\x0c!\xf5\x82\x89o\\"
COOKIE_TTL = 9 * 60

ADMIN_PWD = "eqvU148VnKHornxdmaUX08ElRsj6tDkVMqpUksf4qdM"
IMAGE_PWD = "ZaE86wpZMl8lAjpMI7yezFaSNIUv4yS84LzWoEOdcPI"


print("Database loaded with success")
