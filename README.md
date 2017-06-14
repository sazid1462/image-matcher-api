# FBSearch API
# requirements
  * node 6.x
  * npm 3.x
  * yarn
    * `npm install yarn -g`

# To run the project
  *  `yarn`
  *  `npm run dev`

# Before commit run
  * `npm run lint`

# Install flyway
  * create a user `root` with password `root` in mysql
  * create a database named 'doctApp'
  * from schema folder run `flyway migrate`
  * or run `flyway -configFile=config/flyway.conf migrate`

# Never change in the database without flyway
  * follow the migration file version formatting
