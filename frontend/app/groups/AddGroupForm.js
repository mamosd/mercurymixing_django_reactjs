import { h } from 'preact';
import { connect } from 'preact-redux';
import PropTypes from 'prop-types';
import { bindActions } from '../util';

import * as actions from './actions';

function AddGroupForm({ song, addGroup }) {
	const submitGroup = (event) => {
		const form = event.target;
		addGroup(form.title.value, song);
		form.reset();
		event.preventDefault();
	};

	return (
		<form action="#" className="add-group" onSubmit={submitGroup}>
			<input type="text" name="title" required />
			<input type="submit" value="Add Group" />
		</form>
	);
}

AddGroupForm.propTypes = {
	song: PropTypes.object.isRequired,
	addGroup: PropTypes.func.isRequired,
};

export default connect(null, bindActions(actions))(AddGroupForm);
