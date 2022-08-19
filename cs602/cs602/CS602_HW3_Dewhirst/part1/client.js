const cities = require('./mongo_zipCodeModule_v2');

const colors = require('colors');

(async () => {

	console.log("\nLookup by zip code (02215)".red);
	let result1 = await cities.lookupByZipCode('02215');
	console.log(result1);

	console.log("\nLookup by zip code (99999)".red);
	let result2 = await cities.lookupByZipCode('99999');
	console.log(result2);

	console.log("\nLookup by city (BOSTON, MA)".red);
	let result3 = await cities.lookupByCityState('BOSTON', 'MA');
	console.log(result3);

	console.log("\nGet Population by State (MA)".red);
	let result4 = await cities.getPopulationByState('MA');
	console.log(result4);

	process.exit();
})();
