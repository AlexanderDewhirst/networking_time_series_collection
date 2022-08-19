## CS602 Term Project
For my course project, I intend on building an inventory management application. Each item has a unique identifier, name, description, quantity, price, and store. A store owner has the ability to view the inventory for his stores and not other stores. The store owner has the ability to create, update, and delete products from their store using the user interface.

An administrator has the ability to view all products across all stores. However, they cannot modify a product for any store. The administrator’s role is inventory visibility for reporting purposes.

The NodeJS application will support standard REST protocol and data will persist in MongoDB.


### Getting Started
Install the Mongo client and start a local server at the default port.

Seed the Mongo database with
```
node init_db.js
```

Run the application with
```
node server.js
```
