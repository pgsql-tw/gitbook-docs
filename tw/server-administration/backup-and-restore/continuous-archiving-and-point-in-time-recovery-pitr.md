# 25.3. Continuous Archiving and Point-in-Time Recovery \(PITR\)

PostgreSQL 在執行過程中不斷地在叢集資料目錄的 pg\_wal/ 子目錄中維護一個交易日誌（Write Ahead Log, WAL）。日誌記錄了對資料庫資料檔案所做的所有變更。該日誌主要用於意外災難還原的目的：如果系統意外損毁，則可以透過「重播」自上一個檢查點以來所建立的日誌項目來恢復資料庫的一致性。然而，日誌的存在使得可以使用第三種策略來備份數據庫：我們可以將檔案系統級備份與 WAL 檔案備份結合在一起。 如果需要復原，我們將還原檔案系統備份，然後從備份的 WAL 檔案中重播以使系統進入當下的狀態。 與前面所介紹的方法相比，這種方法的管理更為複雜，但具有一些明顯的好處：

* 我們不需要完美一致的檔案系統備份作為起點。備份中的任何內部不一致都將透過日誌重播進行糾正（這與損毁復原期間發生的變化沒有太大不同）。因此，我們不需要檔案系統的快照功能，而只需要 tar 或類似的封存工具。
* 由於我們可以結合無限長的 WAL 檔案序列進行重播，因此只需繼續封存 WAL 檔案就可以實現連續備份。這對於大型資料庫來說尤其具有價值，在大型資料庫中，經常性進行完整備份可能不太方便。
* 不必一直重複播放 WAL 項目。我們可以隨時停止重播，並獲得當時的資料庫快照。因此，此技術支持時間點還原：自從進行基本備份以來，可以隨時將資料庫還原到其狀態。
* 如果我們將一系列 WAL 檔案連續提供給另一台已載入了相同基本備份檔案的伺服器，則我們將擁有一個熱備份系統：在任何時候，我們都可以啟動第二台伺服器，而該伺服器將具有近乎最新的資料庫副本。

{% hint style="info" %}
pg\_dump 和 pg\_dumpall 並不會產生檔案系統層級的備份，因此不能用於連續歸檔解決方案的一部分。這樣的備份是邏輯上的，並且沒有包含足夠的資訊供 WAL 重播使用。
{% endhint %}

與普通資料系統備份技術一樣，此方法只能支援還原整個資料庫叢集，而不支援部份還原。此外，它還需要大量的檔案儲存空間：基本備份可能會很龐大，繁忙的系統將產生成許多數 MegaByte 等級的 WAL 流量，必須對其進行封存。儘管如此，在許多需要高可靠性的情況下，它還是備份技術中的首選。

要使用連續歸檔（許多資料庫供應商也將其稱為「線上備份」）成功恢復，您需要連續的 WAL 歸檔序列，該序列至少可以延伸到備份的開始時間。因此，在開始第一次基本備份之前，應先設定並測試用於封存 WAL 檔案的程序。因此，我們首先討論封存 WAL 檔案的機制。

## 25.3.1. 設定 WAL 檔案封存

從抽象的意義上講，執行中的 PostgreSQL 系統會產生無限長的 WAL 記錄序列。系統從物理上將此序列劃分為 WAL 分段檔案，每個檔案通常為16MB（儘管分段大小可以在 initdb 期間變更）。 分段檔案被賦予數字名稱，以反映它們在抽象的 WAL 序列中的位置。當不使用 WAL 歸檔時，系統通常只建立幾個分段檔案，然後透過將不再需要的分段檔案重新命名為較高的分段號號來「回收」它們。假設其內容在最後一個檢查點之前的分段檔案不再受關注時，即為可以回收。

歸檔處理 WAL 資料時，我們需要在每個分段檔案填滿後取得其內容，並將該資料保存在回收分段檔案以供重用之前的某個位置。根據應用程序和可用硬體的不同，可能有許多不同的「將資料保存到某處」的方式：我們可以將分段檔案複製到另一台主機上 NFS 掛載的目錄中，然後將它們寫入磁帶中（確保您擁有 一種識別每個檔案的原始名稱的方法），或者將它們一起批次處理並燒錄到 CD 上，或者也可以完全燒錄所有資料。為了給資料庫管理者提供靈活性，PostgreSQL 嘗試不對如何完成歸檔做任何假設。相反地，PostgreSQL 讓管理者指定要執行的 shell 命令，以將完整的分段檔案複製到需要的位置。該命令可以像 cp 一樣簡單，也可以呼叫複雜的 shell 腳本—一切由你決定。

