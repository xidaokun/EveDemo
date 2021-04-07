Plan to design a general storage system that does not include specific scenario requirement logic. This part of the content can be implemented in client or middleware; this system should have modules: 
* 1. Registration/Login/OAuth authorization 
* 2.file, database Storage 
* 3. DCL permission control 
* 4. Paid mode 
* 5. Can be backed up to mainstream cloud disks such as google drive or one drive through Rclone


## Run
./run.sh start


## APIS

### Login
* curl -d '{"name":"cary", "password":"123456"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/register
* curl -d '{"name":"cary", "password":"123456"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/login

### File operation
* curl -H "If-Match: token bf2ef95c-948a-11eb-a5be-645aedeb0763" http://127.0.0.1:5000/api/v1/file/upload/test.txt
* curl -i -H "If-Match: token bf2ef95c-948a-11eb-a5be-645aedeb0763" http://127.0.0.1:5000/api/v1/file/download/test.txt
* curl -i -H "If-Match: token bf2ef95c-948a-11eb-a5be-645aedeb0763" http://127.0.0.1:5000/api/v1/file/list
* curl -i -H "If-Match: token bf2ef95c-948a-11eb-a5be-645aedeb0763" http://127.0.0.1:5000/api/v1/file/information
* curl -d -d '{"file":"test.txt"}' -H "If-Match: token bf2ef95c-948a-11eb-a5be-645aedeb0763" -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/file/delete

### Database operation
* curl -d '{ "collection":"people",
            "schema": {"firstname":{"type":"string","minlength":1,"maxlength":10},"lastname":{"type":"string","minlength":1,"maxlength":15,"required":true,"unique":true}}}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/create_collection
* curl -d '{"firstname": "barack", "lastname": "obama"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/people
* curl -d '[{"firstname": "barack", "lastname": "obama"}, {"firstname": "mitt", "lastname": "romney"}]' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/col/people
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?where=lastname=="obama"
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?sort=-lastname
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?max_results=1&page=1
* curl -i -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X PATCH -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37 -d '{"firstname": "ronald"}'
* curl -i -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X PUT -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37 -d '{"firstname": "ronald"}'
* curl -i -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X DELETE -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37

###  operation