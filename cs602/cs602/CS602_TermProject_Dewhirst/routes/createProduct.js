const e = require('express');
const db = require('../database.js');
const Product = db.getProduct();

module.exports = async (req, res, next) => {
  let req_params = JSON.parse(JSON.stringify(req.params));
  let body_params = JSON.parse(JSON.stringify(req.body));

  await Product.create({
    name: body_params.name,
    description: body_params.description,
    amount: body_params.amount,
    price: body_params.price,
    store: req_params.store_id
  });

  let product = await Product.findOne({
    name: body_params.name,
    store: req_params.store_id
  });

  res.redirect(`/owners/${req_params.owner_id}/stores/${req_params.store_id}/products/${product._id}`)
}
