## 51.2. How Connections Are Established [#](#CONNECT-ESTAB)

PostgreSQL implements a
“process per user” client/server model.
In this model, every
[*[client process](../../appendixes/glossary/README.md#GLOSSARY-CLIENT)*](../../appendixes/glossary/README.md#GLOSSARY-CLIENT)
connects to exactly one
[*[backend process](../../appendixes/glossary/README.md#GLOSSARY-BACKEND)*](../../appendixes/glossary/README.md#GLOSSARY-BACKEND).
As we do not know ahead of time how many connections will be made,
we have to use a “supervisor process” that spawns a new
backend process every time a connection is requested. This supervisor
process is called
[*[postmaster](../../appendixes/glossary/README.md#GLOSSARY-POSTMASTER)*](../../appendixes/glossary/README.md#GLOSSARY-POSTMASTER)
and listens at a specified TCP/IP port for incoming connections.
Whenever it detects a request for a connection, it spawns a new
backend process. Those backend processes communicate with each
other and with other processes of the
[*[instance](../../appendixes/glossary/README.md#GLOSSARY-INSTANCE)*](../../appendixes/glossary/README.md#GLOSSARY-INSTANCE)
using *semaphores* and
[*[shared memory](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY)*](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY)
to ensure data integrity throughout concurrent data access.

The client process can be any program that understands the
PostgreSQL protocol described in
[Chapter 54](../protocol/README.md). Many clients are based on the
C-language library libpq, but several independent
implementations of the protocol exist, such as the Java
JDBC driver.

Once a connection is established, the client process can send a query
to the backend process it's connected to. The query is transmitted using
plain text, i.e., there is no parsing done in the client. The backend
process parses the query, creates an *execution plan*,
executes the plan, and returns the retrieved rows to the client
by transmitting them over the established connection.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/connect-estab.html)（英文原文，待翻譯）
