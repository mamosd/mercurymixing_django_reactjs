const autoprefixer = require('autoprefixer');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const path = require('path');
const webpack = require('webpack');

const ENV = process.env.NODE_ENV || 'development';
const PORT = process.env.PORT || 8080;
const IS_DEV = ENV !== 'production';

const styleConfig = [
	{
		loader: 'css-loader',
		options: { sourceMap: IS_DEV },
	},
	{
		loader: 'postcss-loader',
		options: {
			sourceMap: IS_DEV,
			plugins: () => [
				autoprefixer(), // See browserslist file
			],
		},
	},
	{
		loader: 'sass-loader',
		options: { sourceMap: IS_DEV, sourceMapContents: IS_DEV },
	},
];

const devPlugins = [];

const prodPlugins = [
	new webpack.LoaderOptionsPlugin({
		minimize: true,
		debug: false,
	}),
	new webpack.optimize.UglifyJsPlugin(),
];

module.exports = {
	entry: {
		mixing: './app/index.js',
		classic: './classic/index.js',
	},

	output: {
		filename: '[name].js',
		path: path.resolve(__dirname, './build'),
		publicPath: IS_DEV ? `http://localhost:${PORT}/` : '/',
	},

	resolve: {
		alias: {
			react: 'preact-compat',
			'react-dom': 'preact-compat',
		},
	},

	module: {
		rules: [
			{
				test: /\.jsx?$/,
				exclude: /node_modules/,
				// See .babelrc and .eslintrc.js
				use: ['babel-loader', 'eslint-loader'],
			},
			{
				test: /\.s?css$/,
				use: ExtractTextPlugin.extract({
					fallback: 'style-loader',
					use: styleConfig,
				}),
			},
			{
				test: /\.json$/,
				loader: 'json-loader',
			},
			{
				test: /\.(xml|html|txt|md)$/,
				loader: 'raw-loader',
			},
			{
				test: /\.(svg|woff2?|ttf|eot|jpe?g|png|gif)(\?.*)?$/i,
				loader: 'file-loader',
			},
		],
	},

	plugins: ([
		new webpack.NoEmitOnErrorsPlugin(),
		new webpack.NamedModulesPlugin(),
		new ExtractTextPlugin({
			filename: '[name].css',
			allChunks: true,
			disable: IS_DEV,
		}),
		new webpack.EnvironmentPlugin({ NODE_ENV: ENV }),
	]).concat(IS_DEV ? devPlugins : prodPlugins),

	devtool: IS_DEV ? 'inline-source-map' : 'source-map',

	stats: IS_DEV ? 'errors-only' : {
		hash: false,
		version: false,
		timings: false,
		assets: true,
		entrypoints: false,
		chunks: false,
		chunkModules: false,
		modules: false,
		reasons: false,
		depth: false,
		usedExports: false,
		providedExports: false,
		children: false,
		source: false,
		errors: true,
		errorDetails: true,
		warnings: true,
		publicPath: false,
		performance: false,
	},

	devServer: {
		port: PORT,
		host: '0.0.0.0',
		stats: 'errors-only',
		publicPath: '/',
		contentBase: './src',
		historyApiFallback: true,
		headers: {
			'Access-Control-Allow-Origin': '*',
		},
	},
};
