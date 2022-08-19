const e = require('express');
const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

module.exports = async (req, res, next) => {
  let employee_params = JSON.parse(JSON.stringify(req.params));

  let employee = await Employee.findOne(
      { "_id": employee_params.id }
  )

  let result = { id: employee._id, firstName: employee.firstName, lastName: employee.lastName }
  res.render('deleteEmployeeView', { data: result });
};
