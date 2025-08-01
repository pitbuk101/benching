// middleware.js (ES5 syntax)
const JWTTokenVerifier = require('../utils/JWTTokenVerifier'); // Import the class from JWTTokenVerifier

/**
 * Middleware to verify JWT token
 * @param {object} req - Express request object
 * @param {object} res - Express response object
 * @param {function} next - Express next middleware function
 */
async function verifyJWT(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1]; // Get the token from Authorization header (Bearer token)

  if (!token) {
    return res.status(401).json({ message: 'No token provided' });
  }

  try {
    const result = await JWTTokenVerifier.verifyToken(token);

    if (result.is_authorised) {
      // Attach the user metadata to the request object for use in route handlers
      req.user = result.context;
      return next();
    } else {
      return res.status(403).json({ message: 'Unauthorized', error: result.error });
    }
  } catch (error) {
    return res.status(500).json({ message: 'Internal server error', error: error.message });
  }
}

module.exports = {
  verifyJWT: verifyJWT,
};
