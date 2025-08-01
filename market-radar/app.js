const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();
const protectRoute = require('./api/v1.0/middlewares/protect.mid')
const { getConnection } = require('./api/v1.0/config/snowflake.config');



const app = express();
app.disable('x-powered-by');
app.use(bodyParser.urlencoded({extended:true}));

const PORT = process.env.PORT 

app.get('/health', async (req, res) => {
    try {
        // Try to get a Snowflake connection
        const connection = await getConnection();
        
        // If successful, send a 200 OK response with the health status
        res.status(200).json({
            status: 'ok',
            message: 'Service is running and Snowflake is connected',
            timestamp: new Date().toISOString(),
        });
    } catch (error) {
        // If there's any error, respond with a 500 Internal Server Error
        console.error('Health check failed:', error);
        res.status(500).json({
            status: 'error',
            message: 'Service is down or Snowflake connection failed',
            error: error.message || 'Unknown error',
        });
    }
});



app.use('/api',protectRoute, require('./api'));


const server = app.listen(PORT, (req,res)=>{
    console.log(`We are listening to port ${PORT}`)
});

module.exports.server = server;


