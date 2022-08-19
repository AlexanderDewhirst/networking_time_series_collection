const EmployeeDB = require('./employeeDB.js');

const Employee = EmployeeDB.getModel();

(async() => {

	await Employee.deleteMany({});

	let employee1 = new Employee({
		firstName:'John',lastName:'Smith'
	}); 

	let employee2 = new Employee({
		firstName:'Jane',lastName:'Smith'
	}); 

	let employee3 = new Employee({
		firstName:'John',lastName:'Doe'
	}); 


	await Promise.all([
			employee1.save(), 
			employee2.save(), 
			employee3.save()
		]);

	let currentEmployees = await Employee.find({});

	console.log(currentEmployees);

	process.exit();


})();












