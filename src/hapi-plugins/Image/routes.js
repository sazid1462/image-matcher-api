const Joi = require('joi');
const fs = require('fs');
const Path = require('path');
const sys = require('sys');
const spawn = require('child_process').spawn;

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
            // exec('ls', (exErr, stdout, stderr) => {
            //   sys.print(`stdout ${stdout}`);
            //   sys.print(`stdin ${stderr}`);
            //   if (exErr) {
            //     console.log(`error ${exErr}`);
            //   }
            // });

            const ps = spawn('python', ['/code/pythonScript/elasticclient.py', `/code/uploads/${name}`]);

            ps.stdout.on('data', (res) => {
              console.log(`stdout: ${res}`);
            });

            ps.stderr.on('data', (res) => {
              console.log(`stderr: ${res}`);
            });

            ps.on('close', (res) => {
              console.log(`child process exited with code ${res}`);
            });
            reply(JSON.stringify(ret));
          });
        } else {
          console.log('fuck');
        }
      },
    },
  },
  {
    method: 'GET',
    path: '/image/{uuid}',
    config: {
      tags: ['api'],
      description: 'Get an Image',
      handler: (request, reply) => {
        reply({ status: 'OK' });
      },
    },
  },
  // {
  //   method: 'GET',
  //   path: '/yourpath',
  //   handler: (request, reply) => {
  //     reply(null, something().pipe());
  //   },
  // },
];
