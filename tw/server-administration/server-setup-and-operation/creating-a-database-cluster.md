# 18.2. Creating a Database Cluster

Before you can do anything, you must initialize a database storage area on disk. We call this a _database cluster_. \(The SQL standard uses the term catalog cluster.\) A database cluster is a collection of databases that is managed by a single instance of a running database server. After initialization, a database cluster will contain a database named `postgres`, which is meant as a default database for use by utilities, users and third party applications. The database server itself does not require the `postgres` database to exist, but many external utility programs assume it exists. Another database created within each cluster during initialization is called `template1`. As the name suggests, this will be used as a template for subsequently created databases; it should not be used for actual work. \(See [Chapter 22](https://www.postgresql.org/docs/12/managing-databases.html) for information about creating new databases within a cluster.\)

In file system terms, a database cluster is a single directory under which all data will be stored. We call this the _data directory_ or _data area_. It is completely up to you where you choose to store your data. There is no default, although locations such as `/usr/local/pgsql/data` or `/var/lib/pgsql/data` are popular. To initialize a database cluster, use the command [initdb](https://www.postgresql.org/docs/12/app-initdb.html), which is installed with PostgreSQL. The desired file system location of your database cluster is indicated by the `-D` option, for example:

```text
$ initdb -D /usr/local/pgsql/data
```

Note that you must execute this command while logged into the PostgreSQL user account, which is described in the previous section.

#### Tip

As an alternative to the `-D` option, you can set the environment variable `PGDATA`.

Alternatively, you can run `initdb` via the [pg\_ctl](https://www.postgresql.org/docs/12/app-pg-ctl.html) program like so:

```text
$ pg_ctl -D /usr/local/pgsql/data initdb
```

This may be more intuitive if you are using `pg_ctl` for starting and stopping the server \(see [Section 18.3](https://www.postgresql.org/docs/12/server-start.html)\), so that `pg_ctl` would be the sole command you use for managing the database server instance.

`initdb` will attempt to create the directory you specify if it does not already exist. Of course, this will fail if `initdb` does not have permissions to write in the parent directory. It's generally recommendable that the PostgreSQL user own not just the data directory but its parent directory as well, so that this should not be a problem. If the desired parent directory doesn't exist either, you will need to create it first, using root privileges if the grandparent directory isn't writable. So the process might look like this:

```text
root# mkdir /usr/local/pgsql
root# chown postgres /usr/local/pgsql
root# su postgres
postgres$ initdb -D /usr/local/pgsql/data
```

`initdb` will refuse to run if the data directory exists and already contains files; this is to prevent accidentally overwriting an existing installation.

Because the data directory contains all the data stored in the database, it is essential that it be secured from unauthorized access. `initdb` therefore revokes access permissions from everyone but the PostgreSQL user, and optionally, group. Group access, when enabled, is read-only. This allows an unprivileged user in the same group as the cluster owner to take a backup of the cluster data or perform other operations that only require read access.

Note that enabling or disabling group access on an existing cluster requires the cluster to be shut down and the appropriate mode to be set on all directories and files before restarting PostgreSQL. Otherwise, a mix of modes might exist in the data directory. For clusters that allow access only by the owner, the appropriate modes are `0700` for directories and `0600` for files. For clusters that also allow reads by the group, the appropriate modes are `0750` for directories and `0640` for files.

However, while the directory contents are secure, the default client authentication setup allows any local user to connect to the database and even become the database superuser. If you do not trust other local users, we recommend you use one of `initdb`'s `-W`, `--pwprompt` or `--pwfile` options to assign a password to the database superuser. Also, specify `-A md5` or `-A password` so that the default `trust` authentication mode is not used; or modify the generated `pg_hba.conf` file after running `initdb`, but _before_ you start the server for the first time. \(Other reasonable approaches include using `peer` authentication or file system permissions to restrict connections. See [Chapter 20](https://www.postgresql.org/docs/12/client-authentication.html) for more information.\)

`initdb` also initializes the default locale for the database cluster. Normally, it will just take the locale settings in the environment and apply them to the initialized database. It is possible to specify a different locale for the database; more information about that can be found in [Section 23.1](https://www.postgresql.org/docs/12/locale.html). The default sort order used within the particular database cluster is set by `initdb`, and while you can create new databases using different sort order, the order used in the template databases that initdb creates cannot be changed without dropping and recreating them. There is also a performance impact for using locales other than `C` or `POSIX`. Therefore, it is important to make this choice correctly the first time.

`initdb` also sets the default character set encoding for the database cluster. Normally this should be chosen to match the locale setting. For details see [Section 23.3](https://www.postgresql.org/docs/12/multibyte.html).

Non-`C` and non-`POSIX` locales rely on the operating system's collation library for character set ordering. This controls the ordering of keys stored in indexes. For this reason, a cluster cannot switch to an incompatible collation library version, either through snapshot restore, binary streaming replication, a different operating system, or an operating system upgrade.

## 18.2.1. Use of Secondary File Systems

Many installations create their database clusters on file systems \(volumes\) other than the machine's “root” volume. If you choose to do this, it is not advisable to try to use the secondary volume's topmost directory \(mount point\) as the data directory. Best practice is to create a directory within the mount-point directory that is owned by the PostgreSQL user, and then create the data directory within that. This avoids permissions problems, particularly for operations such as pg\_upgrade, and it also ensures clean failures if the secondary volume is taken offline.

## 18.2.2. File Systems

一般來說，任何具備 POSIX 標準的檔案系統都可以用於 PostgreSQL。 由於各種原因，使用者可能會使用不同的檔案系統，包括供應商支援、效能和熟悉程度。經驗上來說，在所有其他條件都相同的情況下，不應該僅因為切換檔案系統或進行次要的檔案系統配置變更，而期待效能或行為有明顯的改變。

### **18.2.2.1. NFS**

可以使用 NFS 檔案系統來儲存 PostgreSQL 資料目錄。PostgreSQL 對 NFS 檔案系統並沒有任何特殊的要求，這意味著它假設 NFS 的行為與本地連接的磁碟完全相同。PostgreSQL 不使用已知在NFS上具有非標準行為的任何功能，例如檔案鎖定。

將 NFS 與 PostgreSQL 一起使用時，唯一確定要求是使用 hard 選項安裝檔案系統。使用 hard 選項，如果出現網路問題，NFS 程序可以無限期「hang」（暫停），因此此配置將需要仔細的監控。如果出現網路問題，soft 選項會中斷系統呼，但是 PostgreSQL 不會重複以此方式中斷的系統呼叫，因此任何此類中斷都將導致回報 I/O 錯誤。

不必要使用同步（sync）掛載選項。 async 選項的行為就足夠了，因為 PostgreSQL 會在適當的時機發出 fsync 呼叫來強制緩衝寫入。（這類似於它在本機檔案系統上的工作方式。）但是，強烈建議在存在該檔案的系統（主要是 Linux）上的 NFS 伺服器上使用 sync export 選項。否則，實際上不能保證 NFS 用戶端上的 fsync 或等效檔案可以到達伺服器上的永久儲存，這可能導致損壞，類似於在關閉參數 fsync 的情況下提供服務。這些掛載和輸出選項的預設設定在不同的供應商和版本之間略所不同，因此建議在任何情況下都需要進行檢查並且明確指定它們的內容，以避免任何誤解。

在某些情況下，可以透過 NFS 或更低等級的通訊協定（例如 iSCSI）存取外部儲存產品。在後者，儲存裝置為 block device，可以在其上建立任何可用的檔案系統。這種方法可能使 DBA 不必處理 NFS 的某些特質，不過，管理遠端儲存服務的複雜性會仍發生在其他層級之中。

