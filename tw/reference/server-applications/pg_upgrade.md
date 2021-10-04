# pg\_upgrade

pg\_upgrade — 升級 PostgreSQL 伺服器服務

### `語法`

`pg_upgrade` `-b` _`oldbindir`_ `-B` _`newbindir`_ `-d` _`oldconfigdir`_ `-D` _`newconfigdir`_ \[_`option`_...\]

### 說明

pg\_upgrade（以前稱為 pg\_migrator）可以將儲存在 PostgreSQL 資料檔案中的內容升級到更高主版本的 PostgreSQL，而毋需進行資料的匯出匯入，例如從 9.5.8 到 9.6.4 或從 10.7 到 11.2。對於次要版本升級，例如從 9.6.2 升級到 9.6.3 或從 10.1 升級到 10.2，則不需要使用這個工具。

PostgreSQL 的主要發行版會定期增加新的功能，這些新功能通常會變更系統資料表的結構，不過內部資料儲存格式很少更改。pg\_upgrade 透過建立新的系統資料表並且簡單地重新連結舊的使用者資料檔案數據來執行快速升級。如果將來的主要發行版曾經以使舊資料格式無法讀取的方式變更了資料儲存格式，則 pg\_upgrade 將無法用於此類升級。 （社群會儘量避免這種情況發生。）

pg\_upgrade 盡最大努力確保新舊叢集是 binary-compatible．例如，透過檢查相容的編譯設定（包括 32/64 位元的二進位內容）來確保。儘管 pg\_upgrade 無法檢查，但是任何外部模組也是二進位相容的，這一點很重要。

pg\_upgrade 支援從 8.4.X 及更高版本升級到 PostgreSQL 的目前主要版本，包括快照和 beta 版本。

### 選項

pg\_upgrade 接受以下命令列參數：

`-b` _`bindir`_  
`--old-bindir=`_`bindir`_

the old PostgreSQL executable directory; environment variable `PGBINOLD`

`-B` _`bindir`_  
`--new-bindir=`_`bindir`_

the new PostgreSQL executable directory; default is the directory where pg\_upgrade resides; environment variable `PGBINNEW`

`-c`  
`--check`

check clusters only, don't change any data

`-d` _`configdir`_  
`--old-datadir=`_`configdir`_

the old database cluster configuration directory; environment variable `PGDATAOLD`

`-D` _`configdir`_  
`--new-datadir=`_`configdir`_

the new database cluster configuration directory; environment variable `PGDATANEW`

`-j` _`njobs`_  
`--jobs=`_`njobs`_

number of simultaneous processes or threads to use

`-k`  
`--link`

use hard links instead of copying files to the new cluster

`-o` _`options`_  
`--old-options` _`options`_

options to be passed directly to the old `postgres` command; multiple option invocations are appended

`-O` _`options`_  
`--new-options` _`options`_

options to be passed directly to the new `postgres` command; multiple option invocations are appended

`-p` _`port`_  
`--old-port=`_`port`_

the old cluster port number; environment variable `PGPORTOLD`

`-P` _`port`_  
`--new-port=`_`port`_

the new cluster port number; environment variable `PGPORTNEW`

`-r`  
`--retain`

retain SQL and log files even after successful completion

`-s` _`dir`_  
`--socketdir=`_`dir`_

directory to use for postmaster sockets during upgrade; default is current working directory; environment variable `PGSOCKETDIR`

`-U` _`username`_  
`--username=`_`username`_

cluster's install user name; environment variable `PGUSER`

`-v`  
`--verbose`

enable verbose internal logging

`-V`  
`--version`

display version information, then exit

`--clone`

Use efficient file cloning \(also known as “reflinks” on some systems\) instead of copying files to the new cluster. This can result in near-instantaneous copying of the data files, giving the speed advantages of `-k`/`--link` while leaving the old cluster untouched.

