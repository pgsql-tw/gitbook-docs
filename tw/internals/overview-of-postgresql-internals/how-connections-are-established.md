# 50.2. How Connections Are Established

PostgreSQL is implemented using a simple “process per user” client/server model. In this model there is one _client process_ connected to exactly one _server process_. As we do not know ahead of time how many connections will be made, we have to use a _master process_ that spawns a new server process every time a connection is requested. This master process is called `postgres` and listens at a specified TCP/IP port for incoming connections. Whenever a request for a connection is detected the `postgres` process spawns a new server process. The server tasks communicate with each other using _semaphores_ and _shared memory_ to ensure data integrity throughout concurrent data access.

The client process can be any program that understands the PostgreSQL protocol described in [Chapter 52](https://www.postgresql.org/docs/12/protocol.html). Many clients are based on the C-language library libpq, but several independent implementations of the protocol exist, such as the Java JDBC driver.

Once a connection is established the client process can send a query to the _backend_ \(server\). The query is transmitted using plain text, i.e., there is no parsing done in the _frontend_ \(client\). The server parses the query, creates an _execution plan_, executes the plan and returns the retrieved rows to the client by transmitting them over the established connection.

