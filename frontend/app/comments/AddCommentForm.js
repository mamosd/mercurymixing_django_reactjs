import { h } from 'preact';
import { connect } from 'preact-redux';
import PropTypes from 'prop-types';
import { bindActions, stateToProps } from '../util';

import * as actions from './actions';

function AddCommentForm({ project, profile, addComment }) {
	const submitComment = (event) => {
		const { content, attachment } = event.target;
		addComment({
			content: content.value,
			attachment: attachment.files[0],
			author: profile.user,
			project,
		});
		event.target.reset();
		event.preventDefault();
	};

	return (
		<form action="#" className="add-comment" onSubmit={submitComment}>
			<h3>Add a new comment</h3>
			<textarea name="content" cols="30" rows="10" required />
			<input name="attachment" type="file" />
			<input type="submit" value="Add Comment" />
		</form>
	);
}

AddCommentForm.propTypes = {
	project: PropTypes.object.isRequired,
	profile: PropTypes.object.isRequired,
	addComment: PropTypes.func.isRequired,
};

export default connect(stateToProps('profile'), bindActions(actions))(AddCommentForm);
