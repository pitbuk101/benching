const snowflake = require('snowflake-sdk');
require('dotenv').config();

let connection = null;
let isConnecting = false;
let pendingRequests = []; 

const createConnection = () => {
    return new Promise((resolve, reject) => {
        if (connection) {
            return resolve(connection);
        }

        if (isConnecting) {
            pendingRequests.push({ resolve, reject });
            return;
        }

        isConnecting = true;
        connection = snowflake.createConnection({
            account: process.env.SF_ACCOUNT,
            username: process.env.SF_USERNAME,
            password: process.env.SF_PASSWORD,
            warehouse: process.env.warehouse,
            database: process.env.market_database,
            schema: 'NEWS',
        });

        connection.connect((err) => {
            isConnecting = false;

            if (err) {
                const errorMessage = `Unable to connect to Snowflake: ${err.message}`;
                console.error(errorMessage);
                pendingRequests.forEach((req) => req.reject(new Error(errorMessage)));
                pendingRequests = [];
                reject(new Error(errorMessage));
                return;
            }

            console.log('Successfully connected to Snowflake!');
            pendingRequests.forEach((req) => req.resolve(connection));
            pendingRequests = [];
            resolve(connection); 
        });
    });
};

module.exports.getConnection = createConnection;
