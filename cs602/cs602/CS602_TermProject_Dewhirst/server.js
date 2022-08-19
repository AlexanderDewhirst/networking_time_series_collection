const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

var express_handlebars = require('express-handlebars');
var handlebars_helpers = express_handlebars.create({
  helpers: require("./helpers/handlebars.js").helpers,
  defaultLayout: 'main'
});

app.engine('handlebars', handlebars_helpers.engine);
app.set('view engine', 'handlebars');

var router = require('./routes/router.js');
app.use('/', router);

app.listen(3000, function() {
  console.log("Server started.");
});
