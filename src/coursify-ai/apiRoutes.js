const express = require ('express');
const router = express.Router();
const userDataAccess = require('./userDataAccess');

router.get('/user/:email', async(req, res)=>{
    try{
        const email = req.params.email;
        const user = await userDataAccess.getUserData(email);
        if(!user){
            return res.status(404).send('User not found');
        }

        res.json(user);
    }catch (error){
        res.status(500).send(error.toString());
    }

})

module.exports = router;