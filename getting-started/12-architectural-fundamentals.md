# 1.2. 基礎架構[^1]

Before we proceed, you should understand the basicPostgreSQLsystem architecture. Understanding how the parts ofPostgreSQLinteract will make this chapter somewhat clearer.

In database jargon,PostgreSQLuses a client/server model. APostgreSQLsession consists of the following cooperating processes \(programs\):

* A server process, which manages the database files, accepts connections to the database from client applications, and performs database actions on behalf of the clients. The database server program is called`postgres`.

* The user's client \(frontend\) application that wants to perform database operations. Client applications can be very diverse in nature: a client could be a text-oriented tool, a graphical application, a web server that accesses the database to display web pages, or a specialized database maintenance tool. Some client applications are supplied with thePostgreSQLdistribution; most are developed by users.

As is typical of client/server applications, the client and the server can be on different hosts. In that case they communicate over a TCP/IP network connection. You should keep this in mind, because the files that can be accessed on a client machine might not be accessible \(or might only be accessible using a different file name\) on the database server machine.

ThePostgreSQLserver can handle multiple concurrent connections from clients. To achieve this it starts \(“forks”\) a new process for each connection. From that point on, the client and the new server process communicate without intervention by the original`postgres`process. Thus, the master server process is always running, waiting for client connections, whereas client and associated server processes come and go. \(All of this is of course invisible to the user. We only mention it here for completeness.\)

---



[^1]: [PostgreSQL: Documentation: 10: 1.2. Architectural Fundamentals](https://www.postgresql.org/docs/10/static/tutorial-arch.html)

