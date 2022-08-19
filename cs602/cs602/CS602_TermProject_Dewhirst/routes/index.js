const e = require('express');
const db = require('../database.js');
const User = db.getUser();

module.exports = async (req, res, next) => {
  let owners = await User.find({user_type: 'owner'});
  let owner_results = owners.map( owner => {
    return {
      id: owner._id,
      first_name: owner.first_name,
      last_name: owner.last_name
    }
  });

  let administrators = await User.find({user_type: "administrator"});
  let administrator_results = administrators.map( admin => {
    return {
      id: admin._id,
      first_name: admin.first_name,
      last_name: admin.last_name
    }
  });

  res.render('home', { owners: owner_results, administrators: administrator_results });
}
