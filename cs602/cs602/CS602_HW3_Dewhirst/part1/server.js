const express = require('express');
const app = express();

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// setup handlebars view engine
const handlebars = require('express-handlebars');

app.engine('handlebars',
	handlebars({defaultLayout: 'main'}));

app.set('view engine', 'handlebars');

// static resources
app.use(express.static(__dirname + '/public'));

// Use the employee module
const cities = require('./mongo_zipCodeModule_v2');

// GET request to the homepage
app.get('/', function (req, res){
	res.render('homeView');
});

app.get('/zip', async function(req, res) {
	if (req.query.id) {
		let id = req.query.id;
		let result = await cities.lookupByZipCode(id);
		res.render('lookupByZipView', result);
	} else {
		res.render('lookupByZipForm');
	}
});

app.post('/zip', async function(req, res) {
	let id = req.body.id;
	let result = await cities.lookupByZipCode(id);
	res.render('lookupByZipView', result);
});

app.get('/zip/:id', async function(req, res) {
	let id = req.params.id;
	let result = await cities.lookupByZipCode(id);

	res.format({
		'application/json': function() {
			res.json(result);
		},
		'application/xml': function() {
			let resultXml =
				'<?xml version="1.0"?>\n' +
						'<zipCode id="' + result._id + '">\n' +
						'   <city>' + result.city + '</city>\n' +
						'   <state>' + result.state + '</state>\n' +
						'   <pop>' + result.pop + '</pop>\n' +
						'</zipCode>\n';


			res.type('application/xml');
			res.send(resultXml);
		},
		'text/html': function() {
			res.render('lookupByZipView', result);

		}
	});
});

// Complete the code for the following
app.get('/city', async function(req, res){
	let city_state_response = await cities.lookupByCityState(req.query['city'], req.query['state']);

	if (city_state_response["city"] != null && city_state_response["state"] != null) {
		res.render("lookupByCityStateView", { response: city_state_response });
	} else {
		res.render("lookupByCityStateForm");
	}
});

app.post('/city', async function(req, res){
	let city_state_response = await cities.lookupByCityState(req.body['city'], req.body['state']);

	res.render("lookupByCityStateView", { response: city_state_response });
});

app.get('/city/:city/state/:state', async function(req, res) {
	let city_state_response = await cities.lookupByCityState(req.params['city'], req.params['state']);

	res.format({
		html: function() {
			res.render('lookupByCityStateView', { response: city_state_response});
		},
		'application/json': function() {
			res.json(city_state_response);
		},
		'application/xml': function() {
			let cityStateXml = '<?xml version="1.0"?>\n  <response>' +
				'\n    <city>' + city_state_response["city"] + '</city>' +
				'\n    <state>' + city_state_response["state"] + '</state>\n    ' +
				city_state_response["data"].map(function(h) {
					return '<zipcode>' + h['zip'] + '</zipcode><population>' + h['pop'] + '</population>';
				}).join('\n    ') + '\n  </response>';
			res.type('application/xml');
			res.send(cityStateXml);
		}
	});
});

app.get('/pop', async function(req, res) {
	let population_response = await cities.getPopulationByState(req.query['state']);

	if (population_response['state'] != null) {
		res.render("populationView", { response: population_response });
	} else {
		res.render("populationForm");
	}
});

app.get('/pop/:state', async function(req, res) {
	let population_response = await cities.getPopulationByState(req.params['state']);

	res.format({
		html: function() {
			res.render('populationView', { response: population_response });
		},
		'application/json': function() {
			res.json(population_response);
		},
		'application/xml': function() {
			let populationXml = '<?xml version="1.0"?>\n  <response>' +
				'\n    <state>' + population_response['state'] + '</state>' +
				'\n    <population>' + population_response['data'] + '</population>\n  </response>';
			res.type('application/xml');
			res.send(populationXml);
		}
	});
});

app.use(function(req, res) {
	res.status(404);
	res.render('404');
});

app.listen(3000, function(){
  console.log('http://localhost:3000');
});
