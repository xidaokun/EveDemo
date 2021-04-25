import hashlib
import logging


def create_full_path_dir(path):
    try:
        path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        logging.debug(f"Exception in create_full_path: {e}")
        return False
    return True


def md5_encode(value):
    md5 = hashlib.md5()
    md5.update(value.encode("utf-8"))
    return str(md5.hexdigest())

