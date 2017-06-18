const Hapi = require('hapi');

const routePlugins = require('./hapi-plugins');
const hapiPlugins = require('./swaggerGenerator');

const server = new Hapi.Server();
server.connection({
  port: 4000,
});

server.register(hapiPlugins, (err) => {
  if (err) {
    console.log('Plugin load error');
    throw err;
  } else {
    console.log('plugin loaded');
  }
});


server.register(routePlugins, (err) => {
  if (err) {
    console.log('Routes load error');
    throw err;
  } else {
    console.log('Routes loaded');
  }
});

server.start((err) => {
  if (err) {
    console.log('server start error');
    throw err;
  } else {
    console.log('server started at ', server.info.uri);
  }
});
