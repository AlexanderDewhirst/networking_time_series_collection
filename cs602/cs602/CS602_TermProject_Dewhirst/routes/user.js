const e = require('express');
const db = require('../database.js');
const User = db.getUser();
const Store = db.getStore();

module.exports = async (req, res, next) => {
  let user_params = JSON.parse(JSON.stringify(req.params));
  let user = await User.findOne({ '_id': user_params.id });
  let user_result = { id: user._id, first_name: user.first_name, last_name: user.last_name, user_type: user.user_type };

  let stores = null;
  if (user.user_type == 'owner') {
    stores = await Store.find({ owner: user._id });
  } else if (user.user_type == 'administrator') {
    stores = await Store.find({});
  }
  let store_results = stores.map( store => {
    return {
      id: store._id,
      address: store.address
    }
  });

  res.render('user', { user: user_result, stores: store_results });
}
