const EventEmitter = require('events').EventEmitter;
const data = require('./zips.json');

class ZipCodeEmitter extends EventEmitter {
	constructor() {
		super();
	}

	lookupByZipCode(zip)  {
		console.log("Event lookupByZipCode raised!");

		let obj = data.find(el => el['_id'] == zip);

		this._print_results('lookupByZipCode', obj, zip);
		this.emit('lookupByZipCode', obj);
	}

	lookupByCityState(city, state) {
		this._lookupByCityState_handler1(city, state);
		this._lookupByCityState_handler2(city, state);
	}

	_lookupByCityState_handler1(city, state)  {
		console.log("Event lookupByCityState raised! (Handler1)");

		let obj = {
			'city': city,
			'state': state,
			'data': data.filter(el => el['city'] == city && el['state'] == state)
		}

		this._print_results('lookupByCityState', obj, city, state);
		this.emit('lookupByCityState', obj);
	}

	_lookupByCityState_handler2(city, state) {
		console.log("Event lookupByCityState raised! (Handler2)");

		let obj = {
			'city': city,
			'state': state,
			'data': data.filter(el => el['city'] == city && el['state'] == state)
		}

		console.log(`City: ${obj['city']}, State: ${obj['state']}`);
		for (let i = 0; i < obj['data'].length; i++) {
			console.log(`${obj['data'][i]['zip']} has population of ${obj['data'][i]['pop']}`);
		}

		this.emit('lookupByCityState', obj);
	}

	getPopulationByState(state) {
		console.log("Event getPopulationByState raised!");

		let obj = {
			'state': state,
			'data': data.reduce(function (total, row) {
				if (row['state'] == state) {
					return row['pop'] + total;
				} else {
					return total;
				}
			}, 0)
		}

		this._print_results('getPopulationByState', obj, state);
		this.emit('getPopulationByState', obj);
	}

	_print_results(method, result, ...args) {
		if (result === null) {
			console.log(`${method} ${args} - undefined`);
		} else if (typeof result === 'object' && result !== null) {
			console.log(`${method} ${args} - ${JSON.stringify(result)}`);
		} else {
			console.log(`${method} ${args} - ${result}`);
		}
	}
}

module.exports.ZipCodeEmitter = ZipCodeEmitter;
