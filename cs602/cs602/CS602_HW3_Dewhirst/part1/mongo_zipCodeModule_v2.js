const MongoClient = require('mongodb').MongoClient;
const credentials = require("./credentials.js");

const dbUrl = 'mongodb+srv://' + credentials.username +
	':' + credentials.password + '@' + credentials.host + '/' + credentials.database;

let client = null;

const getConnection = async () => {
	if (client == null)
		client = await MongoClient.connect(dbUrl,  { useNewUrlParser: true ,  useUnifiedTopology: true });
	return client;
}

module.exports.lookupByZipCode = async (zip) => {

	let client = await getConnection();
	let collection = client.db(credentials.database).collection('zipcodes');

	let result = await collection.find({'_id': zip}).toArray();

	return result[0];
};

// Complete the code for the following

module.exports.lookupByCityState = async (city, state) => {

	let client = await getConnection();
	let collection = client.db(credentials.database).collection('zipcodes');
	let result = await collection.find({'city': city, 'state': state}).toArray();

	return {
		'city': city,
		'state': state,
		'data': result.filter(el => el['city'] == city && el['state'] == state).map(function (h, _idx) {
			return { "zip": h['_id'], "pop": h['pop'] }
		})
	}
};

module.exports.getPopulationByState = async (state) => {

	let client = await getConnection();
	let collection = client.db(credentials.database).collection('zipcodes');
	let result = await collection.find({'state': state}).toArray();
	return {
		'state': state,
		'data': result.reduce(function (total, row) {
			if (row['state'] == state) {
				return row['pop'] + total;
			} else {
				return total;
			}
		}, 0)
	}
};
