import os.path

from os.path import join, dirname
from dotenv import load_dotenv

# absolute path to the location of .env on remote server.
remote_env = "/home/gallochri/gallobot_env"

# file to load locally
local_env = ".env_locale"


if os.path.isfile(local_env):
    dotenv_path = join(dirname(__file__), local_env)
else:
    dotenv_path = remote_env

print("Enviroment: " + dotenv_path)
load_dotenv(dotenv_path, verbose=True)
