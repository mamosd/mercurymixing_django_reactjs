import { combineReducers } from 'redux';
import reduceReducers from 'reduce-reducers';

import profileReducer from './project/reducers';
import groups from './groups/reducers';
import songs from './songs/reducers';
import tracks from './tracks/reducers';
import comments from './comments/reducers';

const dummyReducer = (state = {}) => state;

/**
 * Root reducer
 * `reduceReducers` will simply combine all TOP-LEVEL reducers
 * while `combineReducers` lets us create slice reducers for specific
 * collections in Redux's store.
 *
 * In other words, top-level reducers that need access to multiple
 * collections should be added as top-level arguments, while slice
 * reducers that only access one collection should be added as arguments
 * of `combineReducers`.
 */
export default reduceReducers(
	profileReducer,
	combineReducers({
		songs,
		groups,
		tracks,
		comments,
		profile: dummyReducer,
		project: dummyReducer,
	}),
);
