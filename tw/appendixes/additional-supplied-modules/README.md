# F. 延伸支援模組

This appendix and the next one contain information regarding the modules that can be found in the `contrib` directory of the PostgreSQL distribution. These include porting tools, analysis utilities, and plug-in features that are not part of the core PostgreSQL system, mainly because they address a limited audience or are too experimental to be part of the main source tree. This does not preclude their usefulness.

This appendix covers extensions and other server plug-in modules found in `contrib`. [Appendix G](https://www.postgresql.org/docs/12/contrib-prog.html) covers utility programs.

When building from the source distribution, these components are not built automatically, unless you build the "world" target \(see [Step 2](https://www.postgresql.org/docs/12/install-procedure.html#BUILD)\). You can build and install all of them by running:

```text
make
make install
```

in the `contrib` directory of a configured source tree; or to build and install just one selected module, do the same in that module's subdirectory. Many of the modules have regression tests, which can be executed by running:

```text
make check
```

before installation or

```text
make installcheck
```

once you have a PostgreSQL server running.

If you are using a pre-packaged version of PostgreSQL, these modules are typically made available as a separate subpackage, such as `postgresql-contrib`.

Many modules supply new user-defined functions, operators, or types. To make use of one of these modules, after you have installed the code you need to register the new SQL objects in the database system. In PostgreSQL 9.1 and later, this is done by executing a [CREATE EXTENSION](https://www.postgresql.org/docs/12/sql-createextension.html) command. In a fresh database, you can simply do

```text
CREATE EXTENSION module_name;
```

This command must be run by a database superuser. This registers the new SQL objects in the current database only, so you need to run this command in each database that you want the module's facilities to be available in. Alternatively, run it in database `template1` so that the extension will be copied into subsequently-created databases by default.

Many modules allow you to install their objects in a schema of your choice. To do that, add `SCHEMA` _`schema_name`_ to the `CREATE EXTENSION` command. By default, the objects will be placed in your current creation target schema, which in turn defaults to `public`.

If your database was brought forward by dump and reload from a pre-9.1 version of PostgreSQL, and you had been using the pre-9.1 version of the module in it, you should instead do

```text
CREATE EXTENSION module_name FROM unpackaged;
```

This will update the pre-9.1 objects of the module into a proper _extension_ object. Future updates to the module will be managed by [ALTER EXTENSION](https://www.postgresql.org/docs/12/sql-alterextension.html). For more information about extension updates, see [Section 37.17](https://www.postgresql.org/docs/12/extend-extensions.html).

Note, however, that some of these modules are not “extensions” in this sense, but are loaded into the server in some other way, for instance by way of [shared\_preload\_libraries](https://www.postgresql.org/docs/12/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES). See the documentation of each module for details.

