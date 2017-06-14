module.exports = [
  {
    method: 'GET',
    path: '/test',
    config: {
      tags: ['api'],
      description: 'Good testing',
      handler: (request, reply) => {
        reply({ status: 'OK' });
      },
    },
  },
];
