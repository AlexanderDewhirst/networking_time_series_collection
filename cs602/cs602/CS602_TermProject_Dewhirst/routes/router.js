var express = require('express');
var router = express.Router();

var index = require('./index.js');
var user = require('./user.js');
var store = require('./store.js');
var product = require('./product.js');
var newProduct = require('./newProduct.js');
var createProduct = require('./createProduct.js');
var updateProduct = require('./updateProduct.js');
var deleteProduct = require('./deleteProduct.js');

router.get('/', index);

router.get('/owners/:id', user);
router.get('/administrators/:id', user);

router.get('/owners/:owner_id/stores/:store_id', store);
router.get('/administrators/:administrator_id/stores/:store_id', store);

router.get('/owners/:owner_id/stores/:store_id/products/:product_id', product);
router.get('/owners/:owner_id/stores/:store_id/newProduct', newProduct);
router.post('/owners/:owner_id/stores/:store_id/products/create', createProduct);
router.post('/owners/:owner_id/stores/:store_id/products/:product_id', updateProduct);
router.post('/owners/:owner_id/stores/:store_id/products/:product_id/delete', deleteProduct);

router.get('/administrators/:administrator_id/stores/:store_id/products/:product_id', product);

// TODO
// Admin can
//  create Owner
//  create Store for Owner

// Fix Delete action

// Add API endpoints for JSON and XML.

module.exports = router;
