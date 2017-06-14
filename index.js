'use strict';

const nodeEnv = process.env.NODE_ENV || 'development';
const src = (nodeEnv === 'development') ? 'src' : 'dist';

// Start the hapi-server
require(`./${src}/server`);