import { h } from 'preact';
import PropTypes from 'prop-types';
import { getClassName, getStatus, fileSize } from '../util';

function Comment({ comment }) {
	const file = comment.attachment;

	const attachmentLink = () => {
		if (!(file && file.name)) return null;
		return (
			<div className="attachment-info">
				{file.url ? <a href={file.url}>{file.name}</a> : file.name}
				<span className="size">({fileSize(file.size)})</span>
			</div>
		);
	};

	return (
		<section className={getClassName(comment, 'comment')}>
			<h4 className="author">{comment.author}</h4>
			<div className="date">{new Date(comment.created).toLocaleString()}</div>
			<div className="status">{getStatus(comment)}</div>
			<p className="content">{comment.content}</p>
			{attachmentLink()}
		</section>
	);
}

Comment.propTypes = {
	comment: PropTypes.object.isRequired,
};

export default Comment;
