const e = require('express');
const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

module.exports = (req, res, next) => {
	res.render('addEmployeeView');
};
