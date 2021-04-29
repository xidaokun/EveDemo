import os

from flask import request, Response

from main.src.utils.auth import verify_request
from main.src.utils.files import filter_path_root, query_upload_get_filepath, query_download
from main.src.utils.server_response import *


class FilesModule:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponse("File")

    def init_app(self, app):
        self.app = app

    def upload_file(self, file_name):
        logging.debug(f"start upload file.....")
        isvalid = verify_request(request)
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        file_name = filter_path_root(file_name)
        logging.debug(f"file name:" + file_name)
        full_path_name, err = query_upload_get_filepath(file_name)

        try:
            with open(full_path_name, "bw") as f:
                chunk_size = 4096
                while True:
                    chunk = request.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    f.write(chunk)
            os.path.getsize(full_path_name.as_posix())
        except Exception as e:
            return self.response.response_err(500, f"Exception: {str(e)}")

        return self.response.response_ok()

    def download_file(self):
        resp = Response()
        isvalid = verify_request(request)
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        file_name = request.args.get('path')
        data, status_code = query_download(file_name)
        if status_code != 200:
            resp.status_code = status_code
            return resp

        return data

    def list_files(self):
        isvalid, payload = verify_request(request)
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        path = "./files" + "/" + payload['name'] + "/"
        try:
            files = os.listdir(path)
        except Exception as e:
            return self.response.response_ok({"files": []})

        names = [name for name in files
                 if os.path.isfile(os.path.join(path, name))]
        return self.response.response_ok({"files": names})

    def get_file_info(self):
        isvalid, payload = verify_request(request)
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        filename = request.args.get('filename')
        if filename is None:
            return self.response.response_err(401, "file name is null")

        path = "./files" + "/" + payload['name'] + "/"
        file_full_name = path + filename.encode('utf-8').decode('utf-8')
        if not os.path.exists(file_full_name):
            return self.response.response_err(404, "file not found")

        size = os.path.getsize(file_full_name)

        return self.response.response_ok({"file": filename, "size": size})

    def delete_file(self):
        isvalid, payload = verify_request(request)
        if isvalid:
            return self.response.response_err(401, "token is invalid")

        content = request.get_json(force=True, silent=True)
        if content is None:
            return self.response.response_err(400, "parameter is not application/json")
        filename = content.get('file_name', None)

        path = "./files" + "/" + payload['name'] + "/"
        fullname = os.path.join(path, filename)
        if os.path.exists(fullname) and os.path.isfile(fullname):
            os.remove(fullname)
            return self.response.response_ok()
        else:
            return self.response.response_err(404, "File not found")