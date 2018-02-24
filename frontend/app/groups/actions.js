import api from '../api';

import {
	GROUP_POST_START, GROUP_POST_SUCCESS, GROUP_POST_ERROR,
	GROUP_DELETE_START, GROUP_DELETE_SUCCESS, GROUP_DELETE_ERROR,
} from './reducers';

export function addGroup(title, song) {
	const group = {
		song: song.id,
		title,
	};
	return api('groups')
		.post(group, GROUP_POST_START, GROUP_POST_SUCCESS, GROUP_POST_ERROR);
}

export function removeGroup(group) {
	return api(`groups/${group.id}`)
		.delete(group, GROUP_DELETE_START, GROUP_DELETE_SUCCESS, GROUP_DELETE_ERROR);
}
