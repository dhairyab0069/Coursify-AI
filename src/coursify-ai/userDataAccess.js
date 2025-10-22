// get user data function apiRoutes.js

const connectToDB = require('./settings_db');

async function getUserData (email){
    const db = await connectToDB();
    const user = await db.collection('users').findOne({email});
    return user;
}

module.exports = {
    getUserData,
};