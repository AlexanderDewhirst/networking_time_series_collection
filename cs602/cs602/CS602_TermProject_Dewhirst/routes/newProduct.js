const e = require('express');
const db = require('../database.js');
const User = db.getUser();
const Store = db.getStore();

module.exports = async (req, res, next) => {
  let params = JSON.parse(JSON.stringify(req.params));

  let user = null;
  if (params.owner_id != null) {
    user = await User.findOne({ '_id': params.owner_id });
  } else if (params.administrator_id != null) {
    user = await User.findOne({ '_id': params.administrator_id });
  }
  let user_result = { id: user._id, first_name: user.first_name, last_name: user.last_name, user_type: user.user_type };

  let store = await Store.findOne({ '_id': params.store_id });
  let store_result = { id: store._id, address: store.address };

  let owner = null;
  if (user.user_type == 'owner') {
    owner = user;
  } else if (user.user_type == 'administrator') {
    owner = await User.findOne({ '_id': store.owner });
  }
  let owner_result = { id: owner._id, first_name: owner.first_name, last_name: owner.last_name, user_type: owner.user_type };

  let product_result = { name: '', description: '', amount: '', price: '' };

  let route = `/owners/${owner.id}/stores/${store.id}/products/create`;
  res.render('product', { route: route, user: user_result, owner: owner_result, store: store_result, product: product_result });
}
