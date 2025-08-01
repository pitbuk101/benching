const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const MCKID_JWKS_URI = process.env.MCKID_JWKS_URI;
const MCKID_EXPECTED_AUDIENCE = process.env.MCKID_EXPECTED_AUDIENCE;
const MCKID_TOKEN_ISSUER = process.env.MCKID_TOKEN_ISSUER;

class JWTTokenVerifier {
  /**
   * Retrieve the signing key from the JWKS URI.
   * @param {string} token - JWT token string.
   * @returns {Promise<string>} - The signing key extracted from JWKS.
   */
  static _getSigningKey(token) {
    const client = jwksClient({
      jwksUri: MCKID_JWKS_URI,
    });

    const decodedToken = jwt.decode(token, { complete: true });
    const kid = decodedToken.header.kid;

    return new Promise(function (resolve, reject) {
      client.getSigningKey(kid, function (err, key) {
        if (err) {
          reject(err);
        } else {
          resolve(key.getPublicKey());
        }
      });
    });
  }

  /**
   * Retrieve the token signing algorithm from JWT headers.
   * @param {string} token - JWT token string.
   * @returns {string} - The signing algorithm extracted from JWT headers.
   */
  static _getSigningAlg(token) {
    const jwtHeaders = this._getJwtHeaders(token);
    return jwtHeaders.alg;
  }

  /**
   * Retrieve JWT token headers.
   * @param {string} token - JWT token string.
   * @returns {object} - The headers of the JWT token.
   */
  static _getJwtHeaders(token) {
    return jwt.decode(token, { complete: true }).header;
  }

  /**
   * Decode the JWT token and verify its signature.
   * @param {string} token - JWT token string.
   * @returns {Promise<object>} - Contextual information extracted from the token.
   */
  static async _decodeToken(token) {
    const signingAlg = this._getSigningAlg(token);
    const signingKey = await this._getSigningKey(token);

    return new Promise(function (resolve, reject) {
      jwt.verify(
        token,
        signingKey,
        {
          algorithms: [signingAlg],
          audience: MCKID_EXPECTED_AUDIENCE,
          issuer: MCKID_TOKEN_ISSUER,
        },
        function (err, decoded) {
          if (err) {
            reject(err);
          } else {
            resolve(decoded);
          }
        }
      );
    });
  }

  /**
   * Build user metadata from the token context.
   * @param {object} tokenContext - The context extracted from the JWT token.
   * @returns {object} - User metadata including email, first name, last name, and firm_no.
   */
  static _buildUserMeta(tokenContext) {
    const email = tokenContext.email;

    if (email) {
      return {
        email: email.toLowerCase(),
        first_name: tokenContext.given_name,
        last_name: tokenContext.family_name,
        firm_no: tokenContext.fmno,
        account_type: 'USER',
      };
    } else {
      const clientId = tokenContext.clientId;
      return {
        email: `${clientId}@sai.mckinsey.com`,
        first_name: 'Service',
        last_name: 'Account',
        firm_no: clientId,
        account_type: 'SERVICE',
      };
    }
  }

  /**
   * Verify the authenticity of the JWT token.
   * @param {string} token - JWT token string.
   * @returns {Promise<object>} - A dictionary containing the verification result and token context.
   */
  static async verifyToken(token) {
    try {
      const tokenContext = await this._decodeToken(token);
      const metadata = this._buildUserMeta(tokenContext);
      return { is_authorised: true, context: metadata };
    } catch (error) {
      return { is_authorised: false, error: error.message };
    }
  }
}

module.exports = JWTTokenVerifier;
