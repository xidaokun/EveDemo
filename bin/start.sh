
function start_main() {

}

function start_test() {

}

function setup_env() {
    case `uname` in
    Linux )
      virtualenv -p `which python3.6` env
      source env/bin/activate
      pip install --upgrade pip
      pip install -r requirements.txt
      ;;
    Darwin )
      virtualenv -p `which python3.7` env
        source env/bin/activate
        pip install --upgrade pip
        pip install --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" -r requirements.txt
        ;;
      * )
        exit 1
        ;;
    esac

}

case "$1" in
    main)
        start_main
        ;;
    test)
        start_test
        ;;
    *)
    echo "Usage: run.sh {docker|direct|test}"
    exit 1
esac