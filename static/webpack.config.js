const path = require('path');
const webpack = require('webpack');

module.exports = {
  devtool: "source-map",
  entry: {
    welcome: './app/welcome/welcome.js',
    org: [
      './app/org/index.js'
    ],
    repo: [
      './app/repo/index.js'
    ],
    user: './app/user/index.js',
    vendor: [
      'react',
      'react-dom',
      'prop-types',
      'react-redux',
      'react-router',
      'react-router-redux',
      'redux',
      'redux-thunk',
      'bootstrap',
      'classnames',
      'popper.js',
      'jquery',
      '@fortawesome/react-fontawesome',
      '@fortawesome/fontawesome-free-solid'
    ]
  },
  output: {
    path: path.join(__dirname, 'dist'),
    filename: "[name].entry.js",
    sourceMapFilename: '[file].map'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: {
          loader: 'babel-loader?cacheDirectory=true'
        },
        exclude: /node_modules/,
        include: __dirname
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      filename: 'vendor.bundle.js'
    })
  ]
};