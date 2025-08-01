require('dotenv').config();  // Make sure to load environment variables from a .env file
const jwksClient = require('jwks-rsa');
const jwt = require('jsonwebtoken');

// Load environment variables
const jwksUri = process.env.MCKID_JWKS_URI;
const expectedAudience = process.env.MCKID_EXPECTED_AUDIENCE;
const expectedIssuer = process.env.MCKID_TOKEN_ISSUER;

// Create the JWKS client to fetch keys from your JWKS endpoint
const client = jwksClient({
  jwksUri: jwksUri,
});

// Function to retrieve the key from the JWKS endpoint based on the JWT's key ID (kid)
function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    if (err) {
      callback(err);
      return;
    }
    const signingKey = key.publicKey || key.rsaPublicKey;
    callback(null, signingKey);
  });
}

// Middleware to verify JWT token
function protectRoute(req, res, next) {
  const authHeader = req.header('Authorization');
  
  if (!authHeader) {
    return res.status(401).json({ message: 'Authorization token is required' });
  }

  const token = authHeader.split(' ')[1]; // Extract token after 'Bearer'
  
  if (!token) {
    return res.status(401).json({ message: 'Authorization token is required' });
  }

  jwt.verify(token, getKey, {
    audience: expectedAudience,  // Validate the audience (aud claim)
    issuer: expectedIssuer,      // Validate the issuer (iss claim)
  }, (err, decoded) => {
    if (err) {
      return res.status(401).json({ message: 'Invalid or expired token', error: err.message });
    }

    // Attach the decoded token to the request object
    req.user = decoded;
    next();  // Proceed to the next middleware or route handler
  });
}

module.exports = protectRoute;
