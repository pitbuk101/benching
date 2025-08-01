// controllers/news.controller.js
const { getPaginatedNews } = require('../services/news.service.js');

exports.getNews = async (req, res, next) => {
    try {
        return res.status(200).json({
            status: 'success',
            msg: "",
            data: []
        });
    } catch (err) {
        next(err);
    }
};

exports.getCategoryNews = async (req, res, next) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 10;
        const categoryName = req.query.categoryName;

        const rows = await getPaginatedNews('CATEGORYNEWS', categoryName, page, pageSize);

        return res.status(200).json({
            data: rows,
            status: 'success'
        });
    } catch (err) {
        console.log(err);
        next(err);
    }
};

exports.getSupplierNews = async (req, res, next) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 10;
        const categoryName = req.query.categoryName;

        const rows = await getPaginatedNews('SUPPLIERNEWS', categoryName, page, pageSize);

        return res.status(200).json({
            data: rows,
            status: 'success'
        });
    } catch (err) {
        console.log(err);
        next(err);
        next(err);
    }
};

exports.getKeywordNews = async (req, res, next) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 10;
        const categoryName = req.query.categoryName;

        const rows = await getPaginatedNews('KEYWORDNEWS', categoryName, page, pageSize);

        return res.status(200).json({
            data: rows,
            status: 'success'
        });
    } catch (err) {
        console.log(err);
        next(err)
    }
};
