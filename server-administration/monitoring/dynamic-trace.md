<a id="DYNAMIC-TRACE"></a>

## 27.5. 動態追蹤 [#](#DYNAMIC-TRACE)

[27.5.1. 為動態追蹤編譯](dynamic-trace.md#COMPILING-FOR-TRACE)

[27.5.2. 內建探針](dynamic-trace.md#TRACE-POINTS)

[27.5.3. 使用探針](dynamic-trace.md#USING-TRACE-POINTS)

[27.5.4. 定義新探針](dynamic-trace.md#DEFINING-TRACE-POINTS)

<a id="id-1.6.14.10.2"></a>

PostgreSQL 提供了支援對資料庫伺服器
進行動態追蹤的功能。這能讓外部工具，
在程式碼中的特定位置被呼叫，藉此追蹤執行過程。

原始碼中已經插入了許多探針（probe）或追蹤點（trace point）。
這些探針的用意，是供資料庫開發人員與管理人員使用。
依預設，這些探針不會被編譯進 PostgreSQL 中；
使用者需要明確告知 configure 指令碼，
才能讓這些探針可供使用。

目前支援
[DTrace](https://en.wikipedia.org/wiki/DTrace)
工具，在撰寫本文時，該工具可在 Solaris、macOS、
FreeBSD、NetBSD，以及 Oracle Linux 上使用。
Linux 上的
[SystemTap](https://sourceware.org/systemtap/) 專案
提供了與 DTrace 相當的功能，同樣可供使用。
理論上，只要變更
`src/include/utils/probes.h` 中巨集的定義，
就能支援其他動態追蹤工具。

<a id="COMPILING-FOR-TRACE"></a>

### 27.5.1. 為動態追蹤編譯 [#](#COMPILING-FOR-TRACE)

依預設，探針並不可用，因此你需要明確告知 configure
指令碼，讓探針在 PostgreSQL 中可供使用。
若要納入 DTrace 支援，請在 configure 時指定
`--enable-dtrace`。詳情請參閱
[17.3.3.6 節](../installation/install-make.md#CONFIGURE-OPTIONS-DEVEL)。

<a id="TRACE-POINTS"></a>

### 27.5.2. 內建探針 [#](#TRACE-POINTS)

原始碼中提供了許多標準探針，
如[表 27.49](dynamic-trace.md#DTRACE-PROBE-POINT-TABLE)所示；
[表 27.50](dynamic-trace.md#TYPEDEFS-TABLE)
則顯示這些探針中所使用的型別。
當然，未來也能加入更多探針，
以增進 PostgreSQL 的可觀察性。

<a id="DTRACE-PROBE-POINT-TABLE"></a>

**表 27.49. 內建 DTrace 探針**

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
      <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-WAL-BUFFERS">wal_buffers</a>
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

**表 27.50. 探針參數中所使用的已定義型別**

<table border="1" class="table" summary="Defined Types Used in Probe Parameters"><colgroup><col/><col/></colgroup><thead><tr><th>型別</th><th>定義</th></tr></thead><tbody><tr><td><code class="type">LocalTransactionId</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">LWLockMode</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">LOCKMODE</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">BlockNumber</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">Oid</code></td><td><code class="type">unsigned int</code></td></tr><tr><td><code class="type">ForkNumber</code></td><td><code class="type">int</code></td></tr><tr><td><code class="type">bool</code></td><td><code class="type">unsigned char</code></td></tr></tbody></table>

<br>

<a id="USING-TRACE-POINTS"></a>

### 27.5.3. 使用探針 [#](#USING-TRACE-POINTS)

以下範例展示了一支 DTrace 指令碼，
用來分析系統中的交易計數，
可作為在效能測試前後對
`pg_stat_database` 拍攝快照的替代方案：

```

#!/usr/sbin/dtrace -qs

postgresql$1:::transaction-start
{
      @start["Start"] = count();
      self->ts  = timestamp;
}

postgresql$1:::transaction-abort
{
      @abort["Abort"] = count();
}

postgresql$1:::transaction-commit
/self->ts/
{
      @commit["Commit"] = count();
      @time["Total time (ns)"] = sum(timestamp - self->ts);
      self->ts=0;
}
```

執行後，此範例 D 指令碼會產生類似下列的輸出：

```

# ./txn_count.d `pgrep -n postgres` or ./txn_count.d <PID>
^C

Start                                          71
Commit                                         70
Total time (ns)                        2312105013
```

### 注意

SystemTap 用於追蹤指令碼的表示法，
與 DTrace 不同，即使底層的追蹤點是相容的。
值得留意的一點是，在撰寫本文時，
SystemTap 指令碼必須以雙底線取代連字號來參照探針名稱。
預期此問題會在未來的 SystemTap 版本中修正。

請務必記得，DTrace 指令碼需要謹慎撰寫並除錯，
否則所蒐集到的追蹤資訊可能毫無意義。
在大多數發現問題的情況下，出問題的往往是插樁（instrumentation）機制本身，
而非底層系統。在討論透過動態追蹤所發現的資訊時，
請務必一併附上所使用的指令碼，
以便他人也能檢查並討論該指令碼。

<a id="DEFINING-TRACE-POINTS"></a>

### 27.5.4. 定義新探針 [#](#DEFINING-TRACE-POINTS)

開發人員可以依需求，在程式碼中的任何位置定義新探針，
不過這需要重新編譯。以下是插入新探針的步驟：

1. 決定探針名稱，以及要透過探針提供哪些資料
2. 將探針定義加入 `src/backend/utils/probes.d`
3. 若含有探針點的模組中尚未含有 `pg_trace.h`，
   請將其納入，並在原始碼中所需的位置，
   插入 `TRACE_POSTGRESQL` 探針巨集
4. 重新編譯，並確認新的探針可供使用

**範例：**
以下範例展示了如何加入一個探針，
用來依交易 ID 追蹤所有新交易。

1. 決定此探針名稱為 `transaction-start`，
   且需要一個 `LocalTransactionId` 型別的參數
2. 將探針定義加入 `src/backend/utils/probes.d`：

   ```

   probe transaction__start(LocalTransactionId);
   ```

   請注意，探針名稱中使用了雙底線。在使用此探針的
   DTrace 指令碼中，雙底線需要替換為連字號，
   因此 `transaction-start` 才是要用於文件中、
   供使用者參考的名稱。
3. 在編譯時，`transaction__start` 會被轉換為一個
   名為 `TRACE_POSTGRESQL_TRANSACTION_START`
   的巨集（請注意，這裡的底線是單一底線），
   只要納入 `pg_trace.h` 即可使用。
   請將此巨集呼叫加入原始碼中適當的位置。
   在此範例中，看起來會像下列這樣：

   ```

   TRACE_POSTGRESQL_TRANSACTION_START(vxid.localTransactionId);
   ```
4. 重新編譯並執行新的二進位檔後，
   透過執行以下 DTrace 命令，
   檢查你新加入的探針是否可供使用。
   你應該會看到類似的輸出：

   ```

   # dtrace -ln transaction-start
      ID    PROVIDER          MODULE           FUNCTION NAME
   18705 postgresql49878     postgres     StartTransactionCommand transaction-start
   18755 postgresql49877     postgres     StartTransactionCommand transaction-start
   18805 postgresql49876     postgres     StartTransactionCommand transaction-start
   18855 postgresql49875     postgres     StartTransactionCommand transaction-start
   18986 postgresql49873     postgres     StartTransactionCommand transaction-start
   ```

在 C 程式碼中加入追蹤巨集時，有幾件事需要留意：

* 你應留意，為探針參數所指定的資料型別，
  必須與巨集中所使用之變數的資料型別相符，
  否則就會產生編譯錯誤。
* 在大多數平台上，若 PostgreSQL 是以
  `--enable-dtrace` 建置的，
  則每當控制流程通過該巨集時，追蹤巨集的引數
  都會被求值，*即使當時並未進行任何追蹤*。
  若你只是要回報幾個區域變數的值，
  通常不需要為此擔心。但請留意，
  不要在引數中放入代價高昂的函式呼叫。
  若你確實需要這麼做，可考慮先檢查該追蹤是否確實已啟用，
  以此保護該巨集：

  ```

  if (TRACE_POSTGRESQL_TRANSACTION_START_ENABLED())
      TRACE_POSTGRESQL_TRANSACTION_START(some_function(...));
  ```

  每個追蹤巨集，都有一個對應的 `ENABLED` 巨集。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dynamic-trace.html)（原文版本：18.6；核對日期：2026-09-26）
