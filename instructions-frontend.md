

## Instructions
You can find the DeepArmor React Challenge at https://github.com/sparkcognition/da-react-challenge

### Prereqs
- Node

### Setup
- Navigate to `lyrics_api/swift-lyrics-react` directory
- Install dependencies with  `npm install`
- Start application with `npm start`
- Open http://localhost:3000/ in browser

### Description
The backend is a simple API for searching and storing lyrics.  The lyrics should have an album, song, and the text of the lyrics. The API supports paging, filtering, sorting.

The current frontend app is minimal - it is a basic React app, with a few dependencies, mainly bootstrap.

Although you can run the API locally if you prefer, it is deployed for your convenience at https://da-react-challenge.herokuapp.com/health

To see the full documentation, navigate to https://da-react-challenge.herokuapp.com/swiftlyrics/swagger/

### Your Task:
For frontend-only positions, aim to complete the first 5 bullet points.  
This is a fairly open-ended challenge - feel free to make any styling or design changes, as long as the requirements can be met.  

This is **your** opportunity to show us what you can do, so if you have an idea that you think would make the application better, go for it!

That said, these are the main tasks we would like to see completed:

   - Wire up the table (currently has 2 hard-coded lyrics) to fetch data from the API, with page size defaulting to 25, but toggleable to 10 or 50;
   - Add a text search box - use query parameter `search` to filter by text in song name, album name, or lyric text
   - Sorting - Allow sorting by song name, album name, or lyric text
   - Implement a Delete button for lyrics which calls the API to delete the lyric
   - Add a form for submitting new lyrics, including the album, song, and text. Album and song are required fields.  This should submit to the API. 
   - Add upvote/downvote functionality to backend API 
   - Implement upvote/downvote - one per lyric (can't be fully blocked with just frontend, but just as best as you can)
	

### What We're Looking For
   - Clean Code with good structure
   - Functionality
   - Good user experience
   - Maintability
   - Reusability
   - Comments
   
