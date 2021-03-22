## Install
* Install python3.5 or latter
* Install mongodb and run mongodb
* pip install -r requirements.txt

## Run
 python run.py runserver


## API
* curl -d '{ "collection":"people",
            "schema": {"firstname":{"type":"string","minlength":1,"maxlength":10},"lastname":{"type":"string","minlength":1,"maxlength":15,"required":true,"unique":true}}}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/create_collection
* curl -d '{"firstname": "barack", "lastname": "obama"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/people
* curl -d '[{"firstname": "barack", "lastname": "obama"}, {"firstname": "mitt", "lastname": "romney"}]' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/db/col/people
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?where=lastname=="obama"
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?sort=-lastname
* curl -i http://127.0.0.1:5000/api/v1/db/col/people?max_results=1&page=1
* curl -i curl -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X PATCH -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37 -d '{"firstname": "ronald"}'
* curl -i curl -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X PUT -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37 -d '{"firstname": "ronald"}'
* curl -i curl -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -H "Content-Type: application/json" -X DELETE -i http://127.0.0.1/api/v1/db/col/people/50adfa4038345b1049c88a37

