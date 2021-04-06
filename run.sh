#!/usr/bin/env bash

function start() {
  echo "Running backend..."
  ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
  setup_env
  python manage.py runserver
}

function tests() {
  pytest --disable-pytest-warnings -xs tests/login_test.py
  pytest --disable-pytest-warnings -xs tests/file_test.py
  pytest --disable-pytest-warnings -xs tests/database_test.py
}


function setup_env () {
    case `uname` in
    Linux )
        #virtualenv -p `which python3.6` .venv
        python3 -m venv .venv
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        ;;
    Darwin )
        #virtualenv -p `which python3.7` .venv
        python3 -m venv .venv
        source .venv/bin/activate
        pip install --upgrade pip
        pip install --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" -r requirements.txt
        ;;
    *)
    exit 1
    ;;
    esac
}

case "$1" in
    start)
      start
      ;;
    test)
      tests
      ;;
    *)
      echo "Help: run.sh {start|test}"
    exit 1
esac