const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

module.exports =  async (req, res, next) => {
  employee_params = JSON.parse(JSON.stringify(req.body));
  let result = await Employee.deleteOne({ "id": employee_params._id });

  res.redirect('/employees');
};