File cloning is only supported on some operating systems and file systems. If it is selected but not supported, the pg\_upgrade run will error. At present, it is supported on Linux \(kernel 4.5 or later\) with Btrfs and XFS \(on file systems created with reflink support\), and on macOS with APFS.

`-?`  
`--help`

show help, then exit

### 使用

這些是使用 pg\_upgrade 進行升級的步驟：

1. **（選擇性）移動舊叢集目錄**

   如果你使用的是特定於版本的安裝目錄，例如 /opt/PostgreSQL/13，則毋須移動舊叢集。圖形安裝程序均使用特定於版本的安裝目錄。如果您的安裝目錄不是特定於版本的，例如 /usr/local/pgsql，則必須移動目前的 PostgreSQL 安裝目錄，以免干擾新的 PostgreSQL 安裝。一旦關閉目前的 PostgreSQL 伺服器，就可以重新命名 PostgreSQL 安裝目錄了。假設舊目錄為 /usr/local/pgsql，則可以執行以下操作：

   ```text
   mv /usr/local/pgsql /usr/local/pgsql.old
   ```

   重新命名該目錄。

2. **對於以原始碼安裝的使用者，請編譯新的版本**

   使用與舊叢集相容的 configure 選項編譯新的 PostgreSQL 原始碼。pg\_upgrade 將在開始升級之前檢查 pg\_controldata 以確保所有設定是相容的。

3. **安裝新的 PostgreSQL 編譯後可執行檔案**

   Install the new server's binaries and support files. pg\_upgrade is included in a default installation.

   For source installs, if you wish to install the new server in a custom location, use the `prefix` variable:

   ```text
   make prefix=/usr/local/pgsql.new install
   ```

4. **初始化新的 PostgreSQL 叢集**

   Initialize the new cluster using `initdb`. Again, use compatible `initdb` flags that match the old cluster. Many prebuilt installers do this step automatically. There is no need to start the new cluster.

5. **安裝自訂的共享物件檔案**

   Install any custom shared object files \(or DLLs\) used by the old cluster into the new cluster, e.g., `pgcrypto.so`, whether they are from `contrib` or some other source. Do not install the schema definitions, e.g., `CREATE EXTENSION pgcrypto`, because these will be upgraded from the old cluster. Also, any custom full text search files \(dictionary, synonym, thesaurus, stop words\) must also be copied to the new cluster.

