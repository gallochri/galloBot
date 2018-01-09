#!/bin/sh -xv
GIT_REPO=https://git.gallochri.com/gallochri/galloBot.git
GIT_CLONE=$HOME/bot/galloBot
PYTHON_ENV=$HOME/bot/gallobot_env
APP=${GIT_CLONE}/app.py

kill $(ps aux | grep ${APP} | grep -v grep | awk '{print $2}')

if [ ! -d ${PYTHON_ENV} ]; then
	python3 -m venv ${PYTHON_ENV}
fi

. ${PYTHON_ENV}/bin/activate

if [ -d ${GIT_CLONE} ]; then
	cd ${GIT_CLONE}
	git pull
else
	git clone ${GIT_REPO} ${GIT_CLONE}
fi

pip install -r ${GIT_CLONE}/requirements.txt
python ${APP}
exit
