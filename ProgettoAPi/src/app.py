import datetime
from quart import Quart
from quart_rate_limiter import RateLimiter, rate_limit
from quart_cors import cors
import tracemalloc

# Enable tracemalloc
tracemalloc.start()

api = Quart(__name__)

#Aggiunta per poter comunicare con il front-end(premessi per ricevere da un origine)
api = cors(
    api,
    allow_origin="http://localhost:5173",   #Verrà modificato con il dominio del sito
    allow_credentials=True,
)

from blueprints import auth, user, files

api.register_blueprint(auth)
api.register_blueprint(user)
api.register_blueprint(files)

rate_limiter = RateLimiter(api)


@api.route("/")
@api.route("/index")
@rate_limit(20, datetime.timedelta(minutes=3))
def index():
    return "Hey there, this is the index page of the API"
