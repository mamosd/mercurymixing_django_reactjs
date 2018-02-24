import reducerFactory from '../reducerFactory';

export const TRACK_POST_START = 'TRACK_POST_START';
export const TRACK_POST_SUCCESS = 'TRACK_POST_SUCCESS';
export const TRACK_POST_ERROR = 'TRACK_POST_ERROR';
export const TRACK_POST_PROGRESS = 'TRACK_POST_PROGRESS';
export const TRACK_POST_CANCEL = 'TRACK_POST_CANCEL';

export const TRACK_DELETE_START = 'TRACK_DELETE_START';
export const TRACK_DELETE_SUCCESS = 'TRACK_DELETE_SUCCESS';
export const TRACK_DELETE_ERROR = 'TRACK_DELETE_ERROR';

export default reducerFactory('TRACK');
