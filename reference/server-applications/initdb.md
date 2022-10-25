# initdb

initdb — 建立一個新的 PostgreSQL 資料庫叢集

### 語法

`initdb` \[_`option`_...] \[ `--pgdata` | `-D` ] _`directory`_

### 說明

initdb 建立一個新的 PostgreSQL 資料庫叢集。資料庫叢集是以單一個伺服器實例管理許多資料庫的單位。

Creating a database cluster consists of creating the directories in which the database data will live, generating the shared catalog tables (tables that belong to the whole cluster rather than to any particular database), and creating the `template1` and `postgres` databases. When you later create a new database, everything in the `template1` database is copied. (Therefore, anything installed in `template1` is automatically copied into each database created later.) The `postgres` database is a default database meant for use by users, utilities and third party applications.

Although `initdb` will attempt to create the specified data directory, it might not have permission if the parent directory of the desired data directory is root-owned. To initialize in such a setup, create an empty data directory as root, then use `chown` to assign ownership of that directory to the database user account, then `su` to become the database user to run `initdb`.

`initdb` must be run as the user that will own the server process, because the server needs to have access to the files and directories that `initdb` creates. Since the server cannot be run as root, you must not run `initdb` as root either. (It will in fact refuse to do so.)

For security reasons the new cluster created by `initdb` will only be accessible by the cluster owner by default. The `--allow-group-access` option allows any user in the same group as the cluster owner to read files in the cluster. This is useful for performing backups as a non-privileged user.

`initdb` initializes the database cluster's default locale and character set encoding. The character set encoding, collation order (`LC_COLLATE`) and character set classes (`LC_CTYPE`, e.g. upper, lower, digit) can be set separately for a database when it is created. `initdb` determines those settings for the `template1` database, which will serve as the default for all other databases.

To alter the default collation order or character set classes, use the `--lc-collate` and `--lc-ctype` options. Collation orders other than `C` or `POSIX` also have a performance penalty. For these reasons it is important to choose the right locale when running `initdb`.

伺服器啟動以後，可以變更其餘的區域設定類別。您也可以使用 --locale 來設定所有語言環境類別的預設值，包括排序規則和字元集。可以透過 SHOW ALL 顯示所有伺服器區域設定值（lc\_ \*）。更多細節可以在 [23.1 節](../../server-administration/localization/locale-support.md)中找到。

要變更預設編碼，請使用 --encoding。更多細節可以在 [23.3 節](../../server-administration/localization/character-set-support.md)中找到。

### 選項

`-A`` `_`authmethod`_\
`--auth=`_`authmethod`_

此選項為 pg\_hba.conf 中使用的本地使用者（host 和 local 項目）指定預設的身份驗證方法。initdb 將使用指定的身份驗證方法預先設定 pg\_hba.conf 的項目，不論是非複寫使用者或是可複寫使用者。

除非您信任系統上的所有本地使用者，否則不要使用 trust。trust 是用於簡易安裝的預設選項。

`--auth-host=`_`authmethod`_

This option specifies the authentication method for local users via TCP/IP connections used in `pg_hba.conf` (`host` lines).

`--auth-local=`_`authmethod`_

This option specifies the authentication method for local users via Unix-domain socket connections used in `pg_hba.conf` (`local` lines).

`-D`` `_`directory`_\
`--pgdata=`_`directory`_

此選項指定資料庫叢集應儲存的目錄。這是 initdb 唯一需要的資訊，但是您可以避免使用這個選項，而是透過使用 PGDATA 環境變數來設定它。這很方便，因為資料庫伺服器（postgres）以後可以透過相同的變數找到資料庫目錄。

`-E`` `_`encoding`_\
`--encoding=`_`encoding`_

