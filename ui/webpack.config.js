const path = require('path');
const webpack = require('webpack');
const fs = require('fs');


module.exports = env => ({
  mode: (env && env.prod) ? 'production' : 'development',
  entry: {
    app: [
      'babel-polyfill',
      './src/index.jsx',
    ]
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '../static/dist')
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
            plugins: ['@babel/plugin-proposal-class-properties'],
          }
        }
      }
    ]
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /node_modules/,
					chunks: 'initial',
					name: 'vendor',
					priority: 10,
					enforce: true
        },
      },
    },
  },
  plugins: [
    {
      apply: (compiler) => {
        compiler.hooks.afterEmit.tap('AfterEmitPlugin', (compilation) => {
          let tpl = fs.readFileSync('./index.tpl', 'utf8');
          compilation.chunks.forEach(chunk => {
            let hash = chunk.hash.substring(0, 8);
            chunk.files.forEach(filename => {
              switch (filename) {
                case 'app.js':
                  tpl = tpl.replace('{app}', `${filename}?${hash}`);
                  break;
                case 'vendor.js':
                  tpl = tpl.replace('{vendor}', `${filename}?${hash}`);
              }
            });
          });
          fs.writeFile('../templates/index.html', tpl, 'utf8', err => err && console.log);
        });
      }
    },
    new webpack.DefinePlugin({
      VERSION: JSON.stringify(require('./package.json').version),
    }),
  ],
});
