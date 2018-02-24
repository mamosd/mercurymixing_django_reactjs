import { h, render } from 'preact';
import { Provider } from 'preact-redux';
import configureStore from './store';
import Project from './project/Project';

// Hot reloading and dev tools
if (module.hot) {
	module.hot.accept();
	require('preact/devtools'); // eslint-disable-line global-require
}

const rootNode = document.querySelector('#root');

render((
	<Provider store={configureStore()}>
		<Project />
	</Provider>
), rootNode, rootNode.firstElementChild);
