## Instructions

[Backend](instructions-backend.md)

[Frontend](instructions-frontend.md)


### Documentation
   - With the server running, navigate to `http://localhost:8000/swiftlyrics/swagger/` to view API documenation
   - ** please note that POST lyrics does not include `song.id` in the documentation, but you can use the ID of the song instead of the name. Same goes for Album.  
       - ID takes precedence if name and ID are included. If song id is included, album is ignored
   - You can also see the responses to GET requests in browser by going to the url:
      - For example, `http://localhost:8000/swiftlyrics/album/`
     
### Troubleshooting
  - To delete database, remove `db.sqlite3` and re-run the `migrate` command
    
