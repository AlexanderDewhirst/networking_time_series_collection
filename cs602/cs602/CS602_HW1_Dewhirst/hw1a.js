const { lookupByZipCode, lookupByCityState, getPopulationByState } = require('./zipCodeModule_v1');
const colors = require('colors');

lookup_zip1 = "02215";
lookup_zip2 = "99999";

lookup_city1 = "BOSTON";
lookup_state1 = "MA";

lookup_city2 = "BOSTON";
lookup_state2 = "TX";

lookup_city3 = "BOSTON";
lookup_state3 = "AK";

population_state1 = "MA";
population_state2 = "TX";
population_state3 = "AA";

let zip_row1 = lookupByZipCode(lookup_zip1);
let zip_row2 = lookupByZipCode(lookup_zip2);

let city_state_row1 = lookupByCityState(lookup_city1, lookup_state1);
let city_state_row2 = lookupByCityState(lookup_city2, lookup_state2);
let city_state_row3 = lookupByCityState(lookup_city3, lookup_state3);

let population1 = getPopulationByState(population_state1);
let population2 = getPopulationByState(population_state2);
let population3 = getPopulationByState(population_state3);

function print_results(method, result, ...args) {
  if (result === null) {
    console.log(`${method} ${args} - undefined`);
  } else if (typeof result === 'object' && result !== null) {
    console.log(`${method} ${args} - ${JSON.stringify(result)}`);
  } else {
    console.log(`${method} ${args} - ${result}`);
  }
}

print_results('lookupByZipCode', zip_row1, [lookup_zip1]);
print_results('lookupByZipCode', zip_row2, [lookup_zip2]);

print_results('lookupByCityState', city_state_row1, [lookup_city1, lookup_state1]);
print_results('lookupByCityState', city_state_row2, [lookup_city2, lookup_state2]);
print_results('lookupByCityState', city_state_row3, [lookup_city3, lookup_state3]);

print_results('getPopulationByState', population1, [population_state1]);
print_results('getPopulationByState', population2, [population_state2]);
print_results('getPopulationByState', population3, [population_state3]);
