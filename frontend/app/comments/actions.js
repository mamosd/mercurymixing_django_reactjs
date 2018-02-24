import api from '../api';

import {
	COMMENT_POST_START, COMMENT_POST_SUCCESS, COMMENT_POST_ERROR,
} from './reducers';

// eslint-disable-next-line import/prefer-default-export
export function addComment({ content, attachment, author, project }) {
	const comment = {
		project: project.id,
		created: new Date(),
		author,
		content,
	};

	// The API will complain if the payload contains an empty `attachment` key,
	// so we only add the key if it will have a value
	if (attachment) comment.attachment = attachment;

	return api('comments')
		.post(comment, COMMENT_POST_START, COMMENT_POST_SUCCESS, COMMENT_POST_ERROR);
}
