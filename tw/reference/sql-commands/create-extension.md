# CREATE EXTENSION

CREATE EXTENSION — 安裝延伸套件

## 語法

```text
CREATE EXTENSION [ IF NOT EXISTS ] extension_name
    [ WITH ] [ SCHEMA schema_name ]
             [ VERSION version ]
             [ FROM old_version ]
             [ CASCADE ]
```

## Description

`CREATE EXTENSION` loads a new extension into the current database. There must not be an extension of the same name already loaded.

Loading an extension essentially amounts to running the extension's script file. The script will typically create new SQL objects such as functions, data types, operators and index support methods. `CREATE EXTENSION`additionally records the identities of all the created objects, so that they can be dropped again if `DROP EXTENSION` is issued.

Loading an extension requires the same privileges that would be required to create its component objects. For most extensions this means superuser or database owner privileges are needed. The user who runs `CREATE EXTENSION` becomes the owner of the extension for purposes of later privilege checks, as well as the owner of any objects created by the extension's script.

## Parameters

`IF NOT EXISTS`

Do not throw an error if an extension with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing extension is anything like the one that would have been created from the currently-available script file._`extension_name`_

The name of the extension to be installed. PostgreSQL will create the extension using details from the file `SHAREDIR/extension/`_`extension_name`_`.control`._`schema_name`_

The name of the schema in which to install the extension's objects, given that the extension allows its contents to be relocated. The named schema must already exist. If not specified, and the extension's control file does not specify a schema either, the current default object creation schema is used.

If the extension specifies a `schema` parameter in its control file, then that schema cannot be overridden with a `SCHEMA` clause. Normally, an error will be raised if a `SCHEMA` clause is given and it conflicts with the extension's `schema` parameter. However, if the `CASCADE` clause is also given, then _`schema_name`_ is ignored when it conflicts. The given _`schema_name`_ will be used for installation of any needed extensions that do not specify`schema` in their control files.

Remember that the extension itself is not considered to be within any schema: extensions have unqualified names that must be unique database-wide. But objects belonging to the extension can be within schemas._`version`_

The version of the extension to install. This can be written as either an identifier or a string literal. The default version is whatever is specified in the extension's control file._`old_version`_

`FROM` _`old_version`_ must be specified when, and only when, you are attempting to install an extension that replaces an “old style” module that is just a collection of objects not packaged into an extension. This option causes `CREATE EXTENSION` to run an alternative installation script that absorbs the existing objects into the extension, instead of creating new objects. Be careful that `SCHEMA` specifies the schema containing these pre-existing objects.

The value to use for _`old_version`_ is determined by the extension's author, and might vary if there is more than one version of the old-style module that can be upgraded into an extension. For the standard additional modules supplied with pre-9.1 PostgreSQL, use `unpackaged` for _`old_version`_ when updating a module to extension style.`CASCADE`

Automatically install any extensions that this extension depends on that are not already installed. Their dependencies are likewise automatically installed, recursively. The `SCHEMA` clause, if given, applies to all extensions that get installed this way. Other options of the statement are not applied to automatically-installed extensions; in particular, their default versions are always selected.

## Notes

Before you can use `CREATE EXTENSION` to load an extension into a database, the extension's supporting files must be installed. Information about installing the extensions supplied with PostgreSQL can be found in [Additional Supplied Modules](https://www.postgresql.org/docs/10/static/contrib.html).

The extensions currently available for loading can be identified from the [`pg_available_extensions`](https://www.postgresql.org/docs/10/static/view-pg-available-extensions.html) or [`pg_available_extension_versions`](https://www.postgresql.org/docs/10/static/view-pg-available-extension-versions.html) system views.

For information about writing new extensions, see [Section 37.15](https://www.postgresql.org/docs/10/static/extend-extensions.html).

## Examples

Install the [hstore](https://www.postgresql.org/docs/10/static/hstore.html) extension into the current database:

```text
CREATE EXTENSION hstore;
```

Update a pre-9.1 installation of `hstore` into extension style:

```text
CREATE EXTENSION hstore SCHEMA public FROM unpackaged;
```

Be careful to specify the schema in which you installed the existing `hstore` objects.

## 相容性

CREATE EXTENSION 是 PostgreSQL 的延伸功能。

## 參閱

[ALTER EXTENSION](alter-extension.md), [DROP EXTENSION](drop-extension.md)

