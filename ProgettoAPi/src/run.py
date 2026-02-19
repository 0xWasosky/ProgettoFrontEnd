from app import api

if __name__ == "__main__":
    api.debug = True

    api.run("127.0.0.1")
