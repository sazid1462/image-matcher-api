const Joi = require('joi');
const fs = require('fs');
const Path = require('path');

module.exports = [
  {
    method: 'POST',
    path: '/image',
    config: {
      tags: ['api'],
      payload: {
        output: 'stream',
        parse: true,
        uploads: 'up_files',
        timeout: 30034,
        allow: 'multipart/form-data',
        failAction: 'log',
        maxBytes: 3000000,
      },
      validate: {
        payload: {
          file: Joi.any()
            .meta({ swaggerType: 'file' })
            .description('json file'),
        },
      },
      plugins: {
        'hapi-swagger': {
          payloadType: 'form',
        },
      },
      handler: (request, reply) => {
        const data = request.payload.file;
        if (data) {
          const name = data.hapi.filename;
          const path = Path.join(__dirname, '/../../../uploads/', name);
          const file = fs.createWriteStream(path);

          file.on('error', (err) => {
            console.error(err);
          });

          data.pipe(file);

          data.on('end', (err) => {
            if (err) {
              throw err;
            }
            const ret = {
              filename: data.hapi.filename,
            };
            reply(JSON.stringify(ret));
          });
        } else {
          console.log('fuck');
        }
      },
    },
  },
];
