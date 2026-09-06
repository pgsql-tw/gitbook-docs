# F. 延伸支援模組

This appendix and the next one contain information regarding the modules that can be found in the `contrib` directory of the PostgreSQL distribution. These include porting tools, analysis utilities, and plug-in features that are not part of the core PostgreSQL system, mainly because they address a limited audience or are too experimental to be part of the main source tree. This does not preclude their usefulness.

本附錄涵蓋了 contrib 中的延伸功能和其他伺服器外掛模組，[附錄 G](../additional-supplied-programs/) 為工具程式的說明。

從原始碼編譯建置時，這些模組並不會自動編譯，除非您有編譯 “world” （參閱[第 2 步](../../server-administration/installation-from-source-code/installation-procedure.md)）。 您可以透過執行以下命令來編譯和安裝這些模組：

<pre><code><strong>make
</strong><strong>make install
</strong></code></pre>

in the `contrib` directory of a configured source tree; or to build and install just one selected module, do the same in that module's subdirectory. Many of the modules have regression tests, which can be executed by running:

<pre><code><strong>make check
</strong></code></pre>

before installation or

<pre><code><strong>make installcheck
</strong></code></pre>

once you have a PostgreSQL server running.

If you are using a pre-packaged version of PostgreSQL, these modules are typically made available as a separate subpackage, such as `postgresql-contrib`.

許多模組提供新的使用者定義函數、運算子或型別。 要使用這些模組之一，在安裝程式後，您需要在資料庫系統中註冊新的 SQL 物件。 這是透過執行 [CREATE EXTENSION](../../reference/sql-commands/create-extension.md) 指令來完成的。 在一個新的資料庫中，你可以簡單地執行：

```
CREATE EXTENSION module_name;
```

This command registers the new SQL objects in the current database only, so you need to run it in each database that you want the module's facilities to be available in. Alternatively, run it in database `template1` so that the extension will be copied into subsequently-created databases by default.

For all these modules, `CREATE EXTENSION` must be run by a database superuser, unless the module is considered “trusted”, in which case it can be run by any user who has `CREATE` privilege on the current database. Modules that are trusted are identified as such in the sections that follow. Generally, trusted modules are ones that cannot provide access to outside-the-database functionality.

Many modules allow you to install their objects in a schema of your choice. To do that, add `SCHEMA`` `_`schema_name`_ to the `CREATE EXTENSION` command. By default, the objects will be placed in your current creation target schema, which in turn defaults to `public`.

Note, however, that some of these modules are not “extensions” in this sense, but are loaded into the server in some other way, for instance by way of [shared\_preload\_libraries](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES). See the documentation of each module for details.
