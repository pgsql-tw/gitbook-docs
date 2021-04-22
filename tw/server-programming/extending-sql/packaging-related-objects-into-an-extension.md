---
description: 版本：11
---

# 37.17. 封裝相關物件到延伸功能中

A useful extension to PostgreSQL typically includes multiple SQL objects; for example, a new data type will require new functions, new operators, and probably new index operator classes. It is helpful to collect all these objects into a single package to simplify database management. PostgreSQL calls such a package an _extension_. To define an extension, you need at least a _script file_ that contains the SQL commands to create the extension's objects, and a _control file_ that specifies a few basic properties of the extension itself. If the extension includes C code, there will typically also be a shared library file into which the C code has been built. Once you have these files, a simple [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command loads the objects into your database.

The main advantage of using an extension, rather than just running the SQL script to load a bunch of “loose” objects into your database, is that PostgreSQL will then understand that the objects of the extension go together. You can drop all the objects with a single [DROP EXTENSION](https://www.postgresql.org/docs/current/sql-dropextension.html) command \(no need to maintain a separate “uninstall” script\). Even more useful, pg\_dump knows that it should not dump the individual member objects of the extension — it will just include a `CREATE EXTENSION` command in dumps, instead. This vastly simplifies migration to a new version of the extension that might contain more or different objects than the old version. Note however that you must have the extension's control, script, and other files available when loading such a dump into a new database.

PostgreSQL will not let you drop an individual object contained in an extension, except by dropping the whole extension. Also, while you can change the definition of an extension member object \(for example, via `CREATE OR REPLACE FUNCTION` for a function\), bear in mind that the modified definition will not be dumped by pg\_dump. Such a change is usually only sensible if you concurrently make the same change in the extension's script file. \(But there are special provisions for tables containing configuration data; see [Section 37.17.4](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-CONFIG-TABLES).\) In production situations, it's generally better to create an extension update script to perform changes to extension member objects.

The extension script may set privileges on objects that are part of the extension via `GRANT` and `REVOKE` statements. The final set of privileges for each object \(if any are set\) will be stored in the [`pg_init_privs`](https://www.postgresql.org/docs/current/catalog-pg-init-privs.html) system catalog. When pg\_dump is used, the `CREATE EXTENSION` command will be included in the dump, followed by the set of `GRANT` and `REVOKE` statements necessary to set the privileges on the objects to what they were at the time the dump was taken.

PostgreSQL does not currently support extension scripts issuing `CREATE POLICY` or `SECURITY LABEL` statements. These are expected to be set after the extension has been created. All RLS policies and security labels on extension objects will be included in dumps created by pg\_dump.

The extension mechanism also has provisions for packaging modification scripts that adjust the definitions of the SQL objects contained in an extension. For example, if version 1.1 of an extension adds one function and changes the body of another function compared to 1.0, the extension author can provide an _update script_ that makes just those two changes. The `ALTER EXTENSION UPDATE` command can then be used to apply these changes and track which version of the extension is actually installed in a given database.

The kinds of SQL objects that can be members of an extension are shown in the description of [ALTER EXTENSION](https://www.postgresql.org/docs/current/sql-alterextension.html). Notably, objects that are database-cluster-wide, such as databases, roles, and tablespaces, cannot be extension members since an extension is only known within one database. \(Although an extension script is not prohibited from creating such objects, if it does so they will not be tracked as part of the extension.\) Also notice that while a table can be a member of an extension, its subsidiary objects such as indexes are not directly considered members of the extension. Another important point is that schemas can belong to extensions, but not vice versa: an extension as such has an unqualified name and does not exist “within” any schema. The extension's member objects, however, will belong to schemas whenever appropriate for their object types. It may or may not be appropriate for an extension to own the schema\(s\) its member objects are within.

If an extension's script creates any temporary objects \(such as temp tables\), those objects are treated as extension members for the remainder of the current session, but are automatically dropped at session end, as any temporary object would be. This is an exception to the rule that extension member objects cannot be dropped without dropping the whole extension.

## 37.17.1. Defining Extension Objects

大多數的延伸功能應該很少假設它們所佔用的資料庫是固定的。 特別是，除非您使用了 SET search\_path = pg\_temp，否則將假設每個不合格的名稱都解析為惡意使用者定義的物件。當心那些隱含相依於 search\_path 的結構：`IN` 和 `CASE expression WHEN` 總是使用搜尋路徑的一個運算子。在這個時機上，請使用 `OPERATOR(schema.=) ANY` 和 `CASE WHEN expression`。

## 37.17.2. Extension Files

The [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command relies on a control file for each extension, which must be named the same as the extension with a suffix of `.control`, and must be placed in the installation's `SHAREDIR/extension` directory. There must also be at least one SQL script file, which follows the naming pattern _`extension`_--_`version`_.sql \(for example, `foo--1.0.sql` for version `1.0` of extension `foo`\). By default, the script file\(s\) are also placed in the `SHAREDIR/extension` directory; but the control file can specify a different directory for the script file\(s\).

The file format for an extension control file is the same as for the `postgresql.conf` file, namely a list of _`parameter_name`_ `=` _`value`_ assignments, one per line. Blank lines and comments introduced by `#` are allowed. Be sure to quote any value that is not a single word or number.

A control file can set the following parameters:`directory` \(`string`\)

The directory containing the extension's SQL script file\(s\). Unless an absolute path is given, the name is relative to the installation's `SHAREDIR` directory. The default behavior is equivalent to specifying `directory = 'extension'`.`default_version` \(`string`\)

The default version of the extension \(the one that will be installed if no version is specified in `CREATE EXTENSION`\). Although this can be omitted, that will result in `CREATE EXTENSION` failing if no `VERSION` option appears, so you generally don't want to do that.`comment` \(`string`\)

A comment \(any string\) about the extension. The comment is applied when initially creating an extension, but not during extension updates \(since that might override user-added comments\). Alternatively, the extension's comment can be set by writing a [COMMENT](https://www.postgresql.org/docs/current/sql-comment.html) command in the script file.`encoding` \(`string`\)

The character set encoding used by the script file\(s\). This should be specified if the script files contain any non-ASCII characters. Otherwise the files will be assumed to be in the database encoding.`module_pathname` \(`string`\)

The value of this parameter will be substituted for each occurrence of `MODULE_PATHNAME` in the script file\(s\). If it is not set, no substitution is made. Typically, this is set to `$libdir/`_`shared_library_name`_ and then `MODULE_PATHNAME` is used in `CREATE FUNCTION` commands for C-language functions, so that the script files do not need to hard-wire the name of the shared library.`requires` \(`string`\)

A list of names of extensions that this extension depends on, for example `requires = 'foo, bar'`. Those extensions must be installed before this one can be installed.`superuser` \(`boolean`\)

If this parameter is `true` \(which is the default\), only superusers can create the extension or update it to a new version. If it is set to `false`, just the privileges required to execute the commands in the installation or update script are required.`relocatable` \(`boolean`\)

An extension is _relocatable_ if it is possible to move its contained objects into a different schema after initial creation of the extension. The default is `false`, i.e. the extension is not relocatable. See [Section 37.17.3](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-RELOCATION) for more information.`schema` \(`string`\)

This parameter can only be set for non-relocatable extensions. It forces the extension to be loaded into exactly the named schema and not any other. The `schema` parameter is consulted only when initially creating an extension, not during extension updates. See [Section 37.17.3](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-RELOCATION) for more information.

In addition to the primary control file _`extension`_.control, an extension can have secondary control files named in the style _`extension`_--_`version`_.control. If supplied, these must be located in the script file directory. Secondary control files follow the same format as the primary control file. Any parameters set in a secondary control file override the primary control file when installing or updating to that version of the extension. However, the parameters `directory` and `default_version` cannot be set in a secondary control file.

An extension's SQL script files can contain any SQL commands, except for transaction control commands \(`BEGIN`, `COMMIT`, etc\) and commands that cannot be executed inside a transaction block \(such as `VACUUM`\). This is because the script files are implicitly executed within a transaction block.

An extension's SQL script files can also contain lines beginning with `\echo`, which will be ignored \(treated as comments\) by the extension mechanism. This provision is commonly used to throw an error if the script file is fed to psql rather than being loaded via `CREATE EXTENSION` \(see example script in [Section 37.17.7](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-EXAMPLE)\). Without that, users might accidentally load the extension's contents as “loose” objects rather than as an extension, a state of affairs that's a bit tedious to recover from.

While the script files can contain any characters allowed by the specified encoding, control files should contain only plain ASCII, because there is no way for PostgreSQL to know what encoding a control file is in. In practice this is only an issue if you want to use non-ASCII characters in the extension's comment. Recommended practice in that case is to not use the control file `comment` parameter, but instead use `COMMENT ON EXTENSION` within a script file to set the comment.

## 37.17.3. Extension Relocatability

Users often wish to load the objects contained in an extension into a different schema than the extension's author had in mind. There are three supported levels of relocatability:

* A fully relocatable extension can be moved into another schema at any time, even after it's been loaded into a database. This is done with the `ALTER EXTENSION SET SCHEMA` command, which automatically renames all the member objects into the new schema. Normally, this is only possible if the extension contains no internal assumptions about what schema any of its objects are in. Also, the extension's objects must all be in one schema to begin with \(ignoring objects that do not belong to any schema, such as procedural languages\). Mark a fully relocatable extension by setting `relocatable = true` in its control file.
* An extension might be relocatable during installation but not afterwards. This is typically the case if the extension's script file needs to reference the target schema explicitly, for example in setting `search_path` properties for SQL functions. For such an extension, set `relocatable = false` in its control file, and use `@extschema@` to refer to the target schema in the script file. All occurrences of this string will be replaced by the actual target schema's name before the script is executed. The user can set the target schema using the `SCHEMA` option of `CREATE EXTENSION`.
* If the extension does not support relocation at all, set `relocatable = false` in its control file, and also set `schema` to the name of the intended target schema. This will prevent use of the `SCHEMA` option of `CREATE EXTENSION`, unless it specifies the same schema named in the control file. This choice is typically necessary if the extension contains internal assumptions about schema names that can't be replaced by uses of `@extschema@`. The `@extschema@` substitution mechanism is available in this case too, although it is of limited use since the schema name is determined by the control file.

In all cases, the script file will be executed with [search\_path](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SEARCH-PATH) initially set to point to the target schema; that is, `CREATE EXTENSION` does the equivalent of this:

```text
SET LOCAL search_path TO @extschema@;
```

This allows the objects created by the script file to go into the target schema. The script file can change `search_path` if it wishes, but that is generally undesirable. `search_path` is restored to its previous setting upon completion of `CREATE EXTENSION`.

The target schema is determined by the `schema` parameter in the control file if that is given, otherwise by the `SCHEMA` option of `CREATE EXTENSION` if that is given, otherwise the current default object creation schema \(the first one in the caller's `search_path`\). When the control file `schema` parameter is used, the target schema will be created if it doesn't already exist, but in the other two cases it must already exist.

If any prerequisite extensions are listed in `requires` in the control file, their target schemas are appended to the initial setting of `search_path`. This allows their objects to be visible to the new extension's script file.

Although a non-relocatable extension can contain objects spread across multiple schemas, it is usually desirable to place all the objects meant for external use into a single schema, which is considered the extension's target schema. Such an arrangement works conveniently with the default setting of `search_path` during creation of dependent extensions.

## 37.17.4. Extension Configuration Tables

Some extensions include configuration tables, which contain data that might be added or changed by the user after installation of the extension. Ordinarily, if a table is part of an extension, neither the table's definition nor its content will be dumped by pg\_dump. But that behavior is undesirable for a configuration table; any data changes made by the user need to be included in dumps, or the extension will behave differently after a dump and reload.

To solve this problem, an extension's script file can mark a table or a sequence it has created as a configuration relation, which will cause pg\_dump to include the table's or the sequence's contents \(not its definition\) in dumps. To do that, call the function `pg_extension_config_dump(regclass, text)` after creating the table or the sequence, for example

```text
CREATE TABLE my_config (key text, value text);
CREATE SEQUENCE my_config_seq;

SELECT pg_catalog.pg_extension_config_dump('my_config', '');
SELECT pg_catalog.pg_extension_config_dump('my_config_seq', '');
```

Any number of tables or sequences can be marked this way. Sequences associated with `serial` or `bigserial` columns can be marked as well.

When the second argument of `pg_extension_config_dump` is an empty string, the entire contents of the table are dumped by pg\_dump. This is usually only correct if the table is initially empty as created by the extension script. If there is a mixture of initial data and user-provided data in the table, the second argument of `pg_extension_config_dump` provides a `WHERE` condition that selects the data to be dumped. For example, you might do

```text
CREATE TABLE my_config (key text, value text, standard_entry boolean);

SELECT pg_catalog.pg_extension_config_dump('my_config', 'WHERE NOT standard_entry');
```

and then make sure that `standard_entry` is true only in the rows created by the extension's script.

For sequences, the second argument of `pg_extension_config_dump` has no effect.

More complicated situations, such as initially-provided rows that might be modified by users, can be handled by creating triggers on the configuration table to ensure that modified rows are marked correctly.

You can alter the filter condition associated with a configuration table by calling `pg_extension_config_dump` again. \(This would typically be useful in an extension update script.\) The only way to mark a table as no longer a configuration table is to dissociate it from the extension with `ALTER EXTENSION ... DROP TABLE`.

Note that foreign key relationships between these tables will dictate the order in which the tables are dumped out by pg\_dump. Specifically, pg\_dump will attempt to dump the referenced-by table before the referencing table. As the foreign key relationships are set up at CREATE EXTENSION time \(prior to data being loaded into the tables\) circular dependencies are not supported. When circular dependencies exist, the data will still be dumped out but the dump will not be able to be restored directly and user intervention will be required.

Sequences associated with `serial` or `bigserial` columns need to be directly marked to dump their state. Marking their parent relation is not enough for this purpose.

## 37.17.5. Extension Updates

One advantage of the extension mechanism is that it provides convenient ways to manage updates to the SQL commands that define an extension's objects. This is done by associating a version name or number with each released version of the extension's installation script. In addition, if you want users to be able to update their databases dynamically from one version to the next, you should provide _update scripts_ that make the necessary changes to go from one version to the next. Update scripts have names following the pattern _`extension`_--_`old_version`_--_`target_version`_.sql \(for example, `foo--1.0--1.1.sql` contains the commands to modify version `1.0` of extension `foo` into version `1.1`\).

Given that a suitable update script is available, the command `ALTER EXTENSION UPDATE` will update an installed extension to the specified new version. The update script is run in the same environment that `CREATE EXTENSION` provides for installation scripts: in particular, `search_path` is set up in the same way, and any new objects created by the script are automatically added to the extension. Also, if the script chooses to drop extension member objects, they are automatically dissociated from the extension.

If an extension has secondary control files, the control parameters that are used for an update script are those associated with the script's target \(new\) version.

The update mechanism can be used to solve an important special case: converting a “loose” collection of objects into an extension. Before the extension mechanism was added to PostgreSQL \(in 9.1\), many people wrote extension modules that simply created assorted unpackaged objects. Given an existing database containing such objects, how can we convert the objects into a properly packaged extension? Dropping them and then doing a plain `CREATE EXTENSION` is one way, but it's not desirable if the objects have dependencies \(for example, if there are table columns of a data type created by the extension\). The way to fix this situation is to create an empty extension, then use `ALTER EXTENSION ADD` to attach each pre-existing object to the extension, then finally create any new objects that are in the current extension version but were not in the unpackaged release. `CREATE EXTENSION` supports this case with its `FROM` _`old_version`_ option, which causes it to not run the normal installation script for the target version, but instead the update script named _`extension`_--_`old_version`_--_`target_version`_.sql. The choice of the dummy version name to use as _`old_version`_ is up to the extension author, though `unpackaged` is a common convention. If you have multiple prior versions you need to be able to update into extension style, use multiple dummy version names to identify them.

`ALTER EXTENSION` is able to execute sequences of update script files to achieve a requested update. For example, if only `foo--1.0--1.1.sql` and `foo--1.1--2.0.sql` are available, `ALTER EXTENSION` will apply them in sequence if an update to version `2.0` is requested when `1.0` is currently installed.

PostgreSQL doesn't assume anything about the properties of version names: for example, it does not know whether `1.1` follows `1.0`. It just matches up the available version names and follows the path that requires applying the fewest update scripts. \(A version name can actually be any string that doesn't contain `--` or leading or trailing `-`.\)

Sometimes it is useful to provide “downgrade” scripts, for example `foo--1.1--1.0.sql` to allow reverting the changes associated with version `1.1`. If you do that, be careful of the possibility that a downgrade script might unexpectedly get applied because it yields a shorter path. The risky case is where there is a “fast path” update script that jumps ahead several versions as well as a downgrade script to the fast path's start point. It might take fewer steps to apply the downgrade and then the fast path than to move ahead one version at a time. If the downgrade script drops any irreplaceable objects, this will yield undesirable results.

To check for unexpected update paths, use this command:

```text
SELECT * FROM pg_extension_update_paths('extension_name');
```

This shows each pair of distinct known version names for the specified extension, together with the update path sequence that would be taken to get from the source version to the target version, or `NULL` if there is no available update path. The path is shown in textual form with `--` separators. You can use `regexp_split_to_array(path,'--')` if you prefer an array format.

## 37.17.6. Installing Extensions Using Update Scripts

An extension that has been around for awhile will probably exist in several versions, for which the author will need to write update scripts. For example, if you have released a `foo` extension in versions `1.0`, `1.1`, and `1.2`, there should be update scripts `foo--1.0--1.1.sql` and `foo--1.1--1.2.sql`. Before PostgreSQL 10, it was necessary to also create new script files `foo--1.1.sql` and `foo--1.2.sql` that directly build the newer extension versions, or else the newer versions could not be installed directly, only by installing `1.0` and then updating. That was tedious and duplicative, but now it's unnecessary, because `CREATE EXTENSION` can follow update chains automatically. For example, if only the script files `foo--1.0.sql`, `foo--1.0--1.1.sql`, and `foo--1.1--1.2.sql` are available then a request to install version `1.2` is honored by running those three scripts in sequence. The processing is the same as if you'd first installed `1.0` and then updated to `1.2`. \(As with `ALTER EXTENSION UPDATE`, if multiple pathways are available then the shortest is preferred.\) Arranging an extension's script files in this style can reduce the amount of maintenance effort needed to produce small updates.

If you use secondary \(version-specific\) control files with an extension maintained in this style, keep in mind that each version needs a control file even if it has no stand-alone installation script, as that control file will determine how the implicit update to that version is performed. For example, if `foo--1.0.control` specifies `requires = 'bar'` but `foo`'s other control files do not, the extension's dependency on `bar` will be dropped when updating from `1.0` to another version.

## 37.17.7. Extension Example

Here is a complete example of an SQL-only extension, a two-element composite type that can store any type of value in its slots, which are named “k” and “v”. Non-text values are automatically coerced to text for storage.

The script file `pair--1.0.sql` looks like this:

```text
-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION pair" to load this file. \quit

CREATE TYPE pair AS ( k text, v text );

CREATE OR REPLACE FUNCTION pair(text, text)
RETURNS pair LANGUAGE SQL AS 'SELECT ROW($1, $2)::@extschema@.pair;';

CREATE OPERATOR ~> (LEFTARG = text, RIGHTARG = text, FUNCTION = pair);

-- "SET search_path" is easy to get right, but qualified names perform better.
CREATE OR REPLACE FUNCTION lower(pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW(lower($1.k), lower($1.v))::@extschema@.pair;'
SET search_path = pg_temp;

CREATE OR REPLACE FUNCTION pair_concat(pair, pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW($1.k OPERATOR(pg_catalog.||) $2.k,
               $1.v OPERATOR(pg_catalog.||) $2.v)::@extschema@.pair;';
```

The control file `pair.control` looks like this:

```text
# pair extension
comment = 'A key/value pair data type'
default_version = '1.0'
relocatable = false
```

While you hardly need a makefile to install these two files into the correct directory, you could use a `Makefile` containing this:

```text
EXTENSION = pair
DATA = pair--1.0.sql

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

This makefile relies on PGXS, which is described in [Section 37.18](https://www.postgresql.org/docs/current/extend-pgxs.html). The command `make install` will install the control and script files into the correct directory as reported by pg\_config.

Once the files are installed, use the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command to load the objects into any particular database.

