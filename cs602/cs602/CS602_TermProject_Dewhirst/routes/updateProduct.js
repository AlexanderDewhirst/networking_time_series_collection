const e = require('express');
const db = require('../database.js');
const Product = db.getProduct();

module.exports = async (req, res, next) => {
  let req_params = JSON.parse(JSON.stringify(req.params));
  let body_params = JSON.parse(JSON.stringify(req.body));

  await Product.findOneAndUpdate({ '_id': body_params.id }, {
    name: body_params.name,
    description: body_params.description,
    amount: body_params.amount,
    price: body_params.price
  });

  res.redirect(`/owners/${req_params.owner_id}/stores/${req_params.store_id}/products/${body_params.id}`);
}
