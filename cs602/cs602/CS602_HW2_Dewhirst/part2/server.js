const express = require('express');
const app = express();

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// setup handlebars view engine
const handlebars = require('express-handlebars');

app.engine(
	'handlebars',
	handlebars({defaultLayout: 'main'})
);
app.set('view engine', 'handlebars');
app.use(express.static(__dirname + '/public'));

const cities = require('./zipCodeModule_v2');


// ROUTES

app.get('/',  (_req, res) => {
	res.render('homeView');
});

app.get('/zip', (req, res) => {
	let zip_response = cities.lookupByZipCode(req.query['id']);

	if (zip_response != null) {
		res.render("lookupByZipView", { response: zip_response });
	} else {
		res.render("lookupByZipForm");
	}
});

app.post('/zip', (req, res) => {
	let zip_response = cities.lookupByZipCode(req.body['id']);

	res.render("lookupByZipView", { response: zip_response });
});

app.get('/zip/:id', (req, res) => {
	let zip_response = cities.lookupByZipCode(req.params['id']);

	res.format({
		html: function() {
			res.render("lookupByZipView", { response: zip_response });
		},
		'application/json': function() {
			res.type('application/json');
			res.send(zip_response);
		},
		'application/xml': function() {
			let zipXml = '<?xml version="1.0"?>\n  <response>\n    <zipcode id="' +
				zip_response["_id"] +
				'">' +
				zip_response["city"] + ', ' + zip_response["state"] + ' - ' + zip_response["pop"] +
				'</zipcode>\n  </response>';
			res.send(zipXml);
		}
	});
});

app.get('/city', (req, res) => {
	let city_state_response = cities.lookupByCityState(req.query['city'], req.query['state']);

	if (city_state_response["city"] != null && city_state_response["state"] != null) {
		res.render("lookupByCityStateView", { response: city_state_response });
	} else {
		res.render("lookupByCityStateForm");
	}
});

app.post('/city', (req, res) => {
	let city_state_response = cities.lookupByCityState(req.body['city'], req.body['state']);

	res.render("lookupByCityStateView", { response: city_state_response });
});

app.get('/city/:city/state/:state', (req, res) => {
	let city_state_response = cities.lookupByCityState(req.params['city'], req.params['state']);

	res.format({
		html: function() {
			res.render('lookupByCityStateView', { response: city_state_response});
		},
		'application/json': function() {
			res.send(city_state_response);
		},
		'application/xml': function() {
			let cityStateXml = '<?xml version="1.0"?>\n  <response>' +
				'\n    <city>' + city_state_response["city"] + '</city>' +
				'\n    <state>' + city_state_response["state"] + '</state>\n    ' +
				city_state_response["data"].map(function(h) {
					return '<zipcode>' + h['zip'] + '</zipcode><population>' + h['pop'] + '</population>';
				}).join('\n    ') + '\n  </response>';
			res.send(cityStateXml);
		}
	})
});

app.get('/pop', (req, res) => {
	let population_response = cities.getPopulationByState(req.query['state']);

	if (population_response['state'] != null) {
		res.render("populationView", { response: population_response });
	} else {
		res.render("populationForm");
	}
});

app.get('/pop/:state', (req, res) => {
	let population_response = cities.getPopulationByState(req.params['state']);

	res.format({
		html: function() {
			res.render('populationView', { response: population_response });
		},
		'application/json': function() {
			res.send(population_response);
		},
		'application/xml': function() {
			let populationXml = '<?xml version="1.0"?>\n  <response>' +
				'\n    <state>' + population_response['state'] + '</state>' +
				'\n    <population>' + population_response['data'] + '</population>\n  </response>';
			res.send(populationXml);
		}
	})
});

app.use((req, res) => {
	res.status(404);
	res.render('404');
});

app.listen(3000, () => {
  console.log('http://localhost:3000');
});
