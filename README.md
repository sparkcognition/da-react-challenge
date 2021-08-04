### Project description:
This repository is part of the application process for SparkCognition.
The changes from the original repository from which this was forked were written, tested and commented by José Carlos Delgado.

   - Postman Collection
      - The Postman Collection for this project can be found in `https://www.getpostman.com/collections/1974be9f9d0872844638`
      and can be also found inside this repository as `da-react-challenge-collection.postman_collection.json`.
      - This collection is meant to be run sequentially.

   - Tests and coverage
      - Tests can be run with the following command (executed from the `lyrics_api` directory):
      `coverage run --source . manage.py test && coverage report`
      The current project has a 100% coverage, results can be seen in the Actions section
      of the repository.

   - Configuration
      - Configuration remains the same as the original project.


### Requirements:
- Prereqs
   - `brew install pyenv`
   - from `da-react-challenge` directory:
      - `pyenv install 3.6.5`
         - Optionally add `eval "$(pyenv init -)"` to `~/.bash_profile`  
      - `pyenv local 3.6.5` 
      - `pip3 install virtualenv`
      - `source ./fresh_venv` to create new virtual environment and install requirements
    
### Project Setup
   - Navigate to `lyrics_api` directory
   - Server  
      - `python manage.py migrate` to setup database
      -  `python manage.py runserver` to start service
   - Frontend
      - Navigate to `swift-lyrics-react` directory
      - `npm install`
      - `npm start`
      - open `http://localhost:3000/` in browser
#### Docker Compose
 You can also use docker compose to run the server
`docker-compose up` from the `da-react-challenge` directory
This is untested, but theoretically should work

### Documentation
   - With the server running, navigate to `http://localhost:8000/swiftlyrics/swagger/` to view API documenation
   - ** please note that POST lyrics does not include `song.id` in the documentation, but you can use the ID of the song instead of the name. Same goes for Album.  
       - ID takes precedence if name and ID are included. If song id is included, album is ignored
   - You can also see the responses to GET requests in browser by going to the url:
      - For example, `http://localhost:8000/swiftlyrics/album/`
     
### Troubleshooting
  - To delete database, remove `db.sqlite3` and re-run the `migrate` command
    
