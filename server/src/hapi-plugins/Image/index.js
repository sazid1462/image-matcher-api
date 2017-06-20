const Routes = require('./routes');

exports.register = (server, option, next) => {
  server.route(Routes);
  next();
};

exports.register.attributes = {
  name: 'Image',
  version: '1.0.0',
};
