import { createStore, compose, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';
import { getKey } from './api';
import { updateDOM, deepGet } from './util';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const ENHANCERS = composeEnhancers(applyMiddleware(thunk));

const EMPTY = {
	project: {},
	profile: {},
	songs: [],
	groups: [],
	tracks: [],
	comments: [],
};

// window.initialState is populated by Django in mixing/project_detail.html
const INITIAL = window.initialState || EMPTY;

// All initial elements should have a 'key' property to keep track of them in the UI
// Yes, we're mutating the initial state because we havent initialized the store yet
['songs', 'groups', 'tracks', 'comments'].forEach(key => {
	INITIAL[key] = INITIAL[key].map(obj => {
		if (!('key' in obj)) obj.key = getKey();
		return obj;
	});
});

/**
 * Callback to be executed when a Redux action is dispatched.
 * @param  {Object} state The Redux state object
 */
function onActionDispatch(state) {
	updateDOM('.track-credit-display', deepGet(state, 'profile.trackCredit'));
}

/**
 * Wire up the Redux store with the reducers, subscribers, and enhancers.
 * @return {Store} The configured Redux store
 */
export default function configureStore() {
	const store = createStore(rootReducer, INITIAL, ENHANCERS);

	store.subscribe(() => onActionDispatch(store.getState()));

	if (module.hot) {
		// Enable Webpack hot module replacement for reducers
		module.hot.accept('./reducers', () => {
			// eslint-disable-next-line global-require
			const nextRootReducer = require('./reducers').default;
			store.replaceReducer(nextRootReducer);
		});
	}

	return store;
}
