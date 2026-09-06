## Chapter 32. libpq — C Library

**Table of Contents**

[32.1. Database Connection Control Functions](libpq-connect.md)
:   [32.1.1. Connection Strings](libpq-connect.md#LIBPQ-CONNSTRING)

    [32.1.2. Parameter Key Words](libpq-connect.md#LIBPQ-PARAMKEYWORDS)

[32.2. Connection Status Functions](libpq-status.md)

[32.3. Command Execution Functions](libpq-exec.md)
:   [32.3.1. Main Functions](libpq-exec.md#LIBPQ-EXEC-MAIN)

    [32.3.2. Retrieving Query Result Information](libpq-exec.md#LIBPQ-EXEC-SELECT-INFO)

    [32.3.3. Retrieving Other Result Information](libpq-exec.md#LIBPQ-EXEC-NONSELECT)

    [32.3.4. Escaping Strings for Inclusion in SQL Commands](libpq-exec.md#LIBPQ-EXEC-ESCAPE-STRING)

[32.4. Asynchronous Command Processing](libpq-async.md)

[32.5. Pipeline Mode](libpq-pipeline-mode.md)
:   [32.5.1. Using Pipeline Mode](libpq-pipeline-mode.md#LIBPQ-PIPELINE-USING)

    [32.5.2. Functions Associated with Pipeline Mode](libpq-pipeline-mode.md#LIBPQ-PIPELINE-FUNCTIONS)

    [32.5.3. When to Use Pipeline Mode](libpq-pipeline-mode.md#LIBPQ-PIPELINE-TIPS)

[32.6. Retrieving Query Results in Chunks](libpq-single-row-mode.md)

[32.7. Canceling Queries in Progress](libpq-cancel.md)
:   [32.7.1. Functions for Sending Cancel Requests](libpq-cancel.md#LIBPQ-CANCEL-FUNCTIONS)

    [32.7.2. Obsolete Functions for Sending Cancel Requests](libpq-cancel.md#LIBPQ-CANCEL-DEPRECATED)

[32.8. The Fast-Path Interface](libpq-fastpath.md)

[32.9. Asynchronous Notification](libpq-notify.md)

[32.10. Functions Associated with the `COPY` Command](libpq-copy.md)
:   [32.10.1. Functions for Sending `COPY` Data](libpq-copy.md#LIBPQ-COPY-SEND)

    [32.10.2. Functions for Receiving `COPY` Data](libpq-copy.md#LIBPQ-COPY-RECEIVE)

    [32.10.3. Obsolete Functions for `COPY`](libpq-copy.md#LIBPQ-COPY-DEPRECATED)

[32.11. Control Functions](libpq-control.md)

[32.12. Miscellaneous Functions](libpq-misc.md)

[32.13. Notice Processing](libpq-notice-processing.md)

[32.14. Event System](libpq-events.md)
:   [32.14.1. Event Types](libpq-events.md#LIBPQ-EVENTS-TYPES)

    [32.14.2. Event Callback Procedure](libpq-events.md#LIBPQ-EVENTS-PROC)

    [32.14.3. Event Support Functions](libpq-events.md#LIBPQ-EVENTS-FUNCS)

    [32.14.4. Event Example](libpq-events.md#LIBPQ-EVENTS-EXAMPLE)

[32.15. Environment Variables](libpq-envars.md)

[32.16. The Password File](libpq-pgpass.md)

[32.17. The Connection Service File](libpq-pgservice.md)

[32.18. LDAP Lookup of Connection Parameters](libpq-ldap.md)

[32.19. SSL Support](libpq-ssl.md)
:   [32.19.1. Client Verification of Server Certificates](libpq-ssl.md#LIBQ-SSL-CERTIFICATES)

    [32.19.2. Client Certificates](libpq-ssl.md#LIBPQ-SSL-CLIENTCERT)

    [32.19.3. Protection Provided in Different Modes](libpq-ssl.md#LIBPQ-SSL-PROTECTION)

    [32.19.4. SSL Client File Usage](libpq-ssl.md#LIBPQ-SSL-FILEUSAGE)

    [32.19.5. SSL Library Initialization](libpq-ssl.md#LIBPQ-SSL-INITIALIZE)

[32.20. OAuth Support](libpq-oauth.md)
:   [32.20.1. Authdata Hooks](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)

    [32.20.2. Debugging and Developer Settings](libpq-oauth.md#LIBPQ-OAUTH-DEBUGGING)

[32.21. Behavior in Threaded Programs](libpq-threading.md)

[32.22. Building libpq Programs](libpq-build.md)

[32.23. Example Programs](libpq-example.md)

<a id="id-1.7.3.2"></a><a id="id-1.7.3.3"></a>

libpq is the C
application programmer's interface to PostgreSQL.
libpq is a set of library functions that allow
client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.

libpq is also the underlying engine for several
other PostgreSQL application interfaces, including
those written for C++, Perl, Python, Tcl and ECPG.
So some aspects of libpq's behavior will be
important to you if you use one of those packages. In particular,
[Section 32.15](libpq-envars.md),
[Section 32.16](libpq-pgpass.md) and
[Section 32.19](libpq-ssl.md)
describe behavior that is visible to the user of any application
that uses libpq.

Some short programs are included at the end of this chapter ([Section 32.23](libpq-example.md)) to show how
to write programs that use libpq. There are also several
complete examples of libpq applications in the
directory `src/test/examples` in the source code distribution.

Client programs that use libpq must
include the header file
`libpq-fe.h`<a id="id-1.7.3.7.3"></a>
and must link with the libpq library.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq.html)（英文原文，待翻譯）
