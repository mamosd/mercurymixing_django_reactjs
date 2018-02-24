import { h } from 'preact';
import { connect } from 'preact-redux';
import PropTypes from 'prop-types';
import { bindActions, fileSize, getClassName, deepGet } from '../util';
import * as actions from './actions';

function Track({ track, removeTrack, cancelTrack }) {
	const { request } = track;

	const status = () => {
		if (typeof request === 'undefined') return null;
		if (request.error) {
			return deepGet(
			request, 'errorResponse.detail', 'An error occurred');
		}
		if (request.canceled) return 'Canceled';
		if (request.deleting) return 'Deleting...';
		if (request.posting) {
			if (request.progress === null) {
				return (
					<div className="indeterminate progress">
						<progress />
						<span>Uploading...</span>
					</div>
				);
			}

			let msg = 'Waiting...';
			if (request.progress > 0) msg = `${(request.progress * 100).toFixed(1)}%`;
			if (request.progress === 1) msg = 'Saving...';

			return (
				<div className="determinate progress">
					<progress value={request.progress} />
					<span>{msg}</span>
				</div>
			);
		}
		return null;
	};

	const deleteButton = () => {
		if (typeof request !== 'undefined') {
			if (request.canceled || request.error || request.deleting) return null;
			if (request.posting) {
				return (
					<button className="cancel" onClick={() => cancelTrack(track)}>
						<span>Cancel</span>
					</button>
				);
			}
		}
		return (
			<button className="delete" onClick={() => removeTrack(track)}>
				<span>Delete</span>
			</button>
		);
	};

	return (
		<div className={getClassName(track, 'track')}>
			<div className="name">{track.file.name}</div>
			<div className="size">{fileSize(track.file.size)}</div>
			<div className="status">{status()}</div>
			{deleteButton()}
		</div>
	);
}

Track.propTypes = {
	track: PropTypes.object.isRequired,
	removeTrack: PropTypes.func.isRequired,
	cancelTrack: PropTypes.func.isRequired,
};

export default connect(null, bindActions(actions))(Track);
