#questo è solo uno script di debug serve per capire se i token e gli id
# degli utenti vengono creati e letti correttamente

#Lo puoi prendere e buttare nel cestino se ti va ahahah
import asyncio
from core import user_db, SECRET
from _libs.Jwt import encode_jwt
import datetime

username = input("Inserire il nome dell'utente: ")
password = input("Inserire la password: ")

async def test_login(username, password):
    user = await user_db.get(username=username, password=password)
    if not user:
        print("Utente non trovato o password errata")
        return

    user_id = user.get("id")
    print("ID utente trovato:", user_id)

    token_payload = {
        "id": user_id,
        "exp": int((datetime.datetime.now() + datetime.timedelta(minutes=6)).timestamp()),
    }

    token = await encode_jwt(payload=token_payload, secret=SECRET)
    print("JWT generato:", token)

# Usa le variabili che arrivano dall'input
asyncio.run(test_login(username, password))