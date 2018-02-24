import api from '../api';

import {
	TRACK_POST_START, TRACK_POST_SUCCESS, TRACK_POST_ERROR,
	TRACK_POST_PROGRESS, TRACK_POST_CANCEL,
	TRACK_DELETE_START, TRACK_DELETE_SUCCESS, TRACK_DELETE_ERROR,
} from './reducers';

export function addTrack(file, group) {
	const track = {
		group: group.id,
		file,
	};
	return api('tracks')
		.post(track, TRACK_POST_START, TRACK_POST_SUCCESS, TRACK_POST_ERROR, TRACK_POST_PROGRESS);
}

export function cancelTrack(track) {
	track.xhr.abort();
	return { type: TRACK_POST_CANCEL, key: track.key };
}

export function removeTrack(track) {
	return api(`tracks/${track.id}`)
		.delete(track, TRACK_DELETE_START, TRACK_DELETE_SUCCESS, TRACK_DELETE_ERROR);
}
