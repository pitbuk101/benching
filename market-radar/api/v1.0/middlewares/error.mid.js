const winston = require('winston');
const errorHandler = (err, req, res, next) => {
    winston.error(err.message, err);
    res.status(500).json({
        status: "failed",
        error: err
    });
};

module.exports = errorHandler;