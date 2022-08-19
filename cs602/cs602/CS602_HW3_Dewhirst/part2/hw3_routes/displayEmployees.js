const employeeDB = require('../employeeDB.js');
const Employee = employeeDB.getModel();

// display employees

module.exports = async (req , res , next) => {
    let employees = await Employee.find({});
    let results = employees.map( emp => {
        return {
            id: emp._id,
            firstName: emp.firstName,
            lastName: emp.lastName
        }
    });

    res.render('displayEmployeesView', { title: "List of Employees", data: results });
};
