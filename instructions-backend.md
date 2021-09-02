## Instructions

You can find the DeepArmor React Challenge at https://github.com/sparkcognition/da-react-challenge
 
### Setup
If you are a Django/Python developer, the project should look somewhat familiar to you - to run it, create a virtual env with Python 3.8, and install the requirements in requirements.txt.

If you are a coming from another background, refer to Django's official docs: https://docs.djangoproject.com/en/3.2/intro/install/
You should be able to use any Python version, but 3.8 is what the challenge was created with. Make sure to install the dependencies in `requirements.txt`

You can use the default, SQL-Lite database for dev purposes - it will get automatically created during the migrate command

From `./lyrics_api` directory:
```
python manage.py migrate
python manage.py runserver
```

### Description
The backend is a simple API for searching and storing lyrics.  The lyrics should have an album, song, and the text of the lyrics. The API supports paging, filtering, sorting.

### Your Task:
There is a lot here, but don't think you have to have it all done - just do as much as you can over a couple hours.  We are more interested in how you work than how much you can get done. 

There may also be bugs in the existing code - our production code is not bug-free either! If you find a bug, feel free to fix it. If you want to make an improvement not explicitly listed, go ahead! For example, if you think the models needs some additional fields to be more useful, feel free to add them.

The details of the implementation are often intentionally vague (see, voting).  Part of the task is to decide what **you** think is the best way to implement the functionality.

That said, these are the main tasks we would like to see completed:

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
	  
   - Add new URL to fetch a random lyric
      - Allow an optional artist filter
	  
   - Include relevant migrations, tests, and error handling
   - Swagger should reflect any changes made to API	
	

### What We're Looking For
   - Clean Code with good structure
   - Functionality
   - Good user experience
   - Maintability
   - Reusability
   - Comments



