import reducerFactory from '../reducerFactory';

export const SONG_POST_START = 'SONG_POST_START';
export const SONG_POST_SUCCESS = 'SONG_POST_SUCCESS';
export const SONG_POST_ERROR = 'SONG_POST_ERROR';

export const SONG_DELETE_START = 'SONG_DELETE_START';
export const SONG_DELETE_SUCCESS = 'SONG_DELETE_SUCCESS';
export const SONG_DELETE_ERROR = 'SONG_DELETE_ERROR';

export default reducerFactory('SONG');
