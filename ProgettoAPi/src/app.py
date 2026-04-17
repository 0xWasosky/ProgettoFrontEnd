import datetime
from quart import Quart
from quart_rate_limiter import RateLimiter, rate_limit
from quart_cors import cors


from blueprints import auth, user, files, classes, admin


api = Quart(__name__)


api = cors(
    api,
    allow_origin=["http://localhost:5173", "http://127.0.0.1:5173"],    #Ho trovato una funzione da frontend che permette di calcolare
    allow_credentials=True,                                             #facilmente il dominio del server solo che aveva bisogno di entrambe le scritture
)

api.register_blueprint(auth)
api.register_blueprint(user)
api.register_blueprint(files)
api.register_blueprint(classes)
api.register_blueprint(admin)

rate_limiter = RateLimiter(api)


@api.route("/")
@api.route("/index")
@rate_limit(20, datetime.timedelta(minutes=3))
def index():
    return "Hey there, this is the index page of the API"
