# F.38.2. 函式

<a id="POSTGRES-FDW-FUNCTIONS"></a>

## F.38.2. 函式 [#](#postgres-fdw-functions) <a href="#postgres-fdw-functions" id="postgres-fdw-functions"></a>

`postgres_fdw_get_connections( IN check_conn boolean DEFAULT false, OUT server_name text, OUT user_name text, OUT valid boolean, OUT used_in_xact boolean, OUT closed boolean, OUT remote_backend_pid int4) returns setof record`

此函式傳回 postgres_fdw 從本機工作階段與外部伺服器建立的所有開啟中連線的資訊。若沒有開啟中的連線，則不傳回任何紀錄。

若 `check_conn` 設為 `true`，
此函式會檢查每個連線的狀態，並將結果顯示在 `closed` 欄位中。
此功能目前只在支援
`poll` 系統呼叫之非標準 `POLLRDHUP` 擴充的系統（包括 Linux）上可用。
這對於檢查交易中使用的所有連線是否仍然開啟很有用。若有任何連線已關閉，交易就無法成功提交，
因此最好在偵測到已關閉的連線時就立即回復，而不是繼續執行到最後。若此函式回報有連線的
`used_in_xact` 與 `closed` 都是
`true`，使用者可以立即回復交易。

此函式的使用範例：

```

    postgres=# SELECT * FROM postgres_fdw_get_connections(true);
     server_name | user_name | valid | used_in_xact | closed | remote_backend_pid
    -------------+-----------+-------+--------------+-----------------------------
     loopback1   | postgres  | t     | t            | f      |            1353340
     loopback2   | public    | t     | t            | f      |            1353120
     loopback3   |           | f     | t            | f      |            1353156
```

輸出欄位說明列於
[表 F.28](#postgres-fdw-get-connections-columns)。

<a id="POSTGRES-FDW-GET-CONNECTIONS-COLUMNS"></a>

### 表 F.28. `postgres_fdw_get_connections` 輸出欄位 [#](#postgres-fdw-get-connections-columns) <a href="#postgres-fdw-get-connections-columns" id="postgres-fdw-get-connections-columns"></a>

<table border="1" class="table" summary="postgres_fdw_get_connections 輸出欄位"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">server_name</code></td><td><code class="type">text</code></td><td>
             此連線的外部伺服器名稱。若伺服器已被刪除但連線仍保持開啟（亦即被標記為無效），此值將為 <code class="literal">NULL</code>。
            </td></tr><tr><td><code class="structfield">user_name</code></td><td><code class="type">text</code></td><td>
             對應到此連線之外部伺服器的本機使用者名稱；若使用的是 public 對應，則為 <code class="literal">public</code>。
             若使用者對應已被刪除但連線仍保持開啟（亦即被標記為無效），此值將為 <code class="literal">NULL</code>。
            </td></tr><tr><td><code class="structfield">valid</code></td><td><code class="type">boolean</code></td><td>
             若此連線無效則為 false；無效表示此連線在目前交易中被使用，但其外部伺服器或使用者對應已被變更或刪除。
             無效的連線會在交易結束時關閉。否則傳回 true。
            </td></tr><tr><td><code class="structfield">used_in_xact</code></td><td><code class="type">boolean</code></td><td>
             若此連線在目前交易中被使用則為 true。
            </td></tr><tr><td><code class="structfield">closed</code></td><td><code class="type">boolean</code></td><td>
             若此連線已關閉則為 true，否則為 false。
             <code class="literal">NULL</code> 會在 <code class="literal">check_conn</code>
             設為 <code class="literal">false</code>，或此平台上無法使用連線狀態檢查時傳回。
            </td></tr><tr><td><code class="structfield">remote_backend_pid</code></td><td><code class="type">int4</code></td><td>
             外部伺服器上處理此連線之遠端後端的程序 ID。若遠端後端已終止且連線已關閉（<code class="literal">closed</code> 設為
             <code class="literal">true</code>），此欄位仍會顯示已終止後端的程序 ID。
            </td></tr></tbody></table>

<br>

`postgres_fdw_disconnect(server_name text) returns boolean`

此函式會捨棄
`postgres_fdw` 從本機工作階段與指定名稱之外部伺服器建立的開啟中連線。請注意，使用不同的使用者對應，可能會有多個連到指定伺服器的連線。
若這些連線在目前的本機交易中被使用，則不會中斷它們，並會回報警告訊息。
若此函式中斷了至少一個連線，則傳回 `true`，否則傳回 `false`。
若找不到指定名稱的外部伺服器，則會回報錯誤。
此函式的使用範例：

```

    postgres=# SELECT postgres_fdw_disconnect('loopback1');
     postgres_fdw_disconnect
    -------------------------
     t
```

`postgres_fdw_disconnect_all() returns boolean`

此函式會捨棄
`postgres_fdw` 從本機工作階段與外部伺服器建立的所有開啟中連線。若這些連線在目前的本機交易中被使用，則不會中斷它們，並會回報警告訊息。
若此函式中斷了至少一個連線，則傳回 `true`，否則傳回 `false`。
此函式的使用範例：

```

    postgres=# SELECT postgres_fdw_disconnect_all();
     postgres_fdw_disconnect_all
    -----------------------------
     t
```

[返回 F.38. postgres_fdw — 存取儲存在外部 PostgreSQL 伺服器中的資料](../postgres-fdw.md#postgres-fdw)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/postgres-fdw.html)（原文版本：18.6；核對日期：2026-10-22）
