const net = require('net');
const colors = require('colors');
const cities = require('./zipCodeModule_v2');

const server = net.createServer((socket) => {

	console.log("Client connection...".red);

	socket.on('end', () => {
		console.log("Client disconnected...".red);
	});

	socket.on('data', (data) => {
		const input = data.toString();
		console.log('Received %s', input);

		let command = input.split(',');
		command = command.map((val) => {
			return val.trim();
		})
		console.log(command);

		if (command[0] == "lookupByZipCode") {
			if (command.length != 2) {
				console.log("Invalid arguments");
				socket.write("Invalid arguments");
			}
			const zip = parseInt(command[1]);
			if (isNaN(zip) == true) {
				console.log("Invalid zipcode");
				socket.write("Invalid zipcode");
			}
			let zip_reponse = JSON.stringify(cities.lookupByZipCode(zip));

			socket.write(zip_reponse);
			console.log(zip_reponse);

		} else if (command[0] == "lookupByCityState") {
			if (command.length != 3) {
				console.log("Invalid arguments");
				socket.write("Invalid arguments");
			}
			const city = command[1];
			const state = command[2];
			let city_state_response = JSON.stringify(cities.lookupByCityState(city, state));

			socket.write(city_state_response);
			console.log(city_state_response);

		} else if (command[0] == "getPopulationByState") {
			console.log(command.length)
			if (command.length != 2) {
				console.log("Invalid arguments");
				socket.write("Invalid arguments");
			}
			const state = command[1];
			let population_response = JSON.stringify(cities.getPopulationByState(state));

			socket.write(population_response);
			console.log(population_response);

		} else {
			socket.write("Command not found.");
			console.log("Command not found.");
		}
	});
});

// listen for client connections
server.listen(3000, () => {
	console.log("Listening for connections on port 3000");
});
