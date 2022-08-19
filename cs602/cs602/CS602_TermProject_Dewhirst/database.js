const mongoose = require('mongoose');
const dbUrl = 'mongodb://localhost:27017'

let connection = null;
let user = null;
let store = null;
let product = null;

let Schema = mongoose.Schema;

let userSchema = new Schema({
  first_name: String,
  last_name: String,
  user_type: String
}, {
  collection: 'users'
});

let storeSchema = new Schema({
  owner: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'owner'
  },
  address: String
}, {
  collection: 'stores'
});

let productSchema = new Schema({
  store: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'store'
  },
  name: String,
  description: String,
  amount: Number,
  price: Number
}, {
  collection: 'products'
});

module.exports = {
  getUser: () => {
    if (connection == null) {
      console.log("Creating DB connection");
      connection = mongoose.createConnection(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true });
    };
    user = connection.model('User', userSchema);
    return user;
  },
  getStore: () => {
    if (connection == null) {
      console.log("Creating DB connection");
      connection = mongoose.createConnection(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true });
    };
    store = connection.model('Store', storeSchema);
    return store;
  },
  getProduct: () => {
    if (connection == null) {
      console.log("Creating DB connection");
      connection = mongoose.createConnection(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true });
    };
    product = connection.model('Product', productSchema);
    return product;
  }
};
