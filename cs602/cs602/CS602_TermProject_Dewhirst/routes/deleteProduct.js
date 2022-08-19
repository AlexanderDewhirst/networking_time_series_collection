const e = require('express');
const db = require('../database.js');
const Product = db.getProduct();

module.exports = async (req, res, next) => {
  let params = JSON.parse(JSON.stringify(req.params));

  await Product.findOneAndDelete({ '_id': params.product_id });

  res.redirect(`/owners/${params.owner_id}/stores/${params.store_id}`);
}
