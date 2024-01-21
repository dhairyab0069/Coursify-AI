/* MongoClient
 The "mongodb" package is the MongoDB driver for Node.js
- This imports the MongoClient class from the mongodb package. 
- The { MongoClient } syntax is destructuring assignment, which is used to extract the MongoClient property from the imported mongodb object.
*/
/* const URI 
- Uniform Resource Identifier
- "process.env" -global Node.js variable, allows access to the predefined environment variables from the system where the Node.js process is running
- connection string should include including the username, password, and cluster information 
*/                    
/* async meaning
async keyword allows to use 'await' within the function to pause the execution until a promise is resolved.
*/
/* if statement meaning
- If dbInstance is already set (!= null), the function returns the exisiting databse stance instead of creating a new connection.
- ensures that only one databse connection is used.
*/
/* const client
- new isntance of MongoClient is created using the connection URI
- useNewUrl parser
- useUnifiedTopology
*/
/* await client
- connect method of the Mongoclient instance is called
- 'await' is used wait for the connection to be established.
*/
/* client.db()
- once the connection is  successful, the 'db' method is called on the MongoClient instance to get a ref to the default database.
- to connect to a specific db, client.db(name of specific db)
- the reference to the db is stored in dbInstance.
*/
/* return
the connected database instance is returned to the caller.
*/
/* module.export
- the functio is exported from the module.
- allows the function to be imported and called in other files in the Node.js project.
*/
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI; //Replace MONGODB_URI
let dbInstance = null; // this will store a reference to the connected database later on.

async function connectToDB() {

    if (dbInstance){
        return dbInstance;
    }

    try{
        const client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology:true});
        await client.connect();
        dbInstance = client.db("Login_details");

        console.log("successfully connected to MongoDB.");

        return dbInstance;

    }catch (error) {
        console.error("connection to MongoDB failed: ", error);
        throw error;
    }
}

module.exports = connectToDB;