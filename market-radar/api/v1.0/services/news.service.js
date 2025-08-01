
// services/news.service.js
const { getConnection } = require('../config/snowflake.config');

async function getPaginatedNews(tableName, categoryName, page, pageSize) {
    const connection = await getConnection();

    if (!connection) {
        throw new Error('No active session. Please create a session first.');
    }

    const offset = (page - 1) * pageSize;

    // Start building the SQL query
    let query = `SELECT * FROM ${tableName}`;

    const queryParams = [];

    // Add a WHERE clause if CATEGORYNAME is provided
    if (categoryName) {
        query += ` WHERE LOWER(CATEGORYNAME) = LOWER(?)`;
        queryParams.push(categoryName);
    }

    // Add the ORDER BY and LIMIT/OFFSET clauses
    query += `
        ORDER BY PUBLICATIONDATE DESC
        LIMIT ? 
        OFFSET ?
    `;
    queryParams.push(pageSize, offset);

    return new Promise((resolve, reject) => {
        connection.execute({
            sqlText: query,
            binds: queryParams,  // Bind parameters to prevent SQL injection
            complete: (err, stmt, rows) => {
                if (err) {
                    return reject(new Error('Error executing query: ' + err.message));
                }
                resolve(rows);
            }
        });
    });
}

module.exports = {
    getPaginatedNews
};
