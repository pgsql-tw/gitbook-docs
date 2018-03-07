# 33. libpq - C Library[^1]

**Table of Contents**

[33.1. Database Connection Control Functions](https://www.postgresql.org/docs/10/static/libpq-connect.html)

[33.1.1. Connection Strings](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNSTRING)

[33.1.2. Parameter Key Words](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)

[33.2. Connection Status Functions](https://www.postgresql.org/docs/10/static/libpq-status.html)

[33.3. Command Execution Functions](https://www.postgresql.org/docs/10/static/libpq-exec.html)

[33.3.1. Main Functions](https://www.postgresql.org/docs/10/static/libpq-exec.html#LIBPQ-EXEC-MAIN)

[33.3.2. Retrieving Query Result Information](https://www.postgresql.org/docs/10/static/libpq-exec.html#LIBPQ-EXEC-SELECT-INFO)

[33.3.3. Retrieving Other Result Information](https://www.postgresql.org/docs/10/static/libpq-exec.html#LIBPQ-EXEC-NONSELECT)

[33.3.4. Escaping Strings for Inclusion in SQL Commands](https://www.postgresql.org/docs/10/static/libpq-exec.html#LIBPQ-EXEC-ESCAPE-STRING)

[33.4. Asynchronous Command Processing](https://www.postgresql.org/docs/10/static/libpq-async.html)

[33.5. Retrieving Query Results Row-By-Row](https://www.postgresql.org/docs/10/static/libpq-single-row-mode.html)

[33.6. Canceling Queries in Progress](https://www.postgresql.org/docs/10/static/libpq-cancel.html)

[33.7. The Fast-Path Interface](https://www.postgresql.org/docs/10/static/libpq-fastpath.html)

[33.8. Asynchronous Notification](https://www.postgresql.org/docs/10/static/libpq-notify.html)

[33.9. Functions Associated with the`COPY`Command](https://www.postgresql.org/docs/10/static/libpq-copy.html)

[33.9.1. Functions for Sending`COPY`Data](https://www.postgresql.org/docs/10/static/libpq-copy.html#LIBPQ-COPY-SEND)

[33.9.2. Functions for Receiving`COPY`Data](https://www.postgresql.org/docs/10/static/libpq-copy.html#LIBPQ-COPY-RECEIVE)

[33.9.3. Obsolete Functions for`COPY`](https://www.postgresql.org/docs/10/static/libpq-copy.html#LIBPQ-COPY-DEPRECATED)

[33.10. Control Functions](https://www.postgresql.org/docs/10/static/libpq-control.html)

[33.11. Miscellaneous Functions](https://www.postgresql.org/docs/10/static/libpq-misc.html)

[33.12. Notice Processing](https://www.postgresql.org/docs/10/static/libpq-notice-processing.html)

[33.13. Event System](https://www.postgresql.org/docs/10/static/libpq-events.html)

[33.13.1. Event Types](https://www.postgresql.org/docs/10/static/libpq-events.html#LIBPQ-EVENTS-TYPES)

[33.13.2. Event Callback Procedure](https://www.postgresql.org/docs/10/static/libpq-events.html#LIBPQ-EVENTS-PROC)

[33.13.3. Event Support Functions](https://www.postgresql.org/docs/10/static/libpq-events.html#LIBPQ-EVENTS-FUNCS)

[33.13.4. Event Example](https://www.postgresql.org/docs/10/static/libpq-events.html#LIBPQ-EVENTS-EXAMPLE)

[33.14. Environment Variables](https://www.postgresql.org/docs/10/static/libpq-envars.html)

[33.15. The Password File](https://www.postgresql.org/docs/10/static/libpq-pgpass.html)

[33.16. The Connection Service File](https://www.postgresql.org/docs/10/static/libpq-pgservice.html)

[33.17. LDAP Lookup of Connection Parameters](https://www.postgresql.org/docs/10/static/libpq-ldap.html)

[33.18. SSL Support](https://www.postgresql.org/docs/10/static/libpq-ssl.html)

[33.18.1. Client Verification of Server Certificates](https://www.postgresql.org/docs/10/static/libpq-ssl.html#LIBQ-SSL-CERTIFICATES)

[33.18.2. Client Certificates](https://www.postgresql.org/docs/10/static/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT)

[33.18.3. Protection Provided in Different Modes](https://www.postgresql.org/docs/10/static/libpq-ssl.html#LIBPQ-SSL-PROTECTION)

[33.18.4. SSL Client File Usage](https://www.postgresql.org/docs/10/static/libpq-ssl.html#LIBPQ-SSL-FILEUSAGE)

[33.18.5. SSL Library Initialization](https://www.postgresql.org/docs/10/static/libpq-ssl.html#LIBPQ-SSL-INITIALIZE)

[33.19. Behavior in Threaded Programs](https://www.postgresql.org/docs/10/static/libpq-threading.html)

[33.20. BuildinglibpqPrograms](https://www.postgresql.org/docs/10/static/libpq-build.html)

[33.21. Example Programs](https://www.postgresql.org/docs/10/static/libpq-example.html)





libpqis theCapplication programmer's interface toPostgreSQL.libpqis a set of library functions that allow client programs to pass queries to thePostgreSQLbackend server and to receive the results of these queries.

libpqis also the underlying engine for several otherPostgreSQLapplication interfaces, including those written for C++, Perl, Python, Tcl andECPG. So some aspects oflibpq's behavior will be important to you if you use one of those packages. In particular,[Section 33.14](https://www.postgresql.org/docs/10/static/libpq-envars.html),[Section 33.15](https://www.postgresql.org/docs/10/static/libpq-pgpass.html)and[Section 33.18](https://www.postgresql.org/docs/10/static/libpq-ssl.html)describe behavior that is visible to the user of any application that useslibpq.

Some short programs are included at the end of this chapter \([Section 33.21](https://www.postgresql.org/docs/10/static/libpq-example.html)\) to show how to write programs that uselibpq. There are also several complete examples oflibpqapplications in the directory`src/test/examples`in the source code distribution.

Client programs that uselibpqmust include the header file`libpq-fe.h`and must link with thelibpqlibrary.

---



[^1]:  [PostgreSQL: Documentation: 10: Chapter 33. libpq - C Library](https://www.postgresql.org/docs/10/static/libpq.html)

