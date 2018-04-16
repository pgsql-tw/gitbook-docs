# 52. Frontend/Backend Protocol

PostgreSQLuses a message-based protocol for communication between frontends and backends \(clients and servers\). The protocol is supported overTCP/IPand also over Unix-domain sockets. Port number 5432 has been registered with IANA as the customary TCP port number for servers supporting this protocol, but in practice any non-privileged port number can be used.

This document describes version 3.0 of the protocol, implemented inPostgreSQL7.4 and later. For descriptions of the earlier protocol versions, see previous releases of thePostgreSQLdocumentation. A single server can support multiple protocol versions. The initial startup-request message tells the server which protocol version the client is attempting to use, and then the server follows that protocol if it is able.

In order to serve multiple clients efficiently, the server launches a new“backend”process for each client. In the current implementation, a new child process is created immediately after an incoming connection is detected. This is transparent to the protocol, however. For purposes of the protocol, the terms“backend”and“server”are interchangeable; likewise“frontend”and“client”are interchangeable.

