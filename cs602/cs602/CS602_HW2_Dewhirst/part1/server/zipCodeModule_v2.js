const data = require('./zips.json');

function lookupByZipCode(zip) {
  return data.find(el => el['_id'] == zip) || {};
}

function lookupByCityState(city, state) {
  return {
    'city': city,
    'state': state,
    'data': data.filter(el => el['city'] == city && el['state'] == state).map(function (h, _idx) {
      return { "zip": h['_id'], "pop": h['pop'] }
    })
  };
}

function getPopulationByState(state) {
  return {
    'state': state,
    'data': data.reduce(function (total, row) {
      if (row['state'] == state) {
        return row['pop'] + total;
      } else {
        return total;
      }
    }, 0)
  };
}

module.exports = {
  lookupByZipCode,
  lookupByCityState,
  getPopulationByState
}
