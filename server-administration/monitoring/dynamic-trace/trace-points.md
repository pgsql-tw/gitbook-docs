# 27.5.2. 內建探針

<a id="TRACE-POINTS"></a>

## 27.5.2. 內建探針 [#](#trace-points) <a href="#trace-points" id="trace-points"></a>

原始碼中提供了許多標準探針，
如[表 27.49](#dtrace-probe-point-table)所示；
[表 27.50](#typedefs-table)
則顯示這些探針中所使用的型別。
當然，未來也能加入更多探針，
以增進 PostgreSQL 的可觀察性。

<a id="DTRACE-PROBE-POINT-TABLE"></a>

### 表 27.49. 內建 DTrace 探針 [#](#dtrace-probe-point-table) <a href="#dtrace-probe-point-table" id="dtrace-probe-point-table"></a>

<table border="1" class="table" summary="Built-in DTrace Probes"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>參數</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">transaction-start</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>在新交易開始時觸發的探針。
      arg0 為交易 ID。</td></tr><tr><td><code class="literal">transaction-commit</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>在交易成功完成時觸發的探針。
      arg0 為交易 ID。</td></tr><tr><td><code class="literal">transaction-abort</code></td><td><code class="literal">(LocalTransactionId)</code></td><td>在交易未成功完成時觸發的探針。
      arg0 為交易 ID。</td></tr><tr><td><code class="literal">query-start</code></td><td><code class="literal">(const char *)</code></td><td>在查詢開始處理時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-done</code></td><td><code class="literal">(const char *)</code></td><td>在查詢處理完成時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-parse-start</code></td><td><code class="literal">(const char *)</code></td><td>在查詢開始剖析時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-parse-done</code></td><td><code class="literal">(const char *)</code></td><td>在查詢剖析完成時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-rewrite-start</code></td><td><code class="literal">(const char *)</code></td><td>在查詢開始重寫時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-rewrite-done</code></td><td><code class="literal">(const char *)</code></td><td>在查詢重寫完成時觸發的探針。
      arg0 為查詢字串。</td></tr><tr><td><code class="literal">query-plan-start</code></td><td><code class="literal">()</code></td><td>在查詢開始規劃時觸發的探針。</td></tr><tr><td><code class="literal">query-plan-done</code></td><td><code class="literal">()</code></td><td>在查詢規劃完成時觸發的探針。</td></tr><tr><td><code class="literal">query-execute-start</code></td><td><code class="literal">()</code></td><td>在查詢開始執行時觸發的探針。</td></tr><tr><td><code class="literal">query-execute-done</code></td><td><code class="literal">()</code></td><td>在查詢執行完成時觸發的探針。</td></tr><tr><td><code class="literal">statement-status</code></td><td><code class="literal">(const char *)</code></td><td>每當伺服器程序更新其
      <code class="structname">pg_stat_activity</code>.<code class="structfield">status</code>
      時，就會觸發的探針。
      arg0 為新的狀態字串。</td></tr><tr><td><code class="literal">checkpoint-start</code></td><td><code class="literal">(int)</code></td><td>在檢查點開始時觸發的探針。
      arg0 存放用來區分不同檢查點類型（例如關機、立即，
      或強制）的位元旗標。</td></tr><tr><td><code class="literal">checkpoint-done</code></td><td><code class="literal">(int, int, int, int, int)</code></td><td>在檢查點完成時觸發的探針。
      （下方所列的探針，會在檢查點處理過程中依序觸發。）
      arg0 為已寫入的緩衝區數量。arg1 為緩衝區總數。
      arg2、arg3 與 arg4，分別存放已新增、
      移除與回收的 WAL 檔案數量。</td></tr><tr><td><code class="literal">clog-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 CLOG 部分開始時觸發的探針。
      arg0 在一般檢查點時為 true，
      在關機檢查點時為 false。</td></tr><tr><td><code class="literal">clog-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 CLOG 部分完成時觸發的探針。
      arg0 的意義與
      <code class="literal">clog-checkpoint-start</code> 相同。</td></tr><tr><td><code class="literal">subtrans-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 SUBTRANS 部分開始時觸發的探針。
      arg0 在一般檢查點時為 true，
      在關機檢查點時為 false。</td></tr><tr><td><code class="literal">subtrans-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 SUBTRANS 部分完成時觸發的探針。
      arg0 的意義與
      <code class="literal">subtrans-checkpoint-start</code> 相同。</td></tr><tr><td><code class="literal">multixact-checkpoint-start</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 MultiXact 部分開始時觸發的探針。
      arg0 在一般檢查點時為 true，
      在關機檢查點時為 false。</td></tr><tr><td><code class="literal">multixact-checkpoint-done</code></td><td><code class="literal">(bool)</code></td><td>在檢查點中 MultiXact 部分完成時觸發的探針。
      arg0 的意義與
      <code class="literal">multixact-checkpoint-start</code> 相同。</td></tr><tr><td><code class="literal">buffer-checkpoint-start</code></td><td><code class="literal">(int)</code></td><td>在檢查點中緩衝區寫入部分開始時觸發的探針。
      arg0 存放用來區分不同檢查點類型（例如關機、立即，
      或強制）的位元旗標。</td></tr><tr><td><code class="literal">buffer-sync-start</code></td><td><code class="literal">(int, int)</code></td><td>在我們於檢查點期間開始寫入髒緩衝區
      （在判斷出哪些緩衝區必須寫入之後）時觸發的探針。
      arg0 為緩衝區總數。
      arg1 為目前為髒、需要寫入的數量。</td></tr><tr><td><code class="literal">buffer-sync-written</code></td><td><code class="literal">(int)</code></td><td>在檢查點期間，每個緩衝區寫入之後觸發的探針。
      arg0 為該緩衝區的 ID 編號。</td></tr><tr><td><code class="literal">buffer-sync-done</code></td><td><code class="literal">(int, int, int)</code></td><td>在所有髒緩衝區都已寫入完成時觸發的探針。
      arg0 為緩衝區總數。
      arg1 為檢查點程序實際寫入的緩衝區數量。
      arg2 為預期要寫入的數量（即
      <code class="literal">buffer-sync-start</code> 的 arg1）；
      任何差異，都反映出其他程序在檢查點期間
      也刷寫了緩衝區。</td></tr><tr><td><code class="literal">buffer-checkpoint-sync-start</code></td><td><code class="literal">()</code></td><td>在髒緩衝區已寫入核心之後、
      開始發出 fsync 請求之前觸發的探針。</td></tr><tr><td><code class="literal">buffer-checkpoint-done</code></td><td><code class="literal">()</code></td><td>在緩衝區同步至磁碟完成時觸發的探針。</td></tr><tr><td><code class="literal">twophase-checkpoint-start</code></td><td><code class="literal">()</code></td><td>在檢查點中兩階段部分開始時觸發的探針。</td></tr><tr><td><code class="literal">twophase-checkpoint-done</code></td><td><code class="literal">()</code></td><td>在檢查點中兩階段部分完成時觸發的探針。</td></tr><tr><td><code class="literal">buffer-extend-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int)</code></td><td>在關聯延伸開始時觸發的探針。
       arg0 存放要延伸的分支（fork）。arg1、arg2 與 arg3，
       存放用以識別該關聯的資料表空間、資料庫，
       與關聯 OID。arg4
       為建立該本機緩衝區暫存關聯之後端的 ID，
       若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>
       （-1）。arg5 為呼叫者想要延伸的區塊數。</td></tr><tr><td><code class="literal">buffer-extend-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int, BlockNumber)</code></td><td>在關聯延伸完成時觸發的探針。
       arg0 存放要延伸的分支（fork）。arg1、arg2 與 arg3，
       存放用以識別該關聯的資料表空間、資料庫，
       與關聯 OID。arg4
       為建立該本機緩衝區暫存關聯之後端的 ID，
       若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>
       （-1）。arg5 為該關聯實際延伸的區塊數，
       由於資源限制，此值可能小於
       <code class="literal">buffer-extend-start</code> 中的數值。
       arg6 存放第一個新區塊的 BlockNumber。</td></tr><tr><td><code class="literal">buffer-read-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>在緩衝區讀取開始時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。
      </td></tr><tr><td><code class="literal">buffer-read-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, bool)</code></td><td>在緩衝區讀取完成時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。
      arg6 在該緩衝區已存在於緩衝池中時為 true，否則為 false。</td></tr><tr><td><code class="literal">buffer-flush-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid)</code></td><td>在對某個共享緩衝區發出任何寫入請求之前觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。</td></tr><tr><td><code class="literal">buffer-flush-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid)</code></td><td>在某次寫入請求完成時觸發的探針。（請注意，
      這只反映將資料傳遞給核心所花的時間；
      通常此時資料實際上尚未寫入磁碟。）
      其引數與 <code class="literal">buffer-flush-start</code> 相同。</td></tr><tr><td><code class="literal">wal-buffer-write-dirty-start</code></td><td><code class="literal">()</code></td><td>在伺服器程序因為已無可用 WAL 緩衝空間，
      而開始寫入某個髒 WAL 緩衝區時觸發的探針。
      （若此情況經常發生，代表
      <a class="xref" href="../../runtime-config/runtime-config-wal.md#GUC-WAL-BUFFERS">wal_buffers</a>
      設定得太小。）</td></tr><tr><td><code class="literal">wal-buffer-write-dirty-done</code></td><td><code class="literal">()</code></td><td>在某次髒 WAL 緩衝區寫入完成時觸發的探針。</td></tr><tr><td><code class="literal">wal-insert</code></td><td><code class="literal">(unsigned char, unsigned char)</code></td><td>在某筆 WAL 紀錄插入時觸發的探針。
      arg0 為該紀錄的資源管理員（rmid）。
      arg1 存放資訊旗標。</td></tr><tr><td><code class="literal">wal-switch</code></td><td><code class="literal">()</code></td><td>在請求 WAL 區段切換時觸發的探針。</td></tr><tr><td><code class="literal">smgr-md-read-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>在開始從某關聯讀取區塊時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。</td></tr><tr><td><code class="literal">smgr-md-read-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)</code></td><td>在某次區塊讀取完成時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。
      arg6 為實際讀取的位元組數，arg7 為請求的位元組數
      （若兩者不同，代表發生了讀取不足）。</td></tr><tr><td><code class="literal">smgr-md-write-start</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int)</code></td><td>在開始將某區塊寫入至某關聯時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。</td></tr><tr><td><code class="literal">smgr-md-write-done</code></td><td><code class="literal">(ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)</code></td><td>在某次區塊寫入完成時觸發的探針。
      arg0 與 arg1，存放該頁面的分支與區塊編號。
      arg2、arg3 與 arg4，存放用以識別該關聯的資料表空間、
      資料庫，與關聯 OID。
      arg5 為建立該本機緩衝區暫存關聯之後端的 ID，
      若為共享緩衝區則為 <code class="symbol">INVALID_PROC_NUMBER</code>（-1）。
      arg6 為實際寫入的位元組數，arg7 為請求的位元組數
      （若兩者不同，代表發生了寫入不足）。</td></tr><tr><td><code class="literal">sort-start</code></td><td><code class="literal">(int, bool, int, int, bool, int)</code></td><td>在某次排序操作開始時觸發的探針。
      arg0 指出這是堆積、索引，還是資料項排序。
      arg1 在強制唯一值時為 true。
      arg2 為鍵欄位的數量。
      arg3 為允許使用的工作記憶體 KB 數。
      arg4 在需要對排序結果進行隨機存取時為 true。
      arg5 在為 <code class="literal">0</code> 時代表循序執行，
      為 <code class="literal">1</code> 時代表平行工作者，
      為 <code class="literal">2</code> 時代表平行領導者。</td></tr><tr><td><code class="literal">sort-done</code></td><td><code class="literal">(bool, long)</code></td><td>在某次排序完成時觸發的探針。
      arg0 在外部排序時為 true，內部排序時為 false。
      arg1 為外部排序所使用的磁碟區塊數，
      或內部排序所使用的記憶體 KB 數。</td></tr><tr><td><code class="literal">lwlock-acquire</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>在某個 LWLock 已被取得時觸發的探針。
      arg0 為該 LWLock 的 tranche。
      arg1 為所請求的鎖定模式，可能是互斥或共享。</td></tr><tr><td><code class="literal">lwlock-release</code></td><td><code class="literal">(char *)</code></td><td>在某個 LWLock 已被釋放時觸發的探針
      （但請注意，任何因此被釋放的等待者，
      此時尚未被喚醒）。
      arg0 為該 LWLock 的 tranche。</td></tr><tr><td><code class="literal">lwlock-wait-start</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>在某個 LWLock 並非立即可用、
      伺服器程序已開始等待該鎖定可用時觸發的探針。
      arg0 為該 LWLock 的 tranche。
      arg1 為所請求的鎖定模式，可能是互斥或共享。</td></tr><tr><td><code class="literal">lwlock-wait-done</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>在伺服器程序已結束等待某個 LWLock
      （但尚未實際取得該鎖定）時觸發的探針。
      arg0 為該 LWLock 的 tranche。
      arg1 為所請求的鎖定模式，可能是互斥或共享。</td></tr><tr><td><code class="literal">lwlock-condacquire</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>在呼叫者指定不等待、且成功取得某個 LWLock 時
      觸發的探針。
      arg0 為該 LWLock 的 tranche。
      arg1 為所請求的鎖定模式，可能是互斥或共享。</td></tr><tr><td><code class="literal">lwlock-condacquire-fail</code></td><td><code class="literal">(char *, LWLockMode)</code></td><td>在呼叫者指定不等待、但未能成功取得某個 LWLock 時
      觸發的探針。
      arg0 為該 LWLock 的 tranche。
      arg1 為所請求的鎖定模式，可能是互斥或共享。</td></tr><tr><td><code class="literal">lock-wait-start</code></td><td><code class="literal">(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)</code></td><td>在某個重量級鎖定（lmgr lock）的請求，
      因該鎖定不可用而開始等待時觸發的探針。
      arg0 到 arg3，是用來識別被鎖定物件的標籤欄位。
      arg4 指出被鎖定物件的類型。
      arg5 指出所請求的鎖定類型。</td></tr><tr><td><code class="literal">lock-wait-done</code></td><td><code class="literal">(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)</code></td><td>在某個重量級鎖定（lmgr lock）的請求
      結束等待（也就是已取得該鎖定）時觸發的探針。
      其引數與 <code class="literal">lock-wait-start</code> 相同。</td></tr><tr><td><code class="literal">deadlock-found</code></td><td><code class="literal">()</code></td><td>在死結偵測器發現死結時觸發的探針。</td></tr></tbody></table>

<br><a id="TYPEDEFS-TABLE"></a>

### 表 27.50. 探針參數中所使用的已定義型別 [#](#typedefs-table) <a href="#typedefs-table" id="typedefs-table"></a>

<table border="1" class="table" summary="Defined Types Used in Probe Parameters"><colgroup><col/><col/></colgroup><thead><tr><th>型別</th><th>定義</th></tr></thead><tbody><tr><td><code class="type">LocalTransactionId</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">LWLockMode</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">LOCKMODE</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">BlockNumber</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">Oid</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">ForkNumber</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bool</code></td><td><code class="type">unsigned char</code></td></tr></tbody></table>

<br>

[返回 27.5. 動態追蹤](../dynamic-trace.md#dynamic-trace)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dynamic-trace.html)（原文版本：18.6；核對日期：2026-09-26）
