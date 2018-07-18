# CREATE LANGUAGE

CREATE LANGUAGE — define a new procedural language

### Synopsis

```text
CREATE [ OR REPLACE ] [ PROCEDURAL ] LANGUAGE name
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
    HANDLER call_handler [ INLINE inline_handler ] [ VALIDATOR valfunction ]
```

### Description

`CREATE LANGUAGE` registers a new procedural language with a PostgreSQL database. Subsequently, functions and trigger procedures can be defined in this new language.

#### Note

As of PostgreSQL 9.1, most procedural languages have been made into “extensions”, and should therefore be installed with [CREATE EXTENSION](https://www.postgresql.org/docs/10/static/sql-createextension.html) not `CREATE LANGUAGE`. Direct use of `CREATE LANGUAGE` should now be confined to extension installation scripts. If you have a “bare” language in your database, perhaps as a result of an upgrade, you can convert it to an extension using `CREATE EXTENSION` _`langname`_ FROM unpackaged.

`CREATE LANGUAGE` effectively associates the language name with handler function\(s\) that are responsible for executing functions written in the language. Refer to [Chapter 55](https://www.postgresql.org/docs/10/static/plhandler.html) for more information about language handlers.

There are two forms of the `CREATE LANGUAGE` command. In the first form, the user supplies just the name of the desired language, and the PostgreSQL server consults the [`pg_pltemplate`](https://www.postgresql.org/docs/10/static/catalog-pg-pltemplate.html)system catalog to determine the correct parameters. In the second form, the user supplies the language parameters along with the language name. The second form can be used to create a language that is not defined in `pg_pltemplate`, but this approach is considered obsolescent.

When the server finds an entry in the `pg_pltemplate` catalog for the given language name, it will use the catalog data even if the command includes language parameters. This behavior simplifies loading of old dump files, which are likely to contain out-of-date information about language support functions.

Ordinarily, the user must have the PostgreSQL superuser privilege to register a new language. However, the owner of a database can register a new language within that database if the language is listed in the `pg_pltemplate` catalog and is marked as allowed to be created by database owners \(`tmpldbacreate` is true\). The default is that trusted languages can be created by database owners, but this can be adjusted by superusers by modifying the contents of `pg_pltemplate`. The creator of a language becomes its owner and can later drop it, rename it, or assign it to a new owner.

`CREATE OR REPLACE LANGUAGE` will either create a new language, or replace an existing definition. If the language already exists, its parameters are updated according to the values specified or taken from `pg_pltemplate`, but the language's ownership and permissions settings do not change, and any existing functions written in the language are assumed to still be valid. In addition to the normal privilege requirements for creating a language, the user must be superuser or owner of the existing language. The `REPLACE` case is mainly meant to be used to ensure that the language exists. If the language has a `pg_pltemplate` entry then `REPLACE` will not actually change anything about an existing definition, except in the unusual case where the `pg_pltemplate` entry has been modified since the language was created.

### Parameters

`TRUSTED`

`TRUSTED` specifies that the language does not grant access to data that the user would not otherwise have. If this key word is omitted when registering the language, only users with the PostgreSQL superuser privilege can use this language to create new functions.

`PROCEDURAL`

This is a noise word.

_`name`_

The name of the new procedural language. The name must be unique among the languages in the database.

For backward compatibility, the name can be enclosed by single quotes.

`HANDLER` _`call_handler`_

_`call_handler`_ is the name of a previously registered function that will be called to execute the procedural language's functions. The call handler for a procedural language must be written in a compiled language such as C with version 1 call convention and registered with PostgreSQL as a function taking no arguments and returning the `language_handler`type, a placeholder type that is simply used to identify the function as a call handler.

`INLINE` _`inline_handler`_

_`inline_handler`_ is the name of a previously registered function that will be called to execute an anonymous code block \([DO](https://www.postgresql.org/docs/10/static/sql-do.html) command\) in this language. If no _`inline_handler`_function is specified, the language does not support anonymous code blocks. The handler function must take one argument of type `internal`, which will be the `DO` command's internal representation, and it will typically return `void`. The return value of the handler is ignored.

`VALIDATOR` _`valfunction`_

_`valfunction`_ is the name of a previously registered function that will be called when a new function in the language is created, to validate the new function. If no validator function is specified, then a new function will not be checked when it is created. The validator function must take one argument of type `oid`, which will be the OID of the to-be-created function, and will typically return `void`.

A validator function would typically inspect the function body for syntactical correctness, but it can also look at other properties of the function, for example if the language cannot handle certain argument types. To signal an error, the validator function should use the `ereport()` function. The return value of the function is ignored.

The `TRUSTED` option and the support function name\(s\) are ignored if the server has an entry for the specified language name in `pg_pltemplate`.

### Notes

Use [DROP LANGUAGE](https://www.postgresql.org/docs/10/static/sql-droplanguage.html) to drop procedural languages.

The system catalog `pg_language` \(see [Section 51.29](https://www.postgresql.org/docs/10/static/catalog-pg-language.html)\) records information about the currently installed languages. Also, the psql command `\dL` lists the installed languages.

To create functions in a procedural language, a user must have the `USAGE` privilege for the language. By default, `USAGE` is granted to `PUBLIC` \(i.e., everyone\) for trusted languages. This can be revoked if desired.

Procedural languages are local to individual databases. However, a language can be installed into the `template1` database, which will cause it to be available automatically in all subsequently-created databases.

The call handler function, the inline handler function \(if any\), and the validator function \(if any\) must already exist if the server does not have an entry for the language in `pg_pltemplate`. But when there is an entry, the functions need not already exist; they will be automatically defined if not present in the database. \(This might result in `CREATE LANGUAGE`failing, if the shared library that implements the language is not available in the installation.\)

In PostgreSQL versions before 7.3, it was necessary to declare handler functions as returning the placeholder type `opaque`, rather than `language_handler`. To support loading of old dump files, `CREATE LANGUAGE` will accept a function declared as returning `opaque`, but it will issue a notice and change the function's declared return type to `language_handler`.

### Examples

The preferred way of creating any of the standard procedural languages is just:

```text
CREATE LANGUAGE plperl;
```

For a language not known in the `pg_pltemplate` catalog, a sequence such as this is needed:

```text
CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

### Compatibility

`CREATE LANGUAGE` is a PostgreSQL extension.

### See Also

[ALTER LANGUAGE](https://www.postgresql.org/docs/10/static/sql-alterlanguage.html), [CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html), [DROP LANGUAGE](https://www.postgresql.org/docs/10/static/sql-droplanguage.html), [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html), [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html)