選擇樣板資料庫的編碼。這也是以後建立的任何資料庫的預設編碼，除非您在此處覆蓋它。預設值是從區域設定產生的；如果不起作用，則會回到 SQL\_ASCII。PostgreSQL 伺服器支援的字元集在[第 23.3.1 節](../../server-administration/localization/character-set-support.md#23-3-1-zhi-yuan-de-zi-yuan-ji)中說明。

`-g`\
`--allow-group-access`

Allows users in the same group as the cluster owner to read all cluster files created by `initdb`. This option is ignored on Windows as it does not support POSIX-style group permissions.

`-k`\
`--data-checksums`

Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. Enabling checksums may incur a noticeable performance penalty. If set, checksums are calculated for all objects, in all databases. All checksum failures will be reported in the [pg\_stat\_database](https://www.postgresql.org/docs/current/monitoring-stats.html#PG-STAT-DATABASE-VIEW) view.

`--locale=`_`locale`_

設定資料庫叢集的預設語言環境。如果未指定此選項，則語言環境將從 initdb 所執行的環境繼承。語言環境支援在 [23.1 節](../../server-administration/localization/locale-support.md)中的說明描述。

`--lc-collate=`_`locale`_\
`--lc-ctype=`_`locale`_\
`--lc-messages=`_`locale`_\
`--lc-monetary=`_`locale`_\
`--lc-numeric=`_`locale`_\
`--lc-time=`_`locale`_

Like `--locale`, but only sets the locale in the specified category.`--no-locale`

Equivalent to `--locale=C`.

`-N`\
`--no-sync`

By default, `initdb` will wait for all files to be written safely to disk. This option causes `initdb` to return without waiting, which is faster, but means that a subsequent operating system crash can leave the data directory corrupt. Generally, this option is useful for testing, but should not be used when creating a production installation.

`--pwfile=`_`filename`_

Makes `initdb` read the database superuser's password from a file. The first line of the file is taken as the password.

`-S`\
`--sync-only`

Safely write all database files to disk and exit. This does not perform any of the normal initdb operations.

`-T`` `_`config`_\
`--text-search-config=`_`config`_

Sets the default text search configuration. See [default\_text\_search\_config](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-DEFAULT-TEXT-SEARCH-CONFIG) for further information.

`-U`` `_`username`_\
`--username=`_`username`_

選擇資料庫超級使用者的使用者名稱。預設為執行 initdb 的有效使用者的名稱。超級使用者名稱到底是什麼並不重要，也可以選擇保留慣用名稱 postgres，即使與作業系統使用者名稱不同也沒有關係。

`-W`\
`--pwprompt`

使 initdb 提示輸入密碼以授予資料庫超級使用者。如果您不打算使用密碼身份驗證，那麼這並不重要。否則，在設定密碼之前，您將無法使用密碼身份驗證。

`-X`` `_`directory`_\
`--waldir=`_`directory`_

This option specifies the directory where the write-ahead log should be stored.

`--wal-segsize=`_`size`_

Set the _WAL segment size_, in megabytes. This is the size of each individual file in the WAL log. The default size is 16 megabytes. The value must be a power of 2 between 1 and 1024 (megabytes). This option can only be set during initialization, and cannot be changed later.

It may be useful to adjust this size to control the granularity of WAL log shipping or archiving. Also, in databases with a high volume of WAL, the sheer number of WAL files per directory can become a performance and management problem. Increasing the WAL file size will reduce the number of WAL files.

Other, less commonly used, options are also available:

`-d`\
`--debug`

Print debugging output from the bootstrap backend and a few other messages of lesser interest for the general public. The bootstrap backend is the program `initdb` uses to create the catalog tables. This option generates a tremendous amount of extremely boring output.

`-L`` `_`directory`_

指定 initdb 應該在哪裡找到其輸入檔案以初始化資料庫叢集。通常這不是必須的。系統將告知您是否需要明確指定其路徑。

`-n`\
`--no-clean`

By default, when `initdb` determines that an error prevented it from completely creating the database cluster, it removes any files it might have created before discovering that it cannot finish the job. This option inhibits tidying-up and is thus useful for debugging.

Other options:

`-V`\
`--version`

Print the initdb version and exit.

`-?`\
`--help`

Show help about initdb command line arguments, and exit.

### 環境變數

`PGDATA`

Specifies the directory where the database cluster is to be stored; can be overridden using the `-D` option.

`PG_COLOR`

Specifies whether to use color in diagnostics messages. Possible values are `always`, `auto`, `never`.

`TZ`

指定要建立的資料庫叢集的預設時區。該值應為完整的時區名稱（請參閱[第 8.5.3 節](../../the-sql-language/data-types/date-time.md#8-5-3-time-zones)）。

與大多數其他 PostgreSQL 工具程式一樣，此工具程式也使用 libpq 所支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

### 提醒

也可以透過 `pg_ctl initdb` 呼叫 `initdb`。

### 參閱

[pg\_ctl](pg\_ctl.md), [postgres](postgres.md)