6. **調整身份認證**

   `pg_upgrade` will connect to the old and new servers several times, so you might want to set authentication to `peer` in `pg_hba.conf` or use a `~/.pgpass` file \(see [Section 33.15](https://www.postgresql.org/docs/13/libpq-pgpass.html)\).

7. **停止兩個伺服器服務**

   Make sure both database servers are stopped using, on Unix, e.g.:

   ```text
   pg_ctl -D /opt/PostgreSQL/9.6 stop
   pg_ctl -D /opt/PostgreSQL/13 stop
   ```

   or on Windows, using the proper service names:

   ```text
   NET STOP postgresql-9.6
   NET STOP postgresql-13
   ```

   Streaming replication and log-shipping standby servers can remain running until a later step.

8. **準備備用伺服器的升級**

   If you are upgrading standby servers using methods outlined in section [Step 10](https://www.postgresql.org/docs/13/pgupgrade.html#PGUPGRADE-STEP-REPLICAS), verify that the old standby servers are caught up by running pg\_controldata against the old primary and standby clusters. Verify that the “Latest checkpoint location” values match in all clusters. \(There will be a mismatch if old standby servers were shut down before the old primary or if the old standby servers are still running.\) Also, make sure `wal_level` is not set to `minimal` in the `postgresql.conf` file on the new primary cluster.

9. **執行 pg\_upgrade**

   Always run the pg\_upgrade binary of the new server, not the old one. pg\_upgrade requires the specification of the old and new cluster's data and executable \(`bin`\) directories. You can also specify user and port values, and whether you want the data files linked or cloned instead of the default copy behavior.

   If you use link mode, the upgrade will be much faster \(no file copying\) and use less disk space, but you will not be able to access your old cluster once you start the new cluster after the upgrade. Link mode also requires that the old and new cluster data directories be in the same file system. \(Tablespaces and `pg_wal` can be on different file systems.\) Clone mode provides the same speed and disk space advantages but does not cause the old cluster to be unusable once the new cluster is started. Clone mode also requires that the old and new data directories be in the same file system. This mode is only available on certain operating systems and file systems.

   The `--jobs` option allows multiple CPU cores to be used for copying/linking of files and to dump and reload database schemas in parallel; a good place to start is the maximum of the number of CPU cores and tablespaces. This option can dramatically reduce the time to upgrade a multi-database server running on a multiprocessor machine.

   For Windows users, you must be logged into an administrative account, and then start a shell as the `postgres` user and set the proper path:

   ```text
   RUNAS /USER:postgres "CMD.EXE"
   SET PATH=%PATH%;C:\Program Files\PostgreSQL\13\bin;
   ```

   and then run pg\_upgrade with quoted directories, e.g.:

   ```text
   pg_upgrade.exe
           --old-datadir "C:/Program Files/PostgreSQL/9.6/data"
           --new-datadir "C:/Program Files/PostgreSQL/13/data"
           --old-bindir "C:/Program Files/PostgreSQL/9.6/bin"
           --new-bindir "C:/Program Files/PostgreSQL/13/bin"
   ```

   Once started, `pg_upgrade` will verify the two clusters are compatible and then do the upgrade. You can use `pg_upgrade --check` to perform only the checks, even if the old server is still running. `pg_upgrade --check` will also outline any manual adjustments you will need to make after the upgrade. If you are going to be using link or clone mode, you should use the option `--link` or `--clone` with `--check` to enable mode-specific checks. `pg_upgrade` requires write permission in the current directory.

   Obviously, no one should be accessing the clusters during the upgrade. pg\_upgrade defaults to running servers on port 50432 to avoid unintended client connections. You can use the same port number for both clusters when doing an upgrade because the old and new clusters will not be running at the same time. However, when checking an old running server, the old and new port numbers must be different.

   If an error occurs while restoring the database schema, `pg_upgrade` will exit and you will have to revert to the old cluster as outlined in [Step 16](https://www.postgresql.org/docs/13/pgupgrade.html#PGUPGRADE-STEP-REVERT) below. To try `pg_upgrade` again, you will need to modify the old cluster so the pg\_upgrade schema restore succeeds. If the problem is a `contrib` module, you might need to uninstall the `contrib` module from the old cluster and install it in the new cluster after the upgrade, assuming the module is not being used to store user data.

10. **升級串流複寫和日誌轉送的備用伺服器**

    If you used link mode and have Streaming Replication \(see [Section 26.2.5](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION)\) or Log-Shipping \(see [Section 26.2](https://www.postgresql.org/docs/13/warm-standby.html)\) standby servers, you can follow these steps to quickly upgrade them. You will not be running pg\_upgrade on the standby servers, but rather rsync on the primary. Do not start any servers yet.

    If you did _not_ use link mode, do not have or do not want to use rsync, or want an easier solution, skip the instructions in this section and simply recreate the standby servers once pg\_upgrade completes and the new primary is running.

    1. **Install the new PostgreSQL binaries on standby servers**

       Make sure the new binaries and support files are installed on all standby servers.

    2. **Make sure the new standby data directories do** _**not**_ **exist**

       Make sure the new standby data directories do _not_ exist or are empty. If initdb was run, delete the standby servers' new data directories.

    3. **Install custom shared object files**

       Install the same custom shared object files on the new standbys that you installed in the new primary cluster.

    4. **Stop standby servers**

       If the standby servers are still running, stop them now using the above instructions.

    5. **Save configuration files**

       Save any configuration files from the old standbys' configuration directories you need to keep, e.g., `postgresql.conf` \(and any files included by it\), `postgresql.auto.conf`, `pg_hba.conf`, because these will be overwritten or removed in the next step.

    6. **Run rsync**

       When using link mode, standby servers can be quickly upgraded using rsync. To accomplish this, from a directory on the primary server that is above the old and new database cluster directories, run this on the _primary_ for each standby server:

       ```text
       rsync --archive --delete --hard-links --size-only --no-inc-recursive old_cluster new_cluster remote_dir
       ```

       where `old_cluster` and `new_cluster` are relative to the current directory on the primary, and `remote_dir` is _above_ the old and new cluster directories on the standby. The directory structure under the specified directories on the primary and standbys must match. Consult the rsync manual page for details on specifying the remote directory, e.g.,

       ```text
       rsync --archive --delete --hard-links --size-only --no-inc-recursive /opt/PostgreSQL/9.5 \
             /opt/PostgreSQL/9.6 standby.example.com:/opt/PostgreSQL
       ```

       You can verify what the command will do using rsync's `--dry-run` option. While rsync must be run on the primary for at least one standby, it is possible to run rsync on an upgraded standby to upgrade other standbys, as long as the upgraded standby has not been started.

       What this does is to record the links created by pg\_upgrade's link mode that connect files in the old and new clusters on the primary server. It then finds matching files in the standby's old cluster and creates links for them in the standby's new cluster. Files that were not linked on the primary are copied from the primary to the standby. \(They are usually small.\) This provides rapid standby upgrades. Unfortunately, rsync needlessly copies files associated with temporary and unlogged tables because these files don't normally exist on standby servers.

       If you have tablespaces, you will need to run a similar rsync command for each tablespace directory, e.g.:

       ```text
       rsync --archive --delete --hard-links --size-only --no-inc-recursive /vol1/pg_tblsp/PG_9.5_201510051 \
             /vol1/pg_tblsp/PG_9.6_201608131 standby.example.com:/vol1/pg_tblsp
       ```

       If you have relocated `pg_wal` outside the data directories, rsync must be run on those directories too.

    7. **Configure streaming replication and log-shipping standby servers**

       Configure the servers for log shipping. \(You do not need to run `pg_start_backup()` and `pg_stop_backup()` or take a file system backup as the standbys are still synchronized with the primary.\)

11. **恢復 pg\_hba.conf**

    If you modified `pg_hba.conf`, restore its original settings. It might also be necessary to adjust other configuration files in the new cluster to match the old cluster, e.g., `postgresql.conf` \(and any files included by it\), `postgresql.auto.conf`.

12. **啟動新的伺服器**

    The new server can now be safely started, and then any rsync'ed standby servers.

13. **升級後處理程序**

    If any post-upgrade processing is required, pg\_upgrade will issue warnings as it completes. It will also generate script files that must be run by the administrator. The script files will connect to each database that needs post-upgrade processing. Each script should be run using:

    ```text
    psql --username=postgres --file=script.sql postgres
    ```

    The scripts can be run in any order and can be deleted once they have been run.

    **Caution**

    In general it is unsafe to access tables referenced in rebuild scripts until the rebuild scripts have run to completion; doing so could yield incorrect results or poor performance. Tables not referenced in rebuild scripts can be accessed immediately.

14. **統計資訊**

    Because optimizer statistics are not transferred by `pg_upgrade`, you will be instructed to run a command to regenerate that information at the end of the upgrade. You might need to set connection parameters to match your new cluster.

15. **刪除舊的叢集檔案**

    Once you are satisfied with the upgrade, you can delete the old cluster's data directories by running the script mentioned when `pg_upgrade` completes. \(Automatic deletion is not possible if you have user-defined tablespaces inside the old data directory.\) You can also delete the old installation directories \(e.g., `bin`, `share`\).

16. **還原到舊的叢集**

    If, after running `pg_upgrade`, you wish to revert to the old cluster, there are several options:

    * If the `--check` option was used, the old cluster was unmodified; it can be restarted.
    * If the `--link` option was _not_ used, the old cluster was unmodified; it can be restarted.
    * If the `--link` option was used, the data files might be shared between the old and new cluster:
      * If `pg_upgrade` aborted before linking started, the old cluster was unmodified; it can be restarted.
      * If you did _not_ start the new cluster, the old cluster was unmodified except that, when linking started, a `.old` suffix was appended to `$PGDATA/global/pg_control`. To reuse the old cluster, remove the `.old` suffix from `$PGDATA/global/pg_control`; you can then restart the old cluster.
      * If you did start the new cluster, it has written to shared files and it is unsafe to use the old cluster. The old cluster will need to be restored from backup in this case.

### 其他注意事項

pg\_upgrade 在目前工作目錄中建立各種工作檔案，例如資料庫結構轉存。為了安全起見，請確保該目錄不能被任何其他使用者讀取或寫入。

pg\_upgrade 在舊的和新的資料目錄中啟動短暫的 postmasters。預設情況下，與這些 postmasters 進行通訊的 Unix socket 檔案是在目前工作目錄中建立的。在某些情況下，目前目錄的路徑名稱可能會太長而無法成為有效的 Unix socket 名稱。在這種情況下，可以使用 -s 選項將 Unix socket 檔案放在路徑名稱較短的某個目錄中。為了安全起見，請確保該目錄不能被任何其他使用者讀取或寫入。 （Windows 不支援此功能。）

所有失敗、重建和重新索引的失敗影響到安裝情況，將由 pg\_upgrade 回報。用於重建資料表和索引的升級後腳本將自動產生。如果要自動執行許多叢集的升級，則應該發現具有相同資料庫架構的叢集對於所有叢集升級都需要相同的升級後步驟； 這是因為升級後的步驟基於資料庫結構，而不是使用者的資料。

所以為了進行部署測試，請建立舊叢集僅含結構的副本，插入虛擬資料，然後進行升級測試。

pg\_upgrade 不支援使用以下 reg\* OID 引用系統資料型別的資料表欄位的資料庫：

| `regcollation` |
| :--- |
| `regconfig` |
| `regdictionary` |
| `regnamespace` |
| `regoper` |
| `regoperator` |
| `regproc` |
| `regprocedure` |

\(`regclass`, `regrole`, and `regtype` can be upgraded.\)

If you are upgrading a pre-PostgreSQL 9.2 cluster that uses a configuration-file-only directory, you must pass the real data directory location to pg\_upgrade, and pass the configuration directory location to the server, e.g., `-d /real-data-directory -o '-D /configuration-directory'`.

If using a pre-9.1 old server that is using a non-default Unix-domain socket directory or a default that differs from the default of the new cluster, set `PGHOST` to point to the old server's socket location. \(This is not relevant on Windows.\)

If you want to use link mode and you do not want your old cluster to be modified when the new cluster is started, consider using the clone mode. If that is not available, make a copy of the old cluster and upgrade that in link mode. To make a valid copy of the old cluster, use `rsync` to create a dirty copy of the old cluster while the server is running, then shut down the old server and run `rsync --checksum` again to update the copy with any changes to make it consistent. \(`--checksum` is necessary because `rsync` only has file modification-time granularity of one second.\) You might want to exclude some files, e.g., `postmaster.pid`, as documented in [Section 25.3.3](https://www.postgresql.org/docs/13/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP). If your file system supports file system snapshots or copy-on-write file copies, you can use that to make a backup of the old cluster and tablespaces, though the snapshot and copies must be created simultaneously or while the database server is down.

### 參閱

[initdb](initdb.md), [pg\_ctl](pg_ctl.md), [pg\_dump](../client-applications/pg_dump.md), [postgres](postgres.md)

