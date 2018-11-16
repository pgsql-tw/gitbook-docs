# 34.10. Control Functions

These functions control miscellaneous details of libpq's behavior.`PQclientEncoding`

Returns the client encoding.

```text
int PQclientEncoding(const PGconn *conn);
```

Note that it returns the encoding ID, not a symbolic string such as `EUC_JP`. If unsuccessful, it returns -1. To convert an encoding ID to an encoding name, you can use:

```text
char *pg_encoding_to_char(int encoding_id);
```

`PQsetClientEncoding`

Sets the client encoding.

```text
int PQsetClientEncoding(PGconn *conn, const char *encoding);
```

_`conn`_ is a connection to the server, and _`encoding`_ is the encoding you want to use. If the function successfully sets the encoding, it returns 0, otherwise -1. The current encoding for this connection can be determined by using `PQclientEncoding`.`PQsetErrorVerbosity`

Determines the verbosity of messages returned by `PQerrorMessage` and `PQresultErrorMessage`.

```text
typedef enum
{
    PQERRORS_TERSE,
    PQERRORS_DEFAULT,
    PQERRORS_VERBOSE
} PGVerbosity;

PGVerbosity PQsetErrorVerbosity(PGconn *conn, PGVerbosity verbosity);
```

`PQsetErrorVerbosity` sets the verbosity mode, returning the connection's previous setting. In _TERSE_ mode, returned messages include severity, primary text, and position only; this will normally fit on a single line. The default mode produces messages that include the above plus any detail, hint, or context fields \(these might span multiple lines\). The _VERBOSE_ mode includes all available fields. Changing the verbosity does not affect the messages available from already-existing `PGresult` objects, only subsequently-created ones. \(But see `PQresultVerboseErrorMessage` if you want to print a previous error with a different verbosity.\)`PQsetErrorContextVisibility`

Determines the handling of `CONTEXT` fields in messages returned by `PQerrorMessage` and `PQresultErrorMessage`.

```text
typedef enum
{
    PQSHOW_CONTEXT_NEVER,
    PQSHOW_CONTEXT_ERRORS,
    PQSHOW_CONTEXT_ALWAYS
} PGContextVisibility;

PGContextVisibility PQsetErrorContextVisibility(PGconn *conn, PGContextVisibility show_context);
```

`PQsetErrorContextVisibility` sets the context display mode, returning the connection's previous setting. This mode controls whether the `CONTEXT` field is included in messages \(unless the verbosity setting is _TERSE_, in which case `CONTEXT` is never shown\). The _NEVER_ mode never includes `CONTEXT`, while _ALWAYS_ always includes it if available. In _ERRORS_ mode \(the default\), `CONTEXT` fields are included only for error messages, not for notices and warnings. Changing this mode does not affect the messages available from already-existing `PGresult` objects, only subsequently-created ones. \(But see `PQresultVerboseErrorMessage` if you want to print a previous error with a different display mode.\)`PQtrace`

Enables tracing of the client/server communication to a debugging file stream.

```text
void PQtrace(PGconn *conn, FILE *stream);
```

#### Note

On Windows, if the libpq library and an application are compiled with different flags, this function call will crash the application because the internal representation of the `FILE`pointers differ. Specifically, multithreaded/single-threaded, release/debug, and static/dynamic flags should be the same for the library and all applications using that library.`PQuntrace`

Disables tracing started by `PQtrace`.

```text
void PQuntrace(PGconn *conn);
```

