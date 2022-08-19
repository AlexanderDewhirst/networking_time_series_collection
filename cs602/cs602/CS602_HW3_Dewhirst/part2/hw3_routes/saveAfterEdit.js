const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

module.exports = async (req, res, next) => {
    employee_params = JSON.parse(JSON.stringify(req.body));
    let employee = await Employee.updateOne(
        { "id": employee_params._id },
        { $set: { firstName: employee_params.fname, lastName: employee_params.lname }}
    );

    res.redirect('/employees');
};
