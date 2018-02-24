import { h } from 'preact';
import { connect } from 'preact-redux';
import PropTypes from 'prop-types';
import { stateToProps } from '../util';

import Song from '../songs/Song';
import AddSongForm from '../songs/AddSongForm';
import Comment from '../comments/Comment';
import AddCommentForm from '../comments/AddCommentForm';

const Project = ({ project, songs, comments }) => (
	<section className={project.active ? 'project active' : 'project inactive'}>
		<section className="songs">
			{songs.map(song => <Song key={song.key} song={song} />)}
		</section>
		<AddSongForm project={project} />
		<section className="comments">
			<h2>Comments {comments.length}</h2>
			{comments.map(cmt => <Comment key={cmt.key} comment={cmt} />)}
		</section>
		<AddCommentForm project={project} />
	</section>
);

Project.propTypes = {
	project: PropTypes.object.isRequired,
	songs: PropTypes.arrayOf(PropTypes.object).isRequired,
	comments: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default connect(stateToProps('project', 'songs', 'comments'))(Project);
