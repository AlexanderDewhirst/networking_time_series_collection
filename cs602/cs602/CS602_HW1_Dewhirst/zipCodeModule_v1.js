const data = require('./zips.json');

function lookupByZipCode(zip) {
  let obj;
  for (let i = 0; i < data.length; i++) {
    if (zip == data[i]['_id']) {
      obj = data[i];
    }
  }
  return obj;
};

function lookupByCityState(city, state) {
  let obj = {
    'city': city,
    'state': state,
    'data': []
  };
  for (let i = 0; i < data.length; i++) {
    if (city == data[i]["city"] && state == data[i]["state"]) {
      zip = data[i]['_id'];
      pop = data[i]['pop'];
      obj['data'].push({"zip": zip, "pop": pop});
    }
  }
  return obj;
}

function getPopulationByState(state) {
  let obj = { 'state': state, 'data': 0 };
  for (let i = 0; i < data.length; i++) {
    if (state == data[i]["state"]) {
      obj['data'] += data[i]["pop"];
    }
  }
  return obj;
}

module.exports = {
  lookupByZipCode,
  lookupByCityState,
  getPopulationByState
}
