type Artist = {
  id: any
  first_year_active: any
  name: any
}

type Album = {
  id: any
  name: any
  year: any
}

type Song = {
  id: any
  name: any
}

type Lyric = {
  id: any
  song: Song
  album: Album
  artist: Artist
}

export type {Artist, Album, Song, Lyric}