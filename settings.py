import os.path

from os.path import join, dirname
from dotenv import load_dotenv

# absolute path to the location of ..env on remote server.
enviroment = "/home/gallochri/gallobot_env"


if os.path.isfile(".env"):
    dotenv_path = join(dirname(__file__), '.env')
    print("Local .env")
else:
    dotenv_path = enviroment
    print("Remote .env")

load_dotenv(dotenv_path, verbose=True)
