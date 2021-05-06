from datetime import datetime
from pathlib import Path

from main.settings import VAULTS_BASE_DIR
from main.src.utils.common import create_full_path_dir
from main.src.utils.flask_rangerequest import RangeRequest


def filter_path_root(name):
    if name[0] == "/":
        return name[1:]
    else:
        return name


def get_save_files_path():
    path = Path(VAULTS_BASE_DIR)
    if path.is_absolute():
        path = path / "files"
    else:
        path = path.resolve() / "files"
    return path.resolve()


def query_upload_get_filepath(file_name):
    err = {}

    path = get_save_files_path()
    full_path_name = (path / file_name).resolve()

    if not create_full_path_dir(full_path_name.parent):
        err["status_code"], err["description"] = 500, "make path dir error"
        return full_path_name, err

    if not full_path_name.exists():
        full_path_name.touch(exist_ok=True)

    if full_path_name.is_dir():
        err["status_code"], err["description"] = 404, "file name is a directory"
        return full_path_name, err

    return full_path_name, err


def query_download(file_name):
    if file_name is None:
        return None, 400
    filename = filter_path_root(file_name)

    path = get_save_files_path()
    file_full_name = (path / filename).resolve()

    if not file_full_name.exists():
        return None, 404

    if not file_full_name.is_file():
        return None, 403

    size = file_full_name.stat().st_size
    with open(file_full_name, 'rb') as f:
        etag = RangeRequest.make_etag(f)
    last_modified = datetime.utcnow()

    return RangeRequest(open(file_full_name, 'rb'),
                        etag=etag,
                        last_modified=last_modified,
                        size=size).make_response(), 200


