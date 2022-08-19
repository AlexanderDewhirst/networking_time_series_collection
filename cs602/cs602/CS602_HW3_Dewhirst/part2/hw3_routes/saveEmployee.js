const e = require('express');
const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

module.exports = async (req, res, next) => {
  employee_params = JSON.parse(JSON.stringify(req.body));

  let employee = await new Employee({
		firstName: employee_params.fname,
		lastName: employee_params.lname
	});

	employee.save(function (err, emp) {
    if (err) return console.log(err);

    console.log(`${emp.firstName} ${emp.lastName} saved.`);
  });
  res.redirect('/employees');
};
