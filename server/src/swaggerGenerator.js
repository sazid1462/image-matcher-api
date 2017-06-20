const HapiSwagger = require('hapi-swagger');
const Inert = require('inert');
const Vision = require('vision');
const Blipp = require('blipp');
const Good = require('good');

const options = {
  info: {
    title: 'Image Matcher Documentation',
    version: '1.0.0',
  },
};

const goodOption = {
  ops: {
    interval: 1000,
  },
  reporters: {
    konsole: [
      {
        module: 'good-squeeze',
        name: 'Squeeze',
        args: [
          {
            log: '*',
            response: '*',
          },
        ],
      }, {
        module: 'good-console',
      },
      'stdout',
    ],
  },
};

module.exports = [
  Inert,
  Vision,
  {
    register: HapiSwagger,
    options,
  },
  Blipp,
  {
    register: Good,
    options: goodOption,
  },
];
