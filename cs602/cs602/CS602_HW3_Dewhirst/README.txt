Run npm install for both part1 and part2 to install the node dependency modules.

Complete the missing functionaility for part1 and part2


Part1 Modifications:

 1) mongo_zipCodeModule_v2.js  
      - Code for lookupByZipCode already provided
      - Complete the code for lookupByCityState and getPopulationByState

 2) Test by running 
       node client.js

 3) server.js - Complete the code for /city... and /pop...

 4) views - Copy from Assignment2 the following files
       lookupByCityStateView.handlebars
       populationView.handlebars


Part2 Modifications:

 1) employeeDB.js  - Fill in the schema definition for firstName and lastName

 2) Populate initial data to your collection by running
        node initDB.js

 3) hw3_routes  - Fill in the code for the following
       addEmployee.js  (render addEmployeeView)
       saveEmpoyee.js  (save the employee to the database)
       deleteEmployee.js  (Find the employee by id and render the deleteEmployeeView for confirmation)
       deleteEmployeeAfterConfirm.js (Find the employee by id, remove from the database, and redirect to /employees)
       editEmployee.js (Find the employee by id and render the editEmployeeView with form populated with the current values)
       saveAfterEdit.js (Find the employee by id, change the employee's properties with the new values, save to the database, and redirect to /employees

	
       
      