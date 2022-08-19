const db = require('./database.js');
const User = db.getUser();
const Store = db.getStore();
const Product = db.getProduct();

(async() => {
  await Product.deleteMany({});
  await Store.deleteMany({});
  await User.deleteMany({});

  let user1 = new User({
    first_name: 'allie',
    last_name: 'gater',
    user_type: 'owner'
  });

  let user2 = new User({
    first_name: 'joe',
    last_name: 'king',
    user_type: 'owner'
  });

  let user3 = new User({
    first_name: 'justin',
    last_name: 'thyme',
    user_type: 'administrator'
  });

  await Promise.all([
    user1.save(),
    user2.save(),
    user3.save()
  ]);

  let owner_one = await User.findOne({first_name: 'allie', last_name: 'gater'});
  console.log(owner_one);
  let owner_two = await User.findOne({first_name: 'joe', last_name: 'king'});
  console.log(owner_two);

  let store1 = new Store({
    owner: owner_one._id,
    address: '123 Fizzbuzz Bee'
  });

  let store2 = new Store({
    owner: owner_two._id,
    address: '321 Foobar Bun'
  });

  await Promise.all([
    store1.save(),
    store2.save()
  ])

  let store_one = await Store.findOne({address: '123 Fizzbuzz Bee'});
  console.log(store_one);
  let store_two = await Store.findOne({address: '321 Foobar Bun'});
  console.log(store_two);

  let product1 = new Product({
    store: store_one._id,
    name: 'prod1',
    description: 'Product 1',
    amount: 1,
    price: 20
  });

  let product2 = new Product({
    store: store_two._id,
    name: 'prod2',
    description: "Product 2",
    amount: 5,
    price: 5
  });

  let product3 = new Product({
    store: store_two._id,
    name: 'prod3',
    description: 'Product 3',
    amount: 2,
    price: 10
  });

  await Promise.all([
    product1.save(),
    product2.save(),
    product3.save()
  ])

  let product_one = await Product.findOne({name: 'prod1'});
  console.log(product_one);
  let product_two = await Product.findOne({name: 'prod2'});
  console.log(product_two);
  let product_three = await Product.findOne({name: 'prod3'});
  console.log(product_three);

  process.exit();
})();
