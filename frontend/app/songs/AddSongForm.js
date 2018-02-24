import { h } from 'preact';
import { connect } from 'preact-redux';
import PropTypes from 'prop-types';
import { bindActions } from '../util';

import * as actions from './actions';

function AddSongForm({ project, addSong }) {
	const submitForm = (event) => {
		const form = event.target;
		addSong(form.title.value, project);
		form.reset();
		event.preventDefault();
	};

	return (
		<form action="#" className="add-song" onSubmit={submitForm}>
			<input type="text" name="title" required />
			<input type="submit" value="Add Song" />
		</form>
	);
}

AddSongForm.propTypes = {
	project: PropTypes.object.isRequired,
	addSong: PropTypes.func.isRequired,
};

export default connect(null, bindActions(actions))(AddSongForm);
