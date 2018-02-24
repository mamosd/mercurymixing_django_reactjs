/**
 * POST request 'start' reducer.
 * Inserts an object in the state and attaches the request information.
 * @param  {Object} state          A key in Redux's store. It's value must be an array.
 * @param  {Object} action         Redux style action
 * @param  {Object} action.payload Contains all the data for the newly inserted object
 * @param  {string} action.key     Unique identifier to keep track of the object in the
 *                                 store when other reducers run.
 * @return {Object}                Resulting state with the inserted object
 */
export const onPostStart = (state, action) => {
	const { key, payload } = action;
	const request = { posting: true, progress: 0 };
	return [...state, { ...payload, key, request }];
};

/**
 * POST request 'success' reducer.
 * Updates an object in the state with the data received from the server.
 * @see    onPostStart
 * @param  {Object} action.key      Unique identifier that was passed to onPostStart
 * @param  {Object} action.response JSON response from the server
 * @return {Object}                 Resulting state with the updated object
 */
export const onPostSuccess = (state, action) => (
	state.map(instance => {
		if (instance.key !== action.key) return instance;
		return {
			...instance,
			...action.response,
			request: {
				...instance.request,
				posting: false,
				progress: 1,
			},
		};
	})
);

/**
 * POST, PUT, and DELETE request 'error' reducer.
 * Updates an object in the state with the error response from the server.
 * @see    onPostStart
 * @param  {Object} action.key      Unique identifier that was passed to on__Start
 * @param  {Object} action.response JSON error response from the server
 * @return {Object}                 Resulting state with the object marked with 'error'
 *                                  and the server's 'errorResponse' attached
 */
export const onPostError = (state, action) => (
	state.map(instance => {
		if (instance.key !== action.key) return instance;
		return {
			...instance,
			request: {
				...instance.request,
				error: true,
				errorResponse: action.response,
			},
		};
	})
);

/**
 * POST, PUT, and DELETE request 'progress' reducer.
 * Updates an object in the state with the current request progress.
 * {@link https://developer.mozilla.org/en/docs/Web/API/ProgressEvent}
 * @see    onPostStart
 * @param  {Object} action.key      Unique identifier that was passed to on__Start
 * @param  {Object} action.event    Object that implements the ProgressEvent interface
 * @return {Object}                 Resulting state with the updated progress
 */
export const onPostProgress = (state, action) => {
	const { event } = action;
	return state.map(instance => {
		let progress = null;
		if (instance.key !== action.key) return instance;
		if (event.lengthComputable) progress = event.loaded / event.total;
		return { ...instance, request: { ...instance.request, progress } };
	});
};

/**
 * POST, PUT, and DELETE request 'cancel' reducer.
 * Updates an object in the state by marking it as 'canceled'.
 * The reducer DOES NOT cancel the request. That's the job of the action creator.
 * @see    onPostStart
 * @param  {Object} action.key      Unique identifier that was passed to on__Start
 * @return {Object}                 The resulting state with the updated object
 */
export const onPostCancel = (state, action) => (
	state.map(instance => {
		if (instance.key !== action.key) return instance;
		return {
			...instance,
			request: { ...instance.request, canceled: true },
		};
	})
);

/**
 * DELETE request 'start' reducer.
 * Updates an object in the state by marking it as 'deleting'.
 * @see    onPostStart
 * @param  {string} action.key      Unique identifier that was passed to onDeleteStart
 * @return {Object}                 The resulting state with the updated object
 */
export const onDeleteStart = (state, action) => (
	state.map(instance => {
		if (instance.key !== action.key) return instance;
		return {
			...instance,
			request: { ...instance.request, deleting: true, progress: 0 },
		};
	})
);

/**
 * DELETE request 'success' reducer.
 * Drops an object from the state.
 * @see    onPostStart
 * @param  {Object} action.key  	Unique identifier that was passed to onDeleteStart
 * @return {Object}                 The resulting state without the dropped object
 */
export const onDeleteSuccess = (state, action) => (
	state.filter(instance => instance.key !== action.key)
);

/**
 * Reducer factory for REST API workflows.
 * Generates a reducer to be composed with `combineReducers`.
 * @param  {string} PREFIX   Will be assigned to all resulting reducers
 * @return {function}        Reducer function with all API actions
 */
export default function reducerFactory(PREFIX) {
	const ACTIONS = {
		[`${PREFIX}_POST_START`]: onPostStart,
		[`${PREFIX}_POST_SUCCESS`]: onPostSuccess,
		[`${PREFIX}_POST_ERROR`]: onPostError,
		[`${PREFIX}_POST_PROGRESS`]: onPostProgress,
		[`${PREFIX}_POST_CANCEL`]: onPostCancel,

		[`${PREFIX}_DELETE_START`]: onDeleteStart,
		[`${PREFIX}_DELETE_SUCCESS`]: onDeleteSuccess,
		[`${PREFIX}_DELETE_ERROR`]: onPostError,
		[`${PREFIX}_DELETE_PROGRESS`]: onPostProgress,
		[`${PREFIX}_DELETE_CANCEL`]: onPostCancel,
	};

	return function objectBasedReducer(state = [], action) {
		if (action && ACTIONS[action.type]) {
			return ACTIONS[action.type](state, action);
		}
		return state;
	};
}
