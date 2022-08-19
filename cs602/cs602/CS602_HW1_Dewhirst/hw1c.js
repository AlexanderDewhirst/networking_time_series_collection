const colors = require('colors');

const ZipCodeEmitter = require('./zipCodeEmitter').ZipCodeEmitter;

const cities = new ZipCodeEmitter();

lookup_zip1 = '02215';
lookup_city1 = 'BOSTON';
lookup_state1 = 'MA';
population_state1 = 'MA';

console.log(`Lookup by zip code (${lookup_zip1})`);
cities.lookupByZipCode(lookup_zip1);

console.log();

console.log(`Lookup by city (${lookup_city1}, ${lookup_state1})`);
cities.lookupByCityState(lookup_city1, lookup_state1);

console.log();

console.log(`Get population by state (${population_state1})`);
cities.getPopulationByState(population_state1);
