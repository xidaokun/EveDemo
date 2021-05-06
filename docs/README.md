Plan to design a general storage system that does not include specific scenario requirement logic. This part of the content can be implemented in client or middleware; this system should have modules: 
* 1.Registration/Login/OAuth authorization 
* 2.file, database Storage 
* 3.DCL permission control 
* 4.Paid mode 
* 5.Can be backed up to mainstream cloud disks such as google drive or one drive through Rclone

>Tip: the project uses JWT based authentication mechanism


## Run
./run.sh start


## APIS

### User manager
1.register user
>curl -d '{"name":"cary", "password":"123456"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/user/register

> {
"_status": "OK"
}

2.user login
>curl -d '{"name":"cary", "password":"123456"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/user/login

> {
"_status": "OK",
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiYWNrZW5kIiwiaWF0IjoxNjE5NzA1MTg2LCJleHAiOjE2MTk3MDU0ODYsImF1ZCI6ImNsaWVudCIsInN1YiI6IjYwOGFiZDFjOWYzOTRmN2Q3ZjAxOWY5NSIsIm5hbWUiOiJjYXJ5Iiwic2NvcGVzIjpbIm9wZW4iXX0.3wirR5I5UCUDmuCi96adm3SctPEOFPYQKf9gcAF9Ib8",
"user_id": "608abd1c9f394f7d7f019f95",
"user_name": "cary"
}

3.change password
>curl -d '{"password":"12345"}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/user/change_pwd

### OAuth
>curl http://127.0.0.1:5000/api/v1/user/oauth?code=your_access_code&type=github&redirect_uri=http://example.com&state=xyz

> {
"_status": "OK",
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiYWNrZW5kIiwiaWF0IjoxNjE5NzA1MTg2LCJleHAiOjE2MTk3MDU0ODYsImF1ZCI6ImNsaWVudCIsInN1YiI6IjYwOGFiZDFjOWYzOTRmN2Q3ZjAxOWY5NSIsIm5hbWUiOiJjYXJ5Iiwic2NvcGVzIjpbIm9wZW4iXX0.3wirR5I5UCUDmuCi96adm3SctPEOFPYQKf9gcAF9Ib8",
"user_id": "608abd1c9f394f7d7f019f95",
"user_name": "cary"
}

### File operation
1.upload file
>curl -H "If-Match: token JWT_TOKEN" http://127.0.0.1:5000/api/v1/file/upload/test.txt

2.download file
>curl -i -H "If-Match: token JWT_TOKEN" http://127.0.0.1:5000/api/v1/file/download?path=test.txt

3.list files
>curl -i -H "If-Match: token JWT_TOKEN" http://127.0.0.1:5000/api/v1/file/list

4.get file information
>curl -i -H "If-Match: token JWT_TOKEN" http://127.0.0.1:5000/api/v1/file/information

5.delete file
>curl -d '{"file":"test.txt"}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/file/delete

### Database operation
1.create collection
>curl -d '{"collection":"workers"}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/create_col

2.insert one/many document
>curl -d '{"collection":"workers","document":{"worker":"cary","title":"developer"},"options":{"bypass_document_validation":false}}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/insert_one

3.update one/many document
>curl -d '{"collection":"workers","filter":{"worker":"cary",},"update":{"$set":{"author":"cary","title":"manger"}},"options":{"upsert":true,"bypass_document_validation":false}}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/update_one

4.count documents
>curl -d '{"collection":"workers","filter":{"worker":"cary",},"options":{"skip":0,"limit":10,"maxTimeMS":1000000000}}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/count_documents

5.delete one/many documents
>curl -d '{"collection":"workers","filter":{"worker":"cary",}}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/delete_one

6.delete collection
>curl -d '{"collection":"workers"}' -H "If-Match: token JWT_TOKEN" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/delete_col


#### TODO
* CORS
* SMS service
* Docker deployment
* FFmpeg
* Message push mechanism
* Safety considerations

