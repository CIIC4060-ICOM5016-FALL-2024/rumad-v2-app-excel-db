# Data Access Layer
Provides the interface between the business-logic 
layer and the underlying database.
Hides the details of interfacing with the database.
Anything SQL goes here.


## Data Access Objects
Objects with methods that allow interfacing with a database without
exposing the database details. These objects allow to create,
read, update and delete (CRUD) the tuples of a relation. Any SQL operations
must be inside these objects.
### Connection Pooling
The DAO's share a connection pool of open connections.
When a transaction needs a connection, the pool lends an
open connection for the DAO to use.
When the DAO is finished, the
connection automatically returns to the pool.
## Handlers
The handlers are what connect the Data Access Layer with the
Business Layer (Model).
Handlers interfaces with the DAO for CRUD operations and return JSON responses.
The handlers are responsible for error handling.