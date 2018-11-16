# 34.3. Command Execution Functions

Once a connection to a database server has been successfully established, the functions described here are used to perform SQL queries and commands.

#### 33.3.1. Main Functions

`PQexec`

Submits a command to the server and waits for the result.

```text
PGresult *PQexec(PGconn *conn, const char *command);
```

Returns a `PGresult` pointer or possibly a null pointer. A non-null pointer will generally be returned except in out-of-memory conditions or serious errors such as inability to send the command to the server. The `PQresultStatus` function should be called to check the return value for any errors \(including the value of a null pointer, in which case it will return `PGRES_FATAL_ERROR`\). Use `PQerrorMessage` to get more information about such errors.

The command string can include multiple SQL commands \(separated by semicolons\). Multiple queries sent in a single `PQexec` call are processed in a single transaction, unless there are explicit `BEGIN`/`COMMIT` commands included in the query string to divide it into multiple transactions. Note however that the returned `PGresult` structure describes only the result of the last command executed from the string. Should one of the commands fail, processing of the string stops with it and the returned `PGresult` describes the error condition.`PQexecParams`

Submits a command to the server and waits for the result, with the ability to pass parameters separately from the SQL command text.

```text
PGresult *PQexecParams(PGconn *conn,
                       const char *command,
                       int nParams,
                       const Oid *paramTypes,
                       const char * const *paramValues,
                       const int *paramLengths,
                       const int *paramFormats,
                       int resultFormat);
```

`PQexecParams` is like `PQexec`, but offers additional functionality: parameter values can be specified separately from the command string proper, and query results can be requested in either text or binary format. `PQexecParams` is supported only in protocol 3.0 and later connections; it will fail when using protocol 2.0.

The function arguments are:_`conn`_

The connection object to send the command through._`command`_

The SQL command string to be executed. If parameters are used, they are referred to in the command string as `$1`, `$2`, etc._`nParams`_

The number of parameters supplied; it is the length of the arrays _`paramTypes[]`_, _`paramValues[]`_, _`paramLengths[]`_, and _`paramFormats[]`_. \(The array pointers can be `NULL` when _`nParams`_ is zero.\)_`paramTypes[]`_

Specifies, by OID, the data types to be assigned to the parameter symbols. If _`paramTypes`_ is `NULL`, or any particular element in the array is zero, the server infers a data type for the parameter symbol in the same way it would do for an untyped literal string._`paramValues[]`_

Specifies the actual values of the parameters. A null pointer in this array means the corresponding parameter is null; otherwise the pointer points to a zero-terminated text string \(for text format\) or binary data in the format expected by the server \(for binary format\)._`paramLengths[]`_

Specifies the actual data lengths of binary-format parameters. It is ignored for null parameters and text-format parameters. The array pointer can be null when there are no binary parameters._`paramFormats[]`_

Specifies whether parameters are text \(put a zero in the array entry for the corresponding parameter\) or binary \(put a one in the array entry for the corresponding parameter\). If the array pointer is null then all parameters are presumed to be text strings.

Values passed in binary format require knowledge of the internal representation expected by the backend. For example, integers must be passed in network byte order. Passing `numeric` values requires knowledge of the server storage format, as implemented in `src/backend/utils/adt/numeric.c::numeric_send()` and `src/backend/utils/adt/numeric.c::numeric_recv()`._`resultFormat`_

Specify zero to obtain results in text format, or one to obtain results in binary format. \(There is not currently a provision to obtain different result columns in different formats, although that is possible in the underlying protocol.\)

The primary advantage of `PQexecParams` over `PQexec` is that parameter values can be separated from the command string, thus avoiding the need for tedious and error-prone quoting and escaping.

Unlike `PQexec`, `PQexecParams` allows at most one SQL command in the given string. \(There can be semicolons in it, but not more than one nonempty command.\) This is a limitation of the underlying protocol, but has some usefulness as an extra defense against SQL-injection attacks.

#### Tip

Specifying parameter types via OIDs is tedious, particularly if you prefer not to hard-wire particular OID values into your program. However, you can avoid doing so even in cases where the server by itself cannot determine the type of the parameter, or chooses a different type than you want. In the SQL command text, attach an explicit cast to the parameter symbol to show what data type you will send. For example:

```text
SELECT * FROM mytable WHERE x = $1::bigint;
```

