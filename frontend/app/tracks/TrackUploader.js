import { h } from 'preact';
import { connect } from 'preact-redux';
import Dropzone from 'react-dropzone';
import PropTypes from 'prop-types';
import { stateToProps, bindActions } from '../util';
import * as actions from './actions';

function TrackUploader({ group, profile, addTrack }) {
	const onDrop = (acceptedFiles) => {
		acceptedFiles.forEach((file, i) => {
			if ((profile.trackCredit - i) > 0) addTrack(file, group);
		});
	};

	if (profile.trackCredit <= 0) {
		return (
			<div className="track-uploader disabled">
				<strong>You&apos;re out of track credits</strong>
				<a href={profile.purchaseUrl}>Get more credits</a>
			</div>
		);
	}

	return (
		<Dropzone className="track-uploader" onDrop={onDrop}>
			<div>Drop your tracks here (click to open file browser).</div>
		</Dropzone>
	);
}

TrackUploader.propTypes = {
	group: PropTypes.object.isRequired,
	profile: PropTypes.object.isRequired,
	addTrack: PropTypes.func.isRequired,
};

export default connect(stateToProps('profile'), bindActions(actions))(TrackUploader);
