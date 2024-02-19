# CREATE EXTENSION

CREATE EXTENSION — install an extension

### 語法

```
CREATE EXTENSION [ IF NOT EXISTS ] extension_name
    [ WITH ] [ SCHEMA schema_name ]
             [ VERSION version ]
             [ CASCADE ]
```

### 說明

`CREATE EXTENSION` loads a new extension into the current database. There must not be an extension of the same name already loaded.

Loading an extension essentially amounts to running the extension's script file. The script will typically create new SQL objects such as functions, data types, operators and index support methods. `CREATE EXTENSION` additionally records the identities of all the created objects, so that they can be dropped again if `DROP EXTENSION` is issued.

The user who runs `CREATE EXTENSION` becomes the owner of the extension for purposes of later privilege checks, and normally also becomes the owner of any objects created by the extension's script.

Loading an extension ordinarily requires the same privileges that would be required to create its component objects. For many extensions this means superuser privileges are needed. However, if the extension is marked _trusted_ in its control file, then it can be installed by any user who has `CREATE` privilege on the current database. In this case the extension object itself will be owned by the calling user, but the contained objects will be owned by the bootstrap superuser (unless the extension's script explicitly assigns them to the calling user). This configuration gives the calling user the right to drop the extension, but not to modify individual objects within it.

### 參數

`IF NOT EXISTS`

Do not throw an error if an extension with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing extension is anything like the one that would have been created from the currently-available script file.

_`extension_name`_

The name of the extension to be installed. PostgreSQL will create the extension using details from the file `SHAREDIR/extension/`_`extension_name`_`.control`.

_`schema_name`_

The name of the schema in which to install the extension's objects, given that the extension allows its contents to be relocated. The named schema must already exist. If not specified, and the extension's control file does not specify a schema either, the current default object creation schema is used.

If the extension specifies a `schema` parameter in its control file, then that schema cannot be overridden with a `SCHEMA` clause. Normally, an error will be raised if a `SCHEMA` clause is given and it conflicts with the extension's `schema` parameter. However, if the `CASCADE` clause is also given, then _`schema_name`_ is ignored when it conflicts. The given _`schema_name`_ will be used for installation of any needed extensions that do not specify `schema` in their control files.

Remember that the extension itself is not considered to be within any schema: extensions have unqualified names that must be unique database-wide. But objects belonging to the extension can be within schemas.

_`version`_

The version of the extension to install. This can be written as either an identifier or a string literal. The default version is whatever is specified in the extension's control file.

`CASCADE`

Automatically install any extensions that this extension depends on that are not already installed. Their dependencies are likewise automatically installed, recursively. The `SCHEMA` clause, if given, applies to all extensions that get installed this way. Other options of the statement are not applied to automatically-installed extensions; in particular, their default versions are always selected.

### 註解

Before you can use `CREATE EXTENSION` to load an extension into a database, the extension's supporting files must be installed. Information about installing the extensions supplied with PostgreSQL can be found in [Additional Supplied Modules](https://www.postgresql.org/docs/current/contrib.html).

The extensions currently available for loading can be identified from the [`pg_available_extensions`](https://www.postgresql.org/docs/current/view-pg-available-extensions.html) or [`pg_available_extension_versions`](https://www.postgresql.org/docs/current/view-pg-available-extension-versions.html) system views.

####

{% hint style="info" %}
以超級使用者身份安裝擴展需要信任擴展的作者以安全的方式編寫擴展安裝腳本。對於惡意用戶來說，創建特洛伊木馬物件並不是非常困難，這些對象將損害以後粗心編寫的擴展腳本的執行，從而允許該用戶獲得超級用戶許可權。但是，特洛伊木馬物件僅在腳本執行期間位於search\_path中時才是危險的，這意味著它們位於擴展的安裝目標架構中或它所依賴的某個擴展的架構中。因此，在處理其腳本未經仔細審查的擴展時，一個好的經驗法則是僅將它們安裝到尚未授予任何不受信任的使用者的 CREATE 許可權的架構中。對於它們所依賴的任何擴展也是如此。

PostgreSQL提供的擴展被認為可以抵禦此類安裝時攻擊，除了少數依賴於其他擴展的擴展。如這些擴展的文件中所述，它們應安裝到安全架構中，或安裝到與它們所依賴的擴展相同的架構中，或兩者兼而有之。
{% endhint %}

有關設計新的延伸功能相關資訊，請參閱[第 38.17 節](../../server-programming/extending-sql/packaging-related-objects-into-an-extension.md)。

### 範例

將 hstore 延伸功能安裝到目前的資料庫中，將其物件置於 SCHEMA addons 中：

```
CREATE EXTENSION hstore SCHEMA addons;
```

同樣結果的另一種做法：

```
SET search_path = addons;
CREATE EXTENSION hstore;
```

## 相容性

CREATE EXTENSION 是 PostgreSQL 的延伸功能。

## 參閱

[ALTER EXTENSION](alter-extension.md), [DROP EXTENSION](drop-extension.md)