This forces parameter `$1` to be treated as `bigint`, whereas by default it would be assigned the same type as `x`. Forcing the parameter type decision, either this way or by specifying a numeric type OID, is strongly recommended when sending parameter values in binary format, because binary format has less redundancy than text format and so there is less chance that the server will detect a type mismatch mistake for you.`PQprepare`

Submits a request to create a prepared statement with the given parameters, and waits for completion.

```text
PGresult *PQprepare(PGconn *conn,
                    const char *stmtName,
                    const char *query,
                    int nParams,
                    const Oid *paramTypes);
```

`PQprepare` creates a prepared statement for later execution with `PQexecPrepared`. This feature allows commands to be executed repeatedly without being parsed and planned each time; see [PREPARE](https://www.postgresql.org/docs/10/static/sql-prepare.html) for details. `PQprepare` is supported only in protocol 3.0 and later connections; it will fail when using protocol 2.0.

The function creates a prepared statement named _`stmtName`_ from the _`query`_ string, which must contain a single SQL command. _`stmtName`_ can be `""` to create an unnamed statement, in which case any pre-existing unnamed statement is automatically replaced; otherwise it is an error if the statement name is already defined in the current session. If any parameters are used, they are referred to in the query as `$1`, `$2`, etc. _`nParams`_ is the number of parameters for which types are pre-specified in the array _`paramTypes[]`_. \(The array pointer can be `NULL` when _`nParams`_ is zero.\) _`paramTypes[]`_ specifies, by OID, the data types to be assigned to the parameter symbols. If _`paramTypes`_ is `NULL`, or any particular element in the array is zero, the server assigns a data type to the parameter symbol in the same way it would do for an untyped literal string. Also, the query can use parameter symbols with numbers higher than _`nParams`_; data types will be inferred for these symbols as well. \(See `PQdescribePrepared` for a means to find out what data types were inferred.\)

As with `PQexec`, the result is normally a `PGresult` object whose contents indicate server-side success or failure. A null result indicates out-of-memory or inability to send the command at all. Use `PQerrorMessage` to get more information about such errors.

Prepared statements for use with `PQexecPrepared` can also be created by executing SQL [PREPARE](https://www.postgresql.org/docs/10/static/sql-prepare.html) statements. Also, although there is no libpq function for deleting a prepared statement, the SQL [DEALLOCATE](https://www.postgresql.org/docs/10/static/sql-deallocate.html) statement can be used for that purpose.`PQexecPrepared`

Sends a request to execute a prepared statement with given parameters, and waits for the result.

```text
PGresult *PQexecPrepared(PGconn *conn,
                         const char *stmtName,
                         int nParams,
                         const char * const *paramValues,
                         const int *paramLengths,
                         const int *paramFormats,
                         int resultFormat);
```

`PQexecPrepared` is like `PQexecParams`, but the command to be executed is specified by naming a previously-prepared statement, instead of giving a query string. This feature allows commands that will be used repeatedly to be parsed and planned just once, rather than each time they are executed. The statement must have been prepared previously in the current session. `PQexecPrepared` is supported only in protocol 3.0 and later connections; it will fail when using protocol 2.0.

The parameters are identical to `PQexecParams`, except that the name of a prepared statement is given instead of a query string, and the _`paramTypes[]`_ parameter is not present \(it is not needed since the prepared statement's parameter types were determined when it was created\).`PQdescribePrepared`

Submits a request to obtain information about the specified prepared statement, and waits for completion.

```text
PGresult *PQdescribePrepared(PGconn *conn, const char *stmtName);
```

`PQdescribePrepared` allows an application to obtain information about a previously prepared statement. `PQdescribePrepared` is supported only in protocol 3.0 and later connections; it will fail when using protocol 2.0.

_`stmtName`_ can be `""` or `NULL` to reference the unnamed statement, otherwise it must be the name of an existing prepared statement. On success, a `PGresult` with status `PGRES_COMMAND_OK` is returned. The functions `PQnparams` and `PQparamtype` can be applied to this `PGresult` to obtain information about the parameters of the prepared statement, and the functions `PQnfields`, `PQfname`, `PQftype`, etc provide information about the result columns \(if any\) of the statement.`PQdescribePortal`

Submits a request to obtain information about the specified portal, and waits for completion.

```text
PGresult *PQdescribePortal(PGconn *conn, const char *portalName);
```

`PQdescribePortal` allows an application to obtain information about a previously created portal. \(libpq does not provide any direct access to portals, but you can use this function to inspect the properties of a cursor created with a `DECLARE CURSOR` SQL command.\) `PQdescribePortal` is supported only in protocol 3.0 and later connections; it will fail when using protocol 2.0.

_`portalName`_ can be `""` or `NULL` to reference the unnamed portal, otherwise it must be the name of an existing portal. On success, a `PGresult` with status `PGRES_COMMAND_OK` is returned. The functions `PQnfields`, `PQfname`, `PQftype`, etc can be applied to the `PGresult` to obtain information about the result columns \(if any\) of the portal.

The `PGresult` structure encapsulates the result returned by the server. libpq application programmers should be careful to maintain the `PGresult` abstraction. Use the accessor functions below to get at the contents of `PGresult`. Avoid directly referencing the fields of the `PGresult` structure because they are subject to change in the future.`PQresultStatus`

Returns the result status of the command.

```text
ExecStatusType PQresultStatus(const PGresult *res);
```

`PQresultStatus` can return one of the following values:`PGRES_EMPTY_QUERY`

The string sent to the server was empty.`PGRES_COMMAND_OK`

Successful completion of a command returning no data.`PGRES_TUPLES_OK`

Successful completion of a command returning data \(such as a `SELECT` or `SHOW`\).`PGRES_COPY_OUT`

Copy Out \(from server\) data transfer started.`PGRES_COPY_IN`

Copy In \(to server\) data transfer started.`PGRES_BAD_RESPONSE`

The server's response was not understood.`PGRES_NONFATAL_ERROR`

A nonfatal error \(a notice or warning\) occurred.`PGRES_FATAL_ERROR`

A fatal error occurred.`PGRES_COPY_BOTH`

Copy In/Out \(to and from server\) data transfer started. This feature is currently used only for streaming replication, so this status should not occur in ordinary applications.`PGRES_SINGLE_TUPLE`

The `PGresult` contains a single result tuple from the current command. This status occurs only when single-row mode has been selected for the query \(see [Section 33.5](https://www.postgresql.org/docs/10/static/libpq-single-row-mode.html)\).

If the result status is `PGRES_TUPLES_OK` or `PGRES_SINGLE_TUPLE`, then the functions described below can be used to retrieve the rows returned by the query. Note that a `SELECT`command that happens to retrieve zero rows still shows `PGRES_TUPLES_OK`. `PGRES_COMMAND_OK` is for commands that can never return rows \(`INSERT` or `UPDATE` without a `RETURNING`clause, etc.\). A response of `PGRES_EMPTY_QUERY` might indicate a bug in the client software.

A result of status `PGRES_NONFATAL_ERROR` will never be returned directly by `PQexec` or other query execution functions; results of this kind are instead passed to the notice processor \(see [Section 33.12](https://www.postgresql.org/docs/10/static/libpq-notice-processing.html)\).`PQresStatus`

Converts the enumerated type returned by `PQresultStatus` into a string constant describing the status code. The caller should not free the result.

```text
char *PQresStatus(ExecStatusType status);
```

`PQresultErrorMessage`

Returns the error message associated with the command, or an empty string if there was no error.

```text
char *PQresultErrorMessage(const PGresult *res);
```

If there was an error, the returned string will include a trailing newline. The caller should not free the result directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.

Immediately following a `PQexec` or `PQgetResult` call, `PQerrorMessage` \(on the connection\) will return the same string as `PQresultErrorMessage` \(on the result\). However, a `PGresult`will retain its error message until destroyed, whereas the connection's error message will change when subsequent operations are done. Use `PQresultErrorMessage` when you want to know the status associated with a particular `PGresult`; use `PQerrorMessage` when you want to know the status from the latest operation on the connection.`PQresultVerboseErrorMessage`

Returns a reformatted version of the error message associated with a `PGresult` object.

```text
char *PQresultVerboseErrorMessage(const PGresult *res,
                                  PGVerbosity verbosity,
                                  PGContextVisibility show_context);
```

In some situations a client might wish to obtain a more detailed version of a previously-reported error. `PQresultVerboseErrorMessage` addresses this need by computing the message that would have been produced by `PQresultErrorMessage` if the specified verbosity settings had been in effect for the connection when the given `PGresult` was generated. If the `PGresult` is not an error result, “PGresult is not an error result” is reported instead. The returned string includes a trailing newline.

Unlike most other functions for extracting data from a `PGresult`, the result of this function is a freshly allocated string. The caller must free it using `PQfreemem()` when the string is no longer needed.

A NULL return is possible if there is insufficient memory.`PQresultErrorField`

Returns an individual field of an error report.

```text
char *PQresultErrorField(const PGresult *res, int fieldcode);
```

_`fieldcode`_ is an error field identifier; see the symbols listed below. `NULL` is returned if the `PGresult` is not an error or warning result, or does not include the specified field. Field values will normally not include a trailing newline. The caller should not free the result directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.

The following field codes are available:`PG_DIAG_SEVERITY`

The severity; the field contents are `ERROR`, `FATAL`, or `PANIC` \(in an error message\), or `WARNING`, `NOTICE`, `DEBUG`, `INFO`, or `LOG` \(in a notice message\), or a localized translation of one of these. Always present.`PG_DIAG_SEVERITY_NONLOCALIZED`

The severity; the field contents are `ERROR`, `FATAL`, or `PANIC` \(in an error message\), or `WARNING`, `NOTICE`, `DEBUG`, `INFO`, or `LOG` \(in a notice message\). This is identical to the `PG_DIAG_SEVERITY` field except that the contents are never localized. This is present only in reports generated by PostgreSQL versions 9.6 and later.`PG_DIAG_SQLSTATE`

The SQLSTATE code for the error. The SQLSTATE code identifies the type of error that has occurred; it can be used by front-end applications to perform specific operations \(such as error handling\) in response to a particular database error. For a list of the possible SQLSTATE codes, see [Appendix A](https://www.postgresql.org/docs/10/static/errcodes-appendix.html). This field is not localizable, and is always present.`PG_DIAG_MESSAGE_PRIMARY`

The primary human-readable error message \(typically one line\). Always present.`PG_DIAG_MESSAGE_DETAIL`

Detail: an optional secondary error message carrying more detail about the problem. Might run to multiple lines.`PG_DIAG_MESSAGE_HINT`

Hint: an optional suggestion what to do about the problem. This is intended to differ from detail in that it offers advice \(potentially inappropriate\) rather than hard facts. Might run to multiple lines.`PG_DIAG_STATEMENT_POSITION`

A string containing a decimal integer indicating an error cursor position as an index into the original statement string. The first character has index 1, and positions are measured in characters not bytes.`PG_DIAG_INTERNAL_POSITION`

This is defined the same as the `PG_DIAG_STATEMENT_POSITION` field, but it is used when the cursor position refers to an internally generated command rather than the one submitted by the client. The `PG_DIAG_INTERNAL_QUERY` field will always appear when this field appears.`PG_DIAG_INTERNAL_QUERY`

The text of a failed internally-generated command. This could be, for example, a SQL query issued by a PL/pgSQL function.`PG_DIAG_CONTEXT`

An indication of the context in which the error occurred. Presently this includes a call stack traceback of active procedural language functions and internally-generated queries. The trace is one entry per line, most recent first.`PG_DIAG_SCHEMA_NAME`

If the error was associated with a specific database object, the name of the schema containing that object, if any.`PG_DIAG_TABLE_NAME`

If the error was associated with a specific table, the name of the table. \(Refer to the schema name field for the name of the table's schema.\)`PG_DIAG_COLUMN_NAME`

If the error was associated with a specific table column, the name of the column. \(Refer to the schema and table name fields to identify the table.\)`PG_DIAG_DATATYPE_NAME`

If the error was associated with a specific data type, the name of the data type. \(Refer to the schema name field for the name of the data type's schema.\)`PG_DIAG_CONSTRAINT_NAME`

If the error was associated with a specific constraint, the name of the constraint. Refer to fields listed above for the associated table or domain. \(For this purpose, indexes are treated as constraints, even if they weren't created with constraint syntax.\)`PG_DIAG_SOURCE_FILE`

The file name of the source-code location where the error was reported.`PG_DIAG_SOURCE_LINE`

The line number of the source-code location where the error was reported.`PG_DIAG_SOURCE_FUNCTION`

The name of the source-code function reporting the error.

#### Note

The fields for schema name, table name, column name, data type name, and constraint name are supplied only for a limited number of error types; see [Appendix A](https://www.postgresql.org/docs/10/static/errcodes-appendix.html). Do not assume that the presence of any of these fields guarantees the presence of another field. Core error sources observe the interrelationships noted above, but user-defined functions may use these fields in other ways. In the same vein, do not assume that these fields denote contemporary objects in the current database.

The client is responsible for formatting displayed information to meet its needs; in particular it should break long lines as needed. Newline characters appearing in the error message fields should be treated as paragraph breaks, not line breaks.

Errors generated internally by libpq will have severity and primary message, but typically no other fields. Errors returned by a pre-3.0-protocol server will include severity and primary message, and sometimes a detail message, but no other fields.

Note that error fields are only available from `PGresult` objects, not `PGconn` objects; there is no `PQerrorField` function.`PQclear`

Frees the storage associated with a `PGresult`. Every command result should be freed via `PQclear` when it is no longer needed.

```text
void PQclear(PGresult *res);
```

You can keep a `PGresult` object around for as long as you need it; it does not go away when you issue a new command, nor even if you close the connection. To get rid of it, you must call `PQclear`. Failure to do this will result in memory leaks in your application.

#### 33.3.2. Retrieving Query Result Information

These functions are used to extract information from a `PGresult` object that represents a successful query result \(that is, one that has status `PGRES_TUPLES_OK` or `PGRES_SINGLE_TUPLE`\). They can also be used to extract information from a successful Describe operation: a Describe's result has all the same column information that actual execution of the query would provide, but it has zero rows. For objects with other status values, these functions will act as though the result has zero rows and zero columns.`PQntuples`

Returns the number of rows \(tuples\) in the query result. \(Note that `PGresult` objects are limited to no more than `INT_MAX` rows, so an `int` result is sufficient.\)

```text
int PQntuples(const PGresult *res);
```

`PQnfields`

Returns the number of columns \(fields\) in each row of the query result.

```text
int PQnfields(const PGresult *res);
```

`PQfname`

Returns the column name associated with the given column number. Column numbers start at 0. The caller should not free the result directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.

```text
char *PQfname(const PGresult *res,
              int column_number);
```

`NULL` is returned if the column number is out of range.`PQfnumber`

Returns the column number associated with the given column name.

```text
int PQfnumber(const PGresult *res,
              const char *column_name);
```

-1 is returned if the given name does not match any column.

The given name is treated like an identifier in an SQL command, that is, it is downcased unless double-quoted. For example, given a query result generated from the SQL command:

```text
SELECT 1 AS FOO, 2 AS "BAR";
```

we would have the results:

```text
PQfname(res, 0)              foo
PQfname(res, 1)              BAR
PQfnumber(res, "FOO")        0
PQfnumber(res, "foo")        0
PQfnumber(res, "BAR")        -1
PQfnumber(res, "\"BAR\"")    1
```

`PQftable`

Returns the OID of the table from which the given column was fetched. Column numbers start at 0.

```text
Oid PQftable(const PGresult *res,
             int column_number);
```

`InvalidOid` is returned if the column number is out of range, or if the specified column is not a simple reference to a table column, or when using pre-3.0 protocol. You can query the system table `pg_class` to determine exactly which table is referenced.

The type `Oid` and the constant `InvalidOid` will be defined when you include the libpq header file. They will both be some integer type.`PQftablecol`

Returns the column number \(within its table\) of the column making up the specified query result column. Query-result column numbers start at 0, but table columns have nonzero numbers.

```text
int PQftablecol(const PGresult *res,
                int column_number);
```

Zero is returned if the column number is out of range, or if the specified column is not a simple reference to a table column, or when using pre-3.0 protocol.`PQfformat`

Returns the format code indicating the format of the given column. Column numbers start at 0.

```text
int PQfformat(const PGresult *res,
              int column_number);
```

Format code zero indicates textual data representation, while format code one indicates binary representation. \(Other codes are reserved for future definition.\)`PQftype`

Returns the data type associated with the given column number. The integer returned is the internal OID number of the type. Column numbers start at 0.

```text
Oid PQftype(const PGresult *res,
            int column_number);
```

You can query the system table `pg_type` to obtain the names and properties of the various data types. The OIDs of the built-in data types are defined in the file `src/include/catalog/pg_type.h` in the source tree.`PQfmod`

Returns the type modifier of the column associated with the given column number. Column numbers start at 0.

```text
int PQfmod(const PGresult *res,
           int column_number);
```

The interpretation of modifier values is type-specific; they typically indicate precision or size limits. The value -1 is used to indicate “no information available”. Most data types do not use modifiers, in which case the value is always -1.`PQfsize`

Returns the size in bytes of the column associated with the given column number. Column numbers start at 0.

```text
int PQfsize(const PGresult *res,
            int column_number);
```

`PQfsize` returns the space allocated for this column in a database row, in other words the size of the server's internal representation of the data type. \(Accordingly, it is not really very useful to clients.\) A negative value indicates the data type is variable-length.`PQbinaryTuples`

Returns 1 if the `PGresult` contains binary data and 0 if it contains text data.

```text
int PQbinaryTuples(const PGresult *res);
```

This function is deprecated \(except for its use in connection with `COPY`\), because it is possible for a single `PGresult` to contain text data in some columns and binary data in others. `PQfformat` is preferred. `PQbinaryTuples` returns 1 only if all columns of the result are binary \(format 1\).`PQgetvalue`

Returns a single field value of one row of a `PGresult`. Row and column numbers start at 0. The caller should not free the result directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.

```text
char *PQgetvalue(const PGresult *res,
                 int row_number,
                 int column_number);
```

For data in text format, the value returned by `PQgetvalue` is a null-terminated character string representation of the field value. For data in binary format, the value is in the binary representation determined by the data type's `typsend` and `typreceive` functions. \(The value is actually followed by a zero byte in this case too, but that is not ordinarily useful, since the value is likely to contain embedded nulls.\)

An empty string is returned if the field value is null. See `PQgetisnull` to distinguish null values from empty-string values.

The pointer returned by `PQgetvalue` points to storage that is part of the `PGresult` structure. One should not modify the data it points to, and one must explicitly copy the data into other storage if it is to be used past the lifetime of the `PGresult` structure itself.`PQgetisnull`

Tests a field for a null value. Row and column numbers start at 0.

```text
int PQgetisnull(const PGresult *res,
                int row_number,
                int column_number);
```

This function returns 1 if the field is null and 0 if it contains a non-null value. \(Note that `PQgetvalue` will return an empty string, not a null pointer, for a null field.\)`PQgetlength`

Returns the actual length of a field value in bytes. Row and column numbers start at 0.

```text
int PQgetlength(const PGresult *res,
                int row_number,
                int column_number);
```

This is the actual data length for the particular data value, that is, the size of the object pointed to by `PQgetvalue`. For text data format this is the same as `strlen()`. For binary format this is essential information. Note that one should _not_ rely on `PQfsize` to obtain the actual data length.`PQnparams`

Returns the number of parameters of a prepared statement.

```text
int PQnparams(const PGresult *res);
```

This function is only useful when inspecting the result of `PQdescribePrepared`. For other types of queries it will return zero.`PQparamtype`

Returns the data type of the indicated statement parameter. Parameter numbers start at 0.

```text
Oid PQparamtype(const PGresult *res, int param_number);
```

This function is only useful when inspecting the result of `PQdescribePrepared`. For other types of queries it will return zero.`PQprint`

Prints out all the rows and, optionally, the column names to the specified output stream.

```text
void PQprint(FILE *fout,      /* output stream */
             const PGresult *res,
             const PQprintOpt *po);
typedef struct
{
    pqbool  header;      /* print output field headings and row count */
    pqbool  align;       /* fill align the fields */
    pqbool  standard;    /* old brain dead format */
    pqbool  html3;       /* output HTML tables */
    pqbool  expanded;    /* expand tables */
    pqbool  pager;       /* use pager for output if needed */
    char    *fieldSep;   /* field separator */
    char    *tableOpt;   /* attributes for HTML table element */
    char    *caption;    /* HTML table caption */
    char    **fieldName; /* null-terminated array of replacement field names */
} PQprintOpt;
```

This function was formerly used by psql to print query results, but this is no longer the case. Note that it assumes all the data is in text format.

#### 33.3.3. Retrieving Other Result Information

These functions are used to extract other information from `PGresult` objects.`PQcmdStatus`

Returns the command status tag from the SQL command that generated the `PGresult`.

```text
char *PQcmdStatus(PGresult *res);
```

Commonly this is just the name of the command, but it might include additional data such as the number of rows processed. The caller should not free the result directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.`PQcmdTuples`

Returns the number of rows affected by the SQL command.

```text
char *PQcmdTuples(PGresult *res);
```

This function returns a string containing the number of rows affected by the SQL statement that generated the `PGresult`. This function can only be used following the execution of a `SELECT`, `CREATE TABLE AS`, `INSERT`, `UPDATE`, `DELETE`, `MOVE`, `FETCH`, or `COPY` statement, or an `EXECUTE` of a prepared query that contains an `INSERT`, `UPDATE`, or `DELETE` statement. If the command that generated the `PGresult` was anything else, `PQcmdTuples` returns an empty string. The caller should not free the return value directly. It will be freed when the associated `PGresult` handle is passed to `PQclear`.`PQoidValue`

Returns the OID of the inserted row, if the SQL command was an `INSERT` that inserted exactly one row into a table that has OIDs, or a `EXECUTE` of a prepared query containing a suitable `INSERT` statement. Otherwise, this function returns `InvalidOid`. This function will also return `InvalidOid` if the table affected by the `INSERT` statement does not contain OIDs.

```text
Oid PQoidValue(const PGresult *res);
```

`PQoidStatus`

This function is deprecated in favor of `PQoidValue` and is not thread-safe. It returns a string with the OID of the inserted row, while `PQoidValue` returns the OID value.

```text
char *PQoidStatus(const PGresult *res);
```

#### 33.3.4. Escaping Strings for Inclusion in SQL Commands

`PQescapeLiteral`

```text
char *PQescapeLiteral(PGconn *conn, const char *str, size_t length);
```

`PQescapeLiteral` escapes a string for use within an SQL command. This is useful when inserting data values as literal constants in SQL commands. Certain characters \(such as quotes and backslashes\) must be escaped to prevent them from being interpreted specially by the SQL parser. `PQescapeLiteral` performs this operation.

`PQescapeLiteral` returns an escaped version of the _`str`_ parameter in memory allocated with `malloc()`. This memory should be freed using `PQfreemem()` when the result is no longer needed. A terminating zero byte is not required, and should not be counted in _`length`_. \(If a terminating zero byte is found before _`length`_ bytes are processed, `PQescapeLiteral`stops at the zero; the behavior is thus rather like `strncpy`.\) The return string has all special characters replaced so that they can be properly processed by the PostgreSQL string literal parser. A terminating zero byte is also added. The single quotes that must surround PostgreSQL string literals are included in the result string.

On error, `PQescapeLiteral` returns `NULL` and a suitable message is stored in the _`conn`_ object.

#### Tip

It is especially important to do proper escaping when handling strings that were received from an untrustworthy source. Otherwise there is a security risk: you are vulnerable to “SQL injection” attacks wherein unwanted SQL commands are fed to your database.

Note that it is not necessary nor correct to do escaping when a data value is passed as a separate parameter in `PQexecParams` or its sibling routines.`PQescapeIdentifier`

```text
char *PQescapeIdentifier(PGconn *conn, const char *str, size_t length);
```

`PQescapeIdentifier` escapes a string for use as an SQL identifier, such as a table, column, or function name. This is useful when a user-supplied identifier might contain special characters that would otherwise not be interpreted as part of the identifier by the SQL parser, or when the identifier might contain upper case characters whose case should be preserved.

`PQescapeIdentifier` returns a version of the _`str`_ parameter escaped as an SQL identifier in memory allocated with `malloc()`. This memory must be freed using `PQfreemem()` when the result is no longer needed. A terminating zero byte is not required, and should not be counted in _`length`_. \(If a terminating zero byte is found before _`length`_ bytes are processed, `PQescapeIdentifier` stops at the zero; the behavior is thus rather like `strncpy`.\) The return string has all special characters replaced so that it will be properly processed as an SQL identifier. A terminating zero byte is also added. The return string will also be surrounded by double quotes.

On error, `PQescapeIdentifier` returns `NULL` and a suitable message is stored in the _`conn`_ object.

#### Tip

As with string literals, to prevent SQL injection attacks, SQL identifiers must be escaped when they are received from an untrustworthy source.`PQescapeStringConn`

```text
size_t PQescapeStringConn(PGconn *conn,
                          char *to, const char *from, size_t length,
                          int *error);
```

`PQescapeStringConn` escapes string literals, much like `PQescapeLiteral`. Unlike `PQescapeLiteral`, the caller is responsible for providing an appropriately sized buffer. Furthermore, `PQescapeStringConn` does not generate the single quotes that must surround PostgreSQL string literals; they should be provided in the SQL command that the result is inserted into. The parameter _`from`_ points to the first character of the string that is to be escaped, and the _`length`_ parameter gives the number of bytes in this string. A terminating zero byte is not required, and should not be counted in _`length`_. \(If a terminating zero byte is found before _`length`_ bytes are processed, `PQescapeStringConn` stops at the zero; the behavior is thus rather like `strncpy`.\) _`to`_ shall point to a buffer that is able to hold at least one more byte than twice the value of _`length`_, otherwise the behavior is undefined. Behavior is likewise undefined if the _`to`_ and _`from`_ strings overlap.

If the _`error`_ parameter is not `NULL`, then `*error` is set to zero on success, nonzero on error. Presently the only possible error conditions involve invalid multibyte encoding in the source string. The output string is still generated on error, but it can be expected that the server will reject it as malformed. On error, a suitable message is stored in the _`conn`_object, whether or not _`error`_ is `NULL`.

`PQescapeStringConn` returns the number of bytes written to _`to`_, not including the terminating zero byte.`PQescapeString`

`PQescapeString` is an older, deprecated version of `PQescapeStringConn`.

```text
size_t PQescapeString (char *to, const char *from, size_t length);
```

The only difference from `PQescapeStringConn` is that `PQescapeString` does not take `PGconn` or _`error`_ parameters. Because of this, it cannot adjust its behavior depending on the connection properties \(such as character encoding\) and therefore _it might give the wrong results_. Also, it has no way to report error conditions.

`PQescapeString` can be used safely in client programs that work with only one PostgreSQL connection at a time \(in this case it can find out what it needs to know “behind the scenes”\). In other contexts it is a security hazard and should be avoided in favor of `PQescapeStringConn`.`PQescapeByteaConn`

Escapes binary data for use within an SQL command with the type `bytea`. As with `PQescapeStringConn`, this is only used when inserting data directly into an SQL command string.

```text
unsigned char *PQescapeByteaConn(PGconn *conn,
                                 const unsigned char *from,
                                 size_t from_length,
                                 size_t *to_length);
```

Certain byte values must be escaped when used as part of a `bytea` literal in an SQL statement. `PQescapeByteaConn` escapes bytes using either hex encoding or backslash escaping. See [Section 8.4](https://www.postgresql.org/docs/10/static/datatype-binary.html) for more information.

The _`from`_ parameter points to the first byte of the string that is to be escaped, and the _`from_length`_ parameter gives the number of bytes in this binary string. \(A terminating zero byte is neither necessary nor counted.\) The _`to_length`_ parameter points to a variable that will hold the resultant escaped string length. This result string length includes the terminating zero byte of the result.

`PQescapeByteaConn` returns an escaped version of the _`from`_ parameter binary string in memory allocated with `malloc()`. This memory should be freed using `PQfreemem()` when the result is no longer needed. The return string has all special characters replaced so that they can be properly processed by the PostgreSQL string literal parser, and the `bytea`input function. A terminating zero byte is also added. The single quotes that must surround PostgreSQL string literals are not part of the result string.

On error, a null pointer is returned, and a suitable error message is stored in the _`conn`_ object. Currently, the only possible error is insufficient memory for the result string.`PQescapeBytea`

`PQescapeBytea` is an older, deprecated version of `PQescapeByteaConn`.

```text
unsigned char *PQescapeBytea(const unsigned char *from,
                             size_t from_length,
                             size_t *to_length);
```

The only difference from `PQescapeByteaConn` is that `PQescapeBytea` does not take a `PGconn` parameter. Because of this, `PQescapeBytea` can only be used safely in client programs that use a single PostgreSQL connection at a time \(in this case it can find out what it needs to know “behind the scenes”\). It _might give the wrong results_ if used in programs that use multiple database connections \(use `PQescapeByteaConn` in such cases\).`PQunescapeBytea`

Converts a string representation of binary data into binary data — the reverse of `PQescapeBytea`. This is needed when retrieving `bytea` data in text format, but not when retrieving it in binary format.

```text
unsigned char *PQunescapeBytea(const unsigned char *from, size_t *to_length);
```

The _`from`_ parameter points to a string such as might be returned by `PQgetvalue` when applied to a `bytea` column. `PQunescapeBytea` converts this string representation into its binary representation. It returns a pointer to a buffer allocated with `malloc()`, or `NULL` on error, and puts the size of the buffer in _`to_length`_. The result must be freed using `PQfreemem`when it is no longer needed.

This conversion is not exactly the inverse of `PQescapeBytea`, because the string is not expected to be “escaped” when received from `PQgetvalue`. In particular this means there is no need for string quoting considerations, and so no need for a `PGconn` parameter.

