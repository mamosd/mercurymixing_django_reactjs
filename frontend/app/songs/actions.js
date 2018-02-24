import api from '../api';

import {
	SONG_POST_START, SONG_POST_SUCCESS, SONG_POST_ERROR,
	SONG_DELETE_START, SONG_DELETE_SUCCESS, SONG_DELETE_ERROR,
} from './reducers';

export function addSong(title, project) {
	const song = {
		project: project.id,
		title,
	};
	return api('songs')
		.post(song, SONG_POST_START, SONG_POST_SUCCESS, SONG_POST_ERROR);
}

export function removeSong(song) {
	return api(`songs/${song.id}`)
		.delete(song, SONG_DELETE_START, SONG_DELETE_SUCCESS, SONG_DELETE_ERROR);
}
