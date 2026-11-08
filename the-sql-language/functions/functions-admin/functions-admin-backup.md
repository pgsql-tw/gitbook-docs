# 9.28.3. 備份控制函式

<a id="FUNCTIONS-ADMIN-BACKUP"></a>

## 9.28.3. 備份控制函式 [#](#functions-admin-backup) <a href="#functions-admin-backup" id="functions-admin-backup"></a>

<a id="id-1.5.8.34.5.2"></a>

[表 9.97](#functions-admin-backup-table) 所列的函式可協助進行線上備份。這些函式不能在復原期間執行（`pg_backup_start`、`pg_backup_stop` 與 `pg_wal_lsn_diff` 除外）。

關於這些函式的正確用法，詳情請參閱[第 25.3 節](../../../server-administration/backup/continuous-archiving.md)。

<a id="FUNCTIONS-ADMIN-BACKUP-TABLE"></a>

### 表 9.97. 備份控制函式 [#](#functions-admin-backup-table) <a href="#functions-admin-backup-table" id="functions-admin-backup-table"></a>

<table border="1" class="table" summary="Backup Control Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.1.1.1.1"></a>
<code class="function">pg_create_restore_point</code> ( <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        在預寫式日誌中建立一個具名的標記紀錄，之後可以用來作為復原目標，並回傳對應的預寫式日誌位置。接著可以將所給的名稱與 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-wal.md#GUC-RECOVERY-TARGET-NAME">recovery_target_name</a> 搭配使用，以指定復原要進行到哪一個時間點。請避免建立多個名稱相同的還原點，因為復原會在第一個名稱符合復原目標的還原點停止。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.2.1.1.1"></a>
<code class="function">pg_current_wal_flush_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的排清位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.3.1.1.1"></a>
<code class="function">pg_current_wal_insert_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的插入位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.4.1.1.1"></a>
<code class="function">pg_current_wal_lsn</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        回傳目前預寫式日誌的寫入位置（請參閱下方說明）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.5.1.1.1"></a>
<code class="function">pg_backup_start</code> (
          <em class="parameter"><code>label</code></em> <code class="type">text</code>
          [<span class="optional">, <em class="parameter"><code>fast</code></em> <code class="type">boolean</code>
</span>] )
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        讓伺服器準備開始進行線上備份。唯一必要的參數是使用者自訂的任意備份標籤。（通常這會是備份傾印檔案存放時所用的名稱。）如果選用的第二個參數指定為 <code class="literal">true</code>，就表示要盡快執行 <code class="function">pg_backup_start</code>。這會強制立即進行檢查點，因而造成 I/O 操作的尖峰，拖慢任何同時執行中的查詢。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.6.1.1.1"></a>
<code class="function">pg_backup_stop</code> (
          [<span class="optional"><em class="parameter"><code>wait_for_archive</code></em> <code class="type">boolean</code>
</span>] )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>labelfile</code></em> <code class="type">text</code>,
        <em class="parameter"><code>spcmapfile</code></em> <code class="type">text</code> )
       </p>
<p>
        完成線上備份的執行。備份標籤檔案與資料表空間對應檔案應有的內容，會作為函式結果的一部分回傳，且必須寫入備份區域中的檔案。這些檔案不可寫入運作中的資料目錄（這樣做會導致 PostgreSQL 在當機時無法重新啟動）。
       </p>
<p>
        有一個 <code class="type">boolean</code> 型別的選用參數。如果為 false，函式會在備份完成後立即回傳，而不等待 WAL 封存。這種行為只有在搭配會獨立監控 WAL 封存的備份軟體時才有用。否則，讓備份保持一致所需的 WAL 可能會遺失，使得備份毫無用處。在預設情況下或此參數為 true 時，如果已啟用封存，<code class="function">pg_backup_stop</code> 會等待 WAL 封存完成。（在備用伺服器上，這表示只有在 <code class="varname">archive_mode</code> = <code class="literal">always</code> 時才會等待。如果主要伺服器上的寫入活動很少，在主要伺服器上執行 <code class="function">pg_switch_wal</code> 以觸發立即的區段切換可能會有幫助。）
       </p>
<p>
        在主要伺服器上執行時，這個函式還會在預寫式日誌封存區域中建立一個備份歷程檔案。歷程檔案包含傳給 <code class="function">pg_backup_start</code> 的標籤、備份的起始與結束預寫式日誌位置，以及備份的起始與結束時間。在記錄結束位置之後，目前的預寫式日誌插入點會自動推進到下一個預寫式日誌檔案，讓結束的預寫式日誌檔案可以立即封存，以完成備份。
       </p>
<p>
        這個函式的結果是單一筆紀錄。<em class="parameter"><code>lsn</code></em> 欄位存放備份的結束預寫式日誌位置（同樣可以忽略）。第二個欄位回傳備份標籤檔案的內容，第三個欄位則回傳資料表空間對應檔案的內容。這些內容必須作為備份的一部分儲存，並且是還原程序中所必需的。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.7.1.1.1"></a>
<code class="function">pg_switch_wal</code> ()
        → <code class="returnvalue">pg_lsn</code>
</p>
<p>
        強制伺服器切換到新的預寫式日誌檔案，讓目前的檔案可以被封存（假設你正在使用連續封存）。結果是剛完成的預寫式日誌檔案中的結束預寫式日誌位置加 1。如果自上次預寫式日誌切換以來沒有任何預寫式日誌活動，<code class="function">pg_switch_wal</code> 不會做任何事，並回傳目前使用中之預寫式日誌檔案的起始位置。
       </p>
<p>
        這個函式預設只限超級使用者使用，但可以將 EXECUTE 權限授予其他使用者來執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.8.1.1.1"></a>
<code class="function">pg_walfile_name</code> ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將預寫式日誌位置轉換為存放該位置的 WAL 檔案名稱。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.9.1.1.1"></a>
<code class="function">pg_walfile_name_offset</code> ( <em class="parameter"><code>lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>file_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>file_offset</code></em> <code class="type">integer</code> )
       </p>
<p>
        將預寫式日誌位置轉換為 WAL 檔案名稱，以及在該檔案內的位元組偏移量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.10.1.1.1"></a>
<code class="function">pg_split_walfile_name</code> ( <em class="parameter"><code>file_name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>segment_number</code></em> <code class="type">numeric</code>,
        <em class="parameter"><code>timeline_id</code></em> <code class="type">bigint</code> )
       </p>
<p>
        從 WAL 檔案名稱中取出序號與時間軸 ID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.5.5.2.2.11.1.1.1"></a>
<code class="function">pg_wal_lsn_diff</code> ( <em class="parameter"><code>lsn1</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>lsn2</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        計算兩個預寫式日誌位置之間以位元組為單位的差值（<em class="parameter"><code>lsn1</code></em> - <em class="parameter"><code>lsn2</code></em>）。這可以與 <code class="structname">pg_stat_replication</code> 或<a class="xref" href="#functions-admin-backup-table">表 9.97</a> 中所列的部分函式搭配使用，以取得複寫延遲。
       </p></td></tr></tbody></table>

<br>

`pg_current_wal_lsn` 會以上述函式所使用的相同格式，顯示目前預寫式日誌（write-ahead log）的寫入位置。同樣地，`pg_current_wal_insert_lsn` 會顯示目前預寫式日誌的插入位置，而 `pg_current_wal_flush_lsn` 則顯示目前預寫式日誌的排清（flush）位置。插入位置是任一時刻預寫式日誌的「邏輯」結尾，而寫入位置是實際已從伺服器內部緩衝區寫出之內容的結尾，排清位置則是已知已寫入持久性儲存裝置的最後位置。寫入位置是從伺服器外部所能檢視之內容的結尾；如果你想要封存僅部分完成的預寫式日誌檔案，通常需要的就是這個位置。插入位置與排清位置主要是提供給伺服器除錯之用。這些都是唯讀操作，不需要超級使用者權限。

你可以使用 `pg_walfile_name_offset`，從 `pg_lsn` 值中取出對應的預寫式日誌檔名與位元組偏移量。例如：

```

postgres=# SELECT * FROM pg_walfile_name_offset((pg_backup_stop()).lsn);
        file_name         | file_offset
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

同樣地，`pg_walfile_name` 只會取出預寫式日誌的檔名。

`pg_split_walfile_name` 可用於從檔案偏移量與 WAL 檔名計算出 LSN，例如：

```

postgres=# \set file_name '000000010000000100C000AB'
postgres=# \set offset 256
postgres=# SELECT '0/0'::pg_lsn + pd.segment_number * ps.setting::int + :offset AS lsn
  FROM pg_split_walfile_name(:'file_name') pd,
       pg_show_all_settings() ps
  WHERE ps.name = 'wal_segment_size';
      lsn
---------------
 C001/AB000100
(1 row)
```

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
