import Cookies from 'js-cookie';

export function getKey() {
	return Math.random().toString(36).substring(2);
}

const apiBase = '/api/';

/**
 * Private API client based on XMLHttpRequest.
 * Dispatches Redux actions before and after the request.
 *
 * @param  {string} url        API endpoint URL
 * @param  {string} method     GET, POST, DELETE, etc...
 * @param  {Object} payload    Payload for the server and Redux actions
 * @param  {function} dispatch Redux's `dispatch` function
 * @param  {string} [START]    Action to be dispatched before the request
 * @param  {string} [SUCCESS]  Action to be dispatched if the request succeeds
 * @param  {string} [ERROR]    Action to be dispatched if the request fails
 * @param  {string} [PROGRESS] Action to be dispatched on request progress
 * @param  {string} [CANCEL]   Action to be dispatched on request abort
 *
 * The START reducer will receive `payload` with an added key of `xhr`, which will be the
 * ongoing XmlHttpRequest. It will also receive a `key`, which will be used to identify
 * the request when other actions are dispatched.
 *
 * The SUCCESS and ERROR reducers will receive: `key` and `response` as action args.
 * `response` will be the server response parsed as JSON (or null if no response).
 *
 * The PROGRESS reducer will receive `key` and `event` as action args. `event` will be
 * the progressEvent triggered by the request.
 *
 * The CANCEL reducer will receive `key` as action args.
 */
function _api(url, method, payload, dispatch, START, SUCCESS, ERROR, PROGRESS, CANCEL) {
	const data = new FormData();
	const xhr = new XMLHttpRequest();
	const key = payload.key || getKey();

	// Create payload
	Object.keys(payload).forEach(name => data.append(name, payload[name]));

	// Remove leading slashes from the url
	if (url.indexOf('/') === 0) url = url.slice(1);

	// Prepend the base API url to all requests
	url = apiBase + url;

	// Make sure urls always have a trailing slash (required by Django)
	if (url.lastIndexOf('/') !== url.length - 1) url += '/';

	// Prepare the request. Tested against Django Rest Framework
	xhr.open(method, url, true);
	xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
	xhr.setRequestHeader('Accept', 'application/json');

	// Async load handler. Determines if response was successful or failed.
	xhr.onload = function apiLoad() {
		let response;
		try {
			response = JSON.parse(xhr.responseText || null);
		} catch (e) {
			response = { detail: 'Could not parse server response' };
		}
		if (xhr.status >= 200 && xhr.status < 300) {
			if (SUCCESS) dispatch({ type: SUCCESS, key, response });
		} else if (ERROR) dispatch({ type: ERROR, key, response });
	};

	// Async error handler (connection error)
	if (ERROR) {
		xhr.onerror = function apiError() {
			dispatch({ type: ERROR, key, response: null });
		};
	}

	// Async progress handler
	if (PROGRESS) {
		xhr.upload.onprogress = function apiProgress(event) {
			dispatch({ type: PROGRESS, key, event });
		};
	}

	// Async cancel handler
	if (CANCEL) {
		xhr.onabort = function apiCancel() {
			dispatch({ type: CANCEL, key });
		};
	}

	// Dispatch the pre-request action
	if (START) dispatch({ type: START, payload: { ...payload, xhr }, key });

	// Send the request to the server
	xhr.send(data);
}

/**
 * Public API client.
 * Provides a set of convenience methods to perform requests.
 * Each method returns a thunk compatible with redux-thunk middleware.
 * @param  {string} url API endpoint URL
 * @return {Object}     Collection of request methods to be executed on the endpoint.
 */
export default function api(url) {
	return {
		// ...actions corresponds to all Redux actions accepted by _api()
		get: function apiGet(payload, ...actions) {
			if (!payload) payload = {};
			return dispatch => _api(url, 'GET', payload, dispatch, ...actions);
		},

		patch: function apiPatch(payload, ...actions) {
			return dispatch => _api(url, 'PATCH', payload, dispatch, ...actions);
		},

		post: function apiPost(payload, ...actions) {
			return dispatch => _api(url, 'POST', payload, dispatch, ...actions);
		},

		put: function apiPut(payload, ...actions) {
			return dispatch => _api(url, 'PUT', payload, dispatch, ...actions);
		},

		delete: function apiDelete(payload, ...actions) {
			return dispatch => _api(url, 'DELETE', payload, dispatch, ...actions);
		},
	};
}

