const express = require('express');
const bodyParser = require('body-parser');
const router = express.Router();
const protectRoute = require('./middlewares/protect.mid')

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({
    extended:true
}));

router.use('/news', require('./routes/news.route'));




module.exports = router;
