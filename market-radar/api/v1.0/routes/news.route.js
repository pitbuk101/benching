const express = require('express');
const router = express.Router();
const newsControolers = require('../controllers/news')
const { verifyJWT } = require('../middlewares/auth.mid'); 


router.get('/category', newsControolers.getCategoryNews);
router.get('/supplier', newsControolers.getSupplierNews);
router.get('/keyword', newsControolers.getKeywordNews);



module.exports = router;