要啟用 WAL 歸檔機制，請將 [wal\_level](../server-configuration/write-ahead-log.md) 組態參數設定為 replica 或更高的等級，將 [archive\_mode](../server-configuration/write-ahead-log.md#19-5-3-archiving) 設定為 on，然後在 [archive\_command](../server-configuration/write-ahead-log.md#19-5-3-archiving) 組態參數中指定要使用的 shell 命令。實際上，這些設定始終會放置在 postgresql.conf 檔案中。在 archive\_command 中，％p 替換為要存檔的檔案路徑名稱，而 ％f 僅替換為檔案名稱。（路徑名稱是相對於目前的工作目錄（即叢集的資料目錄）的。）如果需要在命令中嵌入實際的 ％ 字符，請使用 %%。最簡單的指令是：

```text
archive_command = 'test ! -f /mnt/server/archivedir/%f && cp %p /mnt/server/archivedir/%f'  # Unix
archive_command = 'copy "%p" "C:\\server\\archivedir\\%f"'  # Windows
```

它將可歸檔的 WAL 分段檔案複製到目錄 /mnt/server/archivedir 中。 （這是範例，而不是建議，並且可能不是所有平台都適用。）替換 ％p 和 ％f 參數後，實際執行的命令可能如下所示：

```text
test ! -f /mnt/server/archivedir/00000001000000A900000065 && cp pg_wal/00000001000000A900000065 /mnt/server/archivedir/00000001000000A900000065
```

將為每個要歸檔的新檔案產生一個類似的命令。

將以執行 PostgreSQL 伺服器的同一用戶的所有權執行 archive 命令。由於要歸檔的一系列 WAL 檔案實際上包含了資料庫中的所有內容，因此您將要確保已歸檔的資料受到保護，以免被窺探；例如，應該存檔到沒有同群組使用者，所有其他人都沒有讀取權限的目錄中。

重要的是，檔案封存指令只有在成功時才回傳零並且退出。結果為零時，PostgreSQL 將假設該檔案已成功封存，將會刪除或回收它。但是，回傳非零的狀態將會告訴 PostgreSQL 該檔案尚未封存。它將定期重試，直到成功為止。

通常應將 archive 指令設計為拒絕覆蓋任何先前存在的封存檔案。這是一種重要的安全設定，可以在管理員出錯（例如將兩個不同伺服器的輸出發送到同一封存目錄）時保持封存檔案的完整性。

仍然建議測試的封存指令以確保它確實不會覆蓋現有檔案，並且在這種情況下會回傳非零的結果。上面用於 Unix 的範例指令透過包含一個單獨的測試步驟來確保這一點。在某些 Unix 平台上，cp 具有諸如 -i 之類的選項，這些選項可用於更輕鬆地完成相同的操作，但是在不驗證是否回傳正確結束狀態的情況下，請不要依賴這些選項。（特別是，當使用 -i 並且目標檔案已經存在時，GNU cp 將回傳零，這並不是 PostgreSQL 所預期的行為。）

While designing your archiving setup, consider what will happen if the archive command fails repeatedly because some aspect requires operator intervention or the archive runs out of space. For example, this could occur if you write to tape without an autochanger; when the tape fills, nothing further can be archived until the tape is swapped. You should ensure that any error condition or request to a human operator is reported appropriately so that the situation can be resolved reasonably quickly. The `pg_wal/` directory will continue to fill with WAL segment files until the situation is resolved. \(If the file system containing `pg_wal/` fills up, PostgreSQL will do a PANIC shutdown. No committed transactions will be lost, but the database will remain offline until you free some space.\)

The speed of the archiving command is unimportant as long as it can keep up with the average rate at which your server generates WAL data. Normal operation continues even if the archiving process falls a little behind. If archiving falls significantly behind, this will increase the amount of data that would be lost in the event of a disaster. It will also mean that the `pg_wal/` directory will contain large numbers of not-yet-archived segment files, which could eventually exceed available disk space. You are advised to monitor the archiving process to ensure that it is working as you intend.

In writing your archive command, you should assume that the file names to be archived can be up to 64 characters long and can contain any combination of ASCII letters, digits, and dots. It is not necessary to preserve the original relative path \(`%p`\) but it is necessary to preserve the file name \(`%f`\).

Note that although WAL archiving will allow you to restore any modifications made to the data in your PostgreSQL database, it will not restore changes made to configuration files \(that is, `postgresql.conf`, `pg_hba.conf` and `pg_ident.conf`\), since those are edited manually rather than through SQL operations. You might wish to keep the configuration files in a location that will be backed up by your regular file system backup procedures. See [Section 19.2](https://www.postgresql.org/docs/12/runtime-config-file-locations.html) for how to relocate the configuration files.

The archive command is only invoked on completed WAL segments. Hence, if your server generates only little WAL traffic \(or has slack periods where it does so\), there could be a long delay between the completion of a transaction and its safe recording in archive storage. To put a limit on how old unarchived data can be, you can set [archive\_timeout](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-ARCHIVE-TIMEOUT) to force the server to switch to a new WAL segment file at least that often. Note that archived files that are archived early due to a forced switch are still the same length as completely full files. It is therefore unwise to set a very short `archive_timeout` — it will bloat your archive storage. `archive_timeout` settings of a minute or so are usually reasonable.

Also, you can force a segment switch manually with `pg_switch_wal` if you want to ensure that a just-finished transaction is archived as soon as possible. Other utility functions related to WAL management are listed in [Table 9.84](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-BACKUP-TABLE).

When `wal_level` is `minimal` some SQL commands are optimized to avoid WAL logging, as described in [Section 14.4.7](https://www.postgresql.org/docs/12/populate.html#POPULATE-PITR). If archiving or streaming replication were turned on during execution of one of these statements, WAL would not contain enough information for archive recovery. \(Crash recovery is unaffected.\) For this reason, `wal_level` can only be changed at server start. However, `archive_command` can be changed with a configuration file reload. If you wish to temporarily stop archiving, one way to do it is to set `archive_command` to the empty string \(`''`\). This will cause WAL files to accumulate in `pg_wal/` until a working `archive_command` is re-established.

## 25.3.2. Making a Base Backup

The easiest way to perform a base backup is to use the [pg\_basebackup](https://www.postgresql.org/docs/12/app-pgbasebackup.html) tool. It can create a base backup either as regular files or as a tar archive. If more flexibility than [pg\_basebackup](https://www.postgresql.org/docs/12/app-pgbasebackup.html) can provide is required, you can also make a base backup using the low level API \(see [Section 25.3.3](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP)\).

It is not necessary to be concerned about the amount of time it takes to make a base backup. However, if you normally run the server with `full_page_writes` disabled, you might notice a drop in performance while the backup runs since `full_page_writes` is effectively forced on during backup mode.

To make use of the backup, you will need to keep all the WAL segment files generated during and after the file system backup. To aid you in doing this, the base backup process creates a _backup history file_ that is immediately stored into the WAL archive area. This file is named after the first WAL segment file that you need for the file system backup. For example, if the starting WAL file is `0000000100001234000055CD` the backup history file will be named something like `0000000100001234000055CD.007C9330.backup`. \(The second part of the file name stands for an exact position within the WAL file, and can ordinarily be ignored.\) Once you have safely archived the file system backup and the WAL segment files used during the backup \(as specified in the backup history file\), all archived WAL segments with names numerically less are no longer needed to recover the file system backup and can be deleted. However, you should consider keeping several backup sets to be absolutely certain that you can recover your data.

The backup history file is just a small text file. It contains the label string you gave to [pg\_basebackup](https://www.postgresql.org/docs/12/app-pgbasebackup.html), as well as the starting and ending times and WAL segments of the backup. If you used the label to identify the associated dump file, then the archived history file is enough to tell you which dump file to restore.

Since you have to keep around all the archived WAL files back to your last base backup, the interval between base backups should usually be chosen based on how much storage you want to expend on archived WAL files. You should also consider how long you are prepared to spend recovering, if recovery should be necessary — the system will have to replay all those WAL segments, and that could take awhile if it has been a long time since the last base backup.

## 25.3.3. 使用低階 API 進行基本備份

使用低階 API 進行基本備份的程序比 [pg\_basebackup](../../reference/client-applications/pg_basebackup.md) 方法需要更多的步驟，但是相對簡單。依次執行這些步驟，並在繼續進行下一步之前驗證步驟的成功是非常重要的。

可以以非排他性\(Non-Exclusive\)或排他性\(Exclusive\)方式進行低階的基礎備份。建議使用非排他性方法，不建議使用排他性方法，此方式將來會被捨棄。

### **25.3.3.1.** 進行非排他性\(Non-Exclusive\)的低階備份

非排他性的低階備份是一種允許其他同時備份也正在運行的備份方式（使用相同備份 API 啟動的備份和使用 [pg\_basebackup](../../reference/client-applications/pg_basebackup.md) 啟動的備份）。

1. 確保已啟用 WAL 封存選項並且是在正常的狀態。
2. 以具有運行 pg\_start\_backup 的權限的使用者（超級使用者，或者是已經被授權執行此函數的使用者）身份連線到伺服器（無論哪個資料庫），並執行以下指令：

   ```text
   SELECT pg_start_backup('label', false, false);
   ```

   其中 label 是您要用來唯一識別此備份操作的任何字串。必須維持呼叫 pg\_start\_backup 的連線，直到備份結束，否則備份將會自動中止。

   預設情況下，pg\_start\_backup 可能需要很長時間才能完成。這是因為它會執行一個檢查點\(checkpoint\)，並且該檢查點所需的 I/O 將進行相當長的一段時間，一般情況下是檢查點時間間隔的一半（請參閱配置參數 [checkpoint\_completion\_target](../server-configuration/write-ahead-log.md#19-5-2-checkpoints)）。通常這就是您想要的，因為它最大程度地減少了對查詢處理的影響。如果要儘快開始備份，請將第二個參數更改為 true，這將使用儘可能多的 I/O 發出立即檢查點。 第三個參數為 false 告訴 pg\_start\_backup 啟動非排他性的基礎備份。

3. Perform the backup, using any convenient file-system-backup tool such as tar or cpio \(not pg\_dump or pg\_dumpall\). It is neither necessary nor desirable to stop normal operation of the database while you do this. See [Section 25.3.3.3](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) for things to consider during this backup.
4. In the same connection as before, issue the command:

   ```text
   SELECT * FROM pg_stop_backup(false, true);
   ```

   This terminates backup mode. On a primary, it also performs an automatic switch to the next WAL segment. On a standby, it is not possible to automatically switch WAL segments, so you may wish to run `pg_switch_wal` on the primary to perform a manual switch. The reason for the switch is to arrange for the last WAL segment file written during the backup interval to be ready to archive.

   The `pg_stop_backup` will return one row with three values. The second of these fields should be written to a file named `backup_label` in the root directory of the backup. The third field should be written to a file named `tablespace_map` unless the field is empty. These files are vital to the backup working, and must be written without modification.

5. Once the WAL segment files active during the backup are archived, you are done. The file identified by `pg_stop_backup`'s first return value is the last segment that is required to form a complete set of backup files. On a primary, if `archive_mode` is enabled and the `wait_for_archive` parameter is `true`, `pg_stop_backup` does not return until the last segment has been archived. On a standby, `archive_mode` must be `always` in order for `pg_stop_backup` to wait. Archiving of these files happens automatically since you have already configured `archive_command`. In most cases this happens quickly, but you are advised to monitor your archive system to ensure there are no delays. If the archive process has fallen behind because of failures of the archive command, it will keep retrying until the archive succeeds and the backup is complete. If you wish to place a time limit on the execution of `pg_stop_backup`, set an appropriate `statement_timeout` value, but make note that if `pg_stop_backup` terminates because of this your backup may not be valid.

   If the backup process monitors and ensures that all WAL segment files required for the backup are successfully archived then the `wait_for_archive` parameter \(which defaults to true\) can be set to false to have `pg_stop_backup` return as soon as the stop backup record is written to the WAL. By default, `pg_stop_backup` will wait until all WAL has been archived, which can take some time. This option must be used with caution: if WAL archiving is not monitored correctly then the backup might not include all of the WAL files and will therefore be incomplete and not able to be restored.

### **25.3.3.2. Making An Exclusive Low-Level Backup**

{% hint style="info" %}
排他性的備份方法已經過時，應該避免使用。在 PostgreSQL 9.6 之前，這是唯一可用的低階方法，但是現在建議所有使用者升級其腳本以使用非排他性的備份。
{% endhint %}

排他性備份的流程與非排他性備份的流程基本相同，但是在幾個關鍵步驟上有所不同。這種類型的備份只能在主要資料庫上進行，不允許同時進行其他備份。此外，由於如下所述建立了備份標籤檔案，因此它可以阻止當機後主伺服器的自動重啟。另一方面，從備份或備用資料庫中刪除此檔案是一個常見的人為錯誤，它可能導致嚴重的資料損壞。如果必須使用此方法，則可以使用以下步驟。

1. Ensure that WAL archiving is enabled and working.
2. Connect to the server \(it does not matter which database\) as a user with rights to run pg\_start\_backup \(superuser, or a user who has been granted EXECUTE on the function\) and issue the command:

   ```text
   SELECT pg_start_backup('label');
   ```

   where `label` is any string you want to use to uniquely identify this backup operation. `pg_start_backup` creates a _backup label_ file, called `backup_label`, in the cluster directory with information about your backup, including the start time and label string. The function also creates a _tablespace map_ file, called `tablespace_map`, in the cluster directory with information about tablespace symbolic links in `pg_tblspc/` if one or more such link is present. Both files are critical to the integrity of the backup, should you need to restore from it.

   By default, `pg_start_backup` can take a long time to finish. This is because it performs a checkpoint, and the I/O required for the checkpoint will be spread out over a significant period of time, by default half your inter-checkpoint interval \(see the configuration parameter [checkpoint\_completion\_target](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET)\). This is usually what you want, because it minimizes the impact on query processing. If you want to start the backup as soon as possible, use:

   ```text
   SELECT pg_start_backup('label', true);
   ```

   This forces the checkpoint to be done as quickly as possible.

3. Perform the backup, using any convenient file-system-backup tool such as tar or cpio \(not pg\_dump or pg\_dumpall\). It is neither necessary nor desirable to stop normal operation of the database while you do this. See [Section 25.3.3.3](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) for things to consider during this backup.

   As noted above, if the server crashes during the backup it may not be possible to restart until the `backup_label` file has been manually deleted from the `PGDATA` directory. Note that it is very important to never remove the `backup_label` file when restoring a backup, because this will result in corruption. Confusion about when it is appropriate to remove this file is a common cause of data corruption when using this method; be very certain that you remove the file only on an existing master and never when building a standby or restoring a backup, even if you are building a standby that will subsequently be promoted to a new master.

4. Again connect to the database as a user with rights to run pg\_stop\_backup \(superuser, or a user who has been granted EXECUTE on the function\), and issue the command:

   ```text
   SELECT pg_stop_backup();
   ```

   This function terminates backup mode and performs an automatic switch to the next WAL segment. The reason for the switch is to arrange for the last WAL segment written during the backup interval to be ready to archive.

5. Once the WAL segment files active during the backup are archived, you are done. The file identified by `pg_stop_backup`'s result is the last segment that is required to form a complete set of backup files. If `archive_mode` is enabled, `pg_stop_backup` does not return until the last segment has been archived. Archiving of these files happens automatically since you have already configured `archive_command`. In most cases this happens quickly, but you are advised to monitor your archive system to ensure there are no delays. If the archive process has fallen behind because of failures of the archive command, it will keep retrying until the archive succeeds and the backup is complete.

   When using exclusive backup mode, it is absolutely imperative to ensure that `pg_stop_backup` completes successfully at the end of the backup. Even if the backup itself fails, for example due to lack of disk space, failure to call `pg_stop_backup` will leave the server in backup mode indefinitely, causing future backups to fail and increasing the risk of a restart failure during the time that `backup_label` exists.

### **25.3.3.3. Backing Up The Data Directory**

Some file system backup tools emit warnings or errors if the files they are trying to copy change while the copy proceeds. When taking a base backup of an active database, this situation is normal and not an error. However, you need to ensure that you can distinguish complaints of this sort from real errors. For example, some versions of rsync return a separate exit code for “vanished source files”, and you can write a driver script to accept this exit code as a non-error case. Also, some versions of GNU tar return an error code indistinguishable from a fatal error if a file was truncated while tar was copying it. Fortunately, GNU tar versions 1.16 and later exit with 1 if a file was changed during the backup, and 2 for other errors. With GNU tar version 1.23 and later, you can use the warning options `--warning=no-file-changed --warning=no-file-removed` to hide the related warning messages.

Be certain that your backup includes all of the files under the database cluster directory \(e.g., `/usr/local/pgsql/data`\). If you are using tablespaces that do not reside underneath this directory, be careful to include them as well \(and be sure that your backup archives symbolic links as links, otherwise the restore will corrupt your tablespaces\).

You should, however, omit from the backup the files within the cluster's `pg_wal/` subdirectory. This slight adjustment is worthwhile because it reduces the risk of mistakes when restoring. This is easy to arrange if `pg_wal/` is a symbolic link pointing to someplace outside the cluster directory, which is a common setup anyway for performance reasons. You might also want to exclude `postmaster.pid` and `postmaster.opts`, which record information about the running postmaster, not about the postmaster which will eventually use this backup. \(These files can confuse pg\_ctl.\)

It is often a good idea to also omit from the backup the files within the cluster's `pg_replslot/` directory, so that replication slots that exist on the master do not become part of the backup. Otherwise, the subsequent use of the backup to create a standby may result in indefinite retention of WAL files on the standby, and possibly bloat on the master if hot standby feedback is enabled, because the clients that are using those replication slots will still be connecting to and updating the slots on the master, not the standby. Even if the backup is only intended for use in creating a new master, copying the replication slots isn't expected to be particularly useful, since the contents of those slots will likely be badly out of date by the time the new master comes on line.

The contents of the directories `pg_dynshmem/`, `pg_notify/`, `pg_serial/`, `pg_snapshots/`, `pg_stat_tmp/`, and `pg_subtrans/` \(but not the directories themselves\) can be omitted from the backup as they will be initialized on postmaster startup. If [stats\_temp\_directory](https://www.postgresql.org/docs/12/runtime-config-statistics.html#GUC-STATS-TEMP-DIRECTORY) is set and is under the data directory then the contents of that directory can also be omitted.

Any file or directory beginning with `pgsql_tmp` can be omitted from the backup. These files are removed on postmaster start and the directories will be recreated as needed.

`pg_internal.init` files can be omitted from the backup whenever a file of that name is found. These files contain relation cache data that is always rebuilt when recovering.

The backup label file includes the label string you gave to `pg_start_backup`, as well as the time at which `pg_start_backup` was run, and the name of the starting WAL file. In case of confusion it is therefore possible to look inside a backup file and determine exactly which backup session the dump file came from. The tablespace map file includes the symbolic link names as they exist in the directory `pg_tblspc/` and the full path of each symbolic link. These files are not merely for your information; their presence and contents are critical to the proper operation of the system's recovery process.

It is also possible to make a backup while the server is stopped. In this case, you obviously cannot use `pg_start_backup` or `pg_stop_backup`, and you will therefore be left to your own devices to keep track of which backup is which and how far back the associated WAL files go. It is generally better to follow the continuous archiving procedure above.

## 25.3.4. Recovering Using a Continuous Archive Backup

好的，剛好最糟糕的事情發生了，這時候您需要使用備份來還原資料庫。步驟如下：

1. 停止伺服器（如果正在執行的話）。
2. 如果有足夠的空間，請將整個叢集資料目錄和所有資料表空間複製到一個暫存的路徑，以備之需。請注意，此預防措施需要你的系統上有足夠的可用空間來容納現有資料庫的兩個副本。如果沒有足夠的空間，則至少應保存叢集的 pg\_wal 子目錄的內容，因為它可能包含在系統關閉之前尚未歸檔封存的交易日誌。
3. 刪除叢集資料目錄下以及正在使用的所有資料表空間目錄下的所有現有檔案和子目錄。
4. 從檔案系統備份中還原資料庫檔案。確保已授予正確的擁有者（資料庫系統使用者，而不是 root！）和正確的權限還原它們。如果有使用額外的資料表空間，則應驗證 pg\_tblspc/ 中的符號連結是否也已正確還原。
5. 刪除 pg\_wal/ 中的所有檔案；這些來自檔案系統的備份，因此可能已過時而不是最新。如果您根本沒有備份 pg\_wal/，那麼請以適當的權限重新建立它，請小心確保如果您之前已進行過額外配置，則應將其重新建立為符號連結。
6. 如果您具有在步驟 2 中所保存的未封存 WAL 檔案，請將其複製到 pg\_wal/ 之中。（最好複製它們，而不是移動它們，因為如果出現問題而必須重新開始的話，您仍然擁有未修改的檔案。）
7. 在 postgresql.conf 中進行還原設定（請參閱[第 19.5.4 節](../server-configuration/write-ahead-log.md#19-5-4-archive-recovery)），並在叢集資料目錄中建立檔案 recovery.signal。您可能還需要臨時修改 pg\_hba.conf，以防止一般使用者連線進來，直到您確定還原成功為止。
8. 啟動伺服器。伺服器將進入還原模式，並繼續讀取所需的 WAL 檔案。如果還原由於外部錯誤而終止，則只需重啟伺服器即可繼續還原。還原過程完成後，伺服器將刪除 recovery.signal（以防止以後意外重新進入還原模式），然後開始正常的資料庫操作。
9. 檢查資料庫的內容，以確保您已經還原到所需要的狀態。如果沒有，請回到步驟 1。如果一切正常，請透過將 pg\_hba.conf 恢復為正常狀態來允許您的使用者進行連線。

所有這一切的關鍵部分是建立還原設定，該設定描述了您要如何還原以及還原應進行多長的時間。你絕對必須指定的一件事是 restore\_command，它告訴 PostgreSQL 如何檢索已封存的 WAL 檔案。像 archive\_command 一樣，這是一個 shell 指令字串。它可以包含 %f（依所需的日誌檔案的名稱代換）和 %p（將日誌檔案複製到的路徑名）代換。（路徑名是相對於目前的工作目錄（即叢集的資料目錄）的。）如果需要在指令中使用實際的 % 字元，請寫入 %%。最簡單的指令是：

```text
restore_command = 'cp /mnt/server/archivedir/%f %p'
```

which will copy previously archived WAL segments from the directory `/mnt/server/archivedir`. Of course, you can use something much more complicated, perhaps even a shell script that requests the operator to mount an appropriate tape.

It is important that the command return nonzero exit status on failure. The command _will_ be called requesting files that are not present in the archive; it must return nonzero when so asked. This is not an error condition. An exception is that if the command was terminated by a signal \(other than SIGTERM, which is used as part of a database server shutdown\) or an error by the shell \(such as command not found\), then recovery will abort and the server will not start up.

Not all of the requested files will be WAL segment files; you should also expect requests for files with a suffix of `.history`. Also be aware that the base name of the `%p` path will be different from `%f`; do not expect them to be interchangeable.

WAL segments that cannot be found in the archive will be sought in `pg_wal/`; this allows use of recent un-archived segments. However, segments that are available from the archive will be used in preference to files in `pg_wal/`.

Normally, recovery will proceed through all available WAL segments, thereby restoring the database to the current point in time \(or as close as possible given the available WAL segments\). Therefore, a normal recovery will end with a “file not found” message, the exact text of the error message depending upon your choice of `restore_command`. You may also see an error message at the start of recovery for a file named something like `00000001.history`. This is also normal and does not indicate a problem in simple recovery situations; see [Section 25.3.5](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-TIMELINES) for discussion.

If you want to recover to some previous point in time \(say, right before the junior DBA dropped your main transaction table\), just specify the required [stopping point](https://www.postgresql.org/docs/12/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET). You can specify the stop point, known as the “recovery target”, either by date/time, named restore point or by completion of a specific transaction ID. As of this writing only the date/time and named restore point options are very usable, since there are no tools to help you identify with any accuracy which transaction ID to use.

#### Note

The stop point must be after the ending time of the base backup, i.e., the end time of `pg_stop_backup`. You cannot use a base backup to recover to a time when that backup was in progress. \(To recover to such a time, you must go back to your previous base backup and roll forward from there.\)

If recovery finds corrupted WAL data, recovery will halt at that point and the server will not start. In such a case the recovery process could be re-run from the beginning, specifying a “recovery target” before the point of corruption so that recovery can complete normally. If recovery fails for an external reason, such as a system crash or if the WAL archive has become inaccessible, then the recovery can simply be restarted and it will restart almost from where it failed. Recovery restart works much like checkpointing in normal operation: the server periodically forces all its state to disk, and then updates the `pg_control` file to indicate that the already-processed WAL data need not be scanned again.

## 25.3.5. Timelines

將資料庫還原到先前時間點的能力會有一些複雜，類似於有關時間旅行和平行宇宙的科幻小說故事。例如，在資料庫的原始歷史記錄中，假設您在星期二晚上 5:15 PM 刪除了一個關鍵的資料表，但是直到星期三中午才意識到自己的錯誤。不用擔心，您可以取出備份，恢復到星期二晚上 5:14 的時間點，並開始運行。在資料庫宇宙的歷史記錄中，其實您從未刪除過資料表。但是，假設您後來又意識到這不是一個好主意，並且想回到原始歷史中的星期三上午。在資料庫執行期間，如果您覆蓋了一些 WAL 檔案，而這些檔案會造成你無法再回到你希望回到原來的時空。因此，為避免這種情況，您需要將時間點恢復後產生的一系列 WAL 記錄與原始資料庫歷史記錄中產生的 WAL 記錄檔案區分開來。

To deal with this problem, PostgreSQL has a notion of _timelines_. Whenever an archive recovery completes, a new timeline is created to identify the series of WAL records generated after that recovery. The timeline ID number is part of WAL segment file names so a new timeline does not overwrite the WAL data generated by previous timelines. It is in fact possible to archive many different timelines. While that might seem like a useless feature, it's often a lifesaver. Consider the situation where you aren't quite sure what point-in-time to recover to, and so have to do several point-in-time recoveries by trial and error until you find the best place to branch off from the old history. Without timelines this process would soon generate an unmanageable mess. With timelines, you can recover to _any_ prior state, including states in timeline branches that you abandoned earlier.

Every time a new timeline is created, PostgreSQL creates a “timeline history” file that shows which timeline it branched off from and when. These history files are necessary to allow the system to pick the right WAL segment files when recovering from an archive that contains multiple timelines. Therefore, they are archived into the WAL archive area just like WAL segment files. The history files are just small text files, so it's cheap and appropriate to keep them around indefinitely \(unlike the segment files which are large\). You can, if you like, add comments to a history file to record your own notes about how and why this particular timeline was created. Such comments will be especially valuable when you have a thicket of different timelines as a result of experimentation.

The default behavior of recovery is to recover along the same timeline that was current when the base backup was taken. If you wish to recover into some child timeline \(that is, you want to return to some state that was itself generated after a recovery attempt\), you need to specify the target timeline ID in [recovery\_target\_timeline](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-TIMELINE). You cannot recover into timelines that branched off earlier than the base backup.

## 25.3.6. Tips and Examples

Some tips for configuring continuous archiving are given here.

### **25.3.6.1. Standalone Hot Backups**

It is possible to use PostgreSQL's backup facilities to produce standalone hot backups. These are backups that cannot be used for point-in-time recovery, yet are typically much faster to backup and restore than pg\_dump dumps. \(They are also much larger than pg\_dump dumps, so in some cases the speed advantage might be negated.\)

As with base backups, the easiest way to produce a standalone hot backup is to use the [pg\_basebackup](https://www.postgresql.org/docs/12/app-pgbasebackup.html) tool. If you include the `-X` parameter when calling it, all the write-ahead log required to use the backup will be included in the backup automatically, and no special action is required to restore the backup.

If more flexibility in copying the backup files is needed, a lower level process can be used for standalone hot backups as well. To prepare for low level standalone hot backups, make sure `wal_level` is set to `replica` or higher, `archive_mode` to `on`, and set up an `archive_command` that performs archiving only when a _switch file_ exists. For example:

```text
archive_command = 'test ! -f /var/lib/pgsql/backup_in_progress || (test ! -f /var/lib/pgsql/archive/%f && cp %p /var/lib/pgsql/archive/%f)'
```

This command will perform archiving when `/var/lib/pgsql/backup_in_progress` exists, and otherwise silently return zero exit status \(allowing PostgreSQL to recycle the unwanted WAL file\).

With this preparation, a backup can be taken using a script like the following:

```text
touch /var/lib/pgsql/backup_in_progress
psql -c "select pg_start_backup('hot_backup');"
tar -cf /var/lib/pgsql/backup.tar /var/lib/pgsql/data/
psql -c "select pg_stop_backup();"
rm /var/lib/pgsql/backup_in_progress
tar -rf /var/lib/pgsql/backup.tar /var/lib/pgsql/archive/
```

The switch file `/var/lib/pgsql/backup_in_progress` is created first, enabling archiving of completed WAL files to occur. After the backup the switch file is removed. Archived WAL files are then added to the backup so that both base backup and all required WAL files are part of the same tar file. Please remember to add error handling to your backup scripts.

### **25.3.6.2. Compressed Archive Logs**

如果需要考慮封存檔案的儲存空間，則可以使用 gzip 壓縮這些檔案：

```text
archive_command = 'gzip < %p > /var/lib/pgsql/archive/%f'
```

然後，您將需要在還原過程中使用 gunzip：

```text
restore_command = 'gunzip < /mnt/server/archivedir/%f > %p'
```

### **25.3.6.3. Archive\_command Scripts**

Many people choose to use scripts to define their `archive_command`, so that their `postgresql.conf` entry looks very simple:

```text
archive_command = 'local_backup_script.sh "%p" "%f"'
```

Using a separate script file is advisable any time you want to use more than a single command in the archiving process. This allows all complexity to be managed within the script, which can be written in a popular scripting language such as bash or perl.

Examples of requirements that might be solved within a script include:

* Copying data to secure off-site data storage
* Batching WAL files so that they are transferred every three hours, rather than one at a time
* Interfacing with other backup and recovery software
* Interfacing with monitoring software to report errors

{% hint style="info" %}
使用 archive\_command 腳本時，最好啟用 [logging\_collector](../server-configuration/error-reporting-and-logging.md#logging_collector-boolean)。這樣的話，從腳本寫入 stderr 的所有訊息都會出現在資料庫伺服器記錄檔之中，從而使複雜的設定在異常時易於除錯。
{% endhint %}

## 25.3.7. Caveats

截至目前為止，連續歸檔技術\(PITR\)仍然存在著一些侷限性。這些可能會在未來的版本中改善：

* 如果在執行基礎備份時執行了 [CREATE DATABASE](../../reference/sql-commands/create-database.md) 命令，然後在仍在進行基礎備份的同時修改了 CREATE DATABASE 所複製的樣版資料庫，則還原的時候很可能會使這些修改連帶影響到其所建立的資料庫之中。 這當然不是希望發生的事。為了避免這種風險，最好在進行基礎1備份的同時不要修改任何樣版資料庫。
* [CREATE TABLESPACE](../../reference/sql-commands/create-tablespace.md) 指令使用絕對路徑進行存放 WAL 記錄，因此重放交易時，將會以相同絕對路徑的資料表空間進行重放。如果正在其他主機上重放交易日誌，則這可能不是希望的的結果。即使在同一台主機上重放交易日誌，但是將日誌重放到新的資料目錄中，也可能很危險：重放仍將覆蓋原始資料表空間的內容。為了避免這種潛在的麻煩，最佳實作是在建立或刪除資料表空間之後進行新的基礎備份。

你還需要注意的是，一般而言 WAL 格式相當龐大，因為它包含許多磁碟頁面快照。這些頁面快照旨在支援災難復原，因為我們可能需要修復部分寫入的磁碟頁面。根據系統硬體和軟體環境的不同，部分寫入的風險可能很小，可以忽略，在這種情況下，您可以透過使用 [full\_page\_writes](../server-configuration/write-ahead-log.md#full_page_writes-boolean) 參數關閉頁面快照來顯著減少已歸檔日誌的總量。（在執行此操作之前，請先閱讀[第 29 章](../reliability-and-the-write-ahead-log/)中的說明和警告。）關閉頁面快照並不會阻礙將日誌用於 PITR 操作。未來的發展方向1是即使在啟用 full\_page\_writes 的情況下，也可以透過刪除不必要的頁面副本來壓縮已歸檔封存的 WAL 資料。同時，管理者可能希望透過儘可能增加檢查點\(checkpoint\)間隔參數來減少 WAL 中包含的頁面快照的數量。

