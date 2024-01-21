Fetching Data from the Login_detail database to the Settings page.

BACK END SETUP

1. Databse Connection

   - Set up a server-side script using maybe Node.js with Express
   - Download Node and MongoDB driver connect to your MongoDB Atlas database.
   - Connect to MongoDB Atlas database.

   - Using the connection

     - can use the connect function on server.js once the integration is done.
     - close the connection

- settings_db.js: establishes the connection to the MongoDB, using the MongoDB driver. Exports the connectToDB function, which returns a databse connection instance when called.

- userDataAccess.js: Create this new file at the same level as settings_db.js. This will contain your getUserData function and potentially other database interaction functions.

- apiRoutes.js: Create a new file for your Express route handlers that will use the functions from userDataAccess.js to serve API endpoints.
