import React from 'react';

function LyricEntry(props) {
	const lyric = props.lyric;
	
	return (
    	<tr>
    	  <th scope="row">{lyric.id}</th>
    	  <td>{lyric.text}</td>
    	  <td>{lyric.song.name}</td>
    	  <td>{lyric.album.name}</td>
    	  <td>{lyric.artist.name}</td>
    	  <td>Edit</td>
    	  <td>Delete</td>
    	</tr>
	)
}

export default LyricEntry;