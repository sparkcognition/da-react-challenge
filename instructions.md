## Instructions

You can find the DeepArmor React Challenge at https://github.com/sparkcognition/da-react-challenge
- Clone the repo
- Setup has two options:
	- Docker Compose
		- Simply run "docker-compose up" from the da-react-challenge directory - this should bring up the backend and setup the database automatically, exposing the server on port 8000
	- Manual
		- Follow the instructions in the readme

You'll also need to setup the React application(under lyrics_api/swift-lyrics-react) - Instructions are also in the readme, and the default React readme included in the project

### API Description
The backend is a simple API for searching and storing lyrics.  The lyrics should have an album, song, and the text of the lyrics. The API supports paging, filtering, sorting.

The current frontend app is minimal - it is a basic React app, with a few dependencies, mainly bootstrap.

### Your Task:
- FRONTEND
   - Wire up the table (currently has 2 hard-coded lyrics) to fetch data from the API, with page size defaulting to 25, but toggleable to 10 or 50;
   - Search box - query parameter 'search' will search text in song name, album name, or lyric text
   - Sorting - Allow sorting by song name, album name, or lyric text
   - Implement a Delete button for lyrics.
   - Add a form for submitting new lyrics, including the album, song, and text. Album and song are required fields.
   - Add upvote/downvote functionality to backend API
   - Implement upvote/downvote - one per lyric (can't be fully blocked with just frontend, but just as best as you can)
	
- BACKEND
   - Add lyrics upvote/downvote functionality to backend
      - Lyrics can be upvoted/downvoted by lyric ID
      - Include upvote/downvote count on the lyrics serializers
	   
   - Make album creation separate from Lyric creation
      - Add year to album model (year is required on create, but existing albums can be null)
	  - Name must be unique	to artist
	  - Year, name and artist all required - return appropriate HTTP error code when not included
	  - Change lyric creation to require ID of an already existing album
	  
   - Add support for other artists
      - An artist has:
	     - Name 
	   	 - First year active (optional) 
	  - API for
	     - Create, Delete, List, Update, and Get by ID
		 - List artists should be:
		    - sortable by first year active or name, ascending or descending,
		    - filterable by year active greater than or less than a provided year
		 - Delete should delete any child model objects (album,song,lyrics)
		 - List artists should have id, name, first year active in response
		 - Get by id should include list of albums(name, id)
		 - Album serializer should include artist
	  - Existing lyrics should have Taylor Swift with first year active as 2004
	  
   - Add endpoint to fetch a random lyric
      - Should be optionally filtered by artist
	  
   - Include relevant migrations, tests, and error handling
   - Swagger should reflect any changes made to API	
	

### What We're Looking For
   - Clean Code with good structure
   - Functionality
   - Good user experience
   - Maintability
   - Reusability
   - Comments



