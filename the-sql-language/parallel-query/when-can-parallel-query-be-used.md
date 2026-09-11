<a id="WHEN-CAN-PARALLEL-QUERY-BE-USED"></a>

## 15.2. 何時可以使用平行查詢？ [#](#WHEN-CAN-PARALLEL-QUERY-BE-USED)

有幾項設定會導致查詢規劃器在任何情況下都不產生平行查詢計畫。要產生任何平行查詢計畫，下列設定必須依所示方式設定。

* [max_parallel_workers_per_gather](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) 必須設為大於零的值。這是一個更一般原則的特例：使用的工作程序數量不應超過透過 `max_parallel_workers_per_gather` 設定的數量。

此外，系統不能在單一使用者模式下執行。由於在這種情況下整個資料庫系統是以單一程序執行，因此不會有任何可用的背景工作程序。

即使一般而言可以產生平行查詢計畫，只要下列任一項成立，規劃器就不會為特定查詢產生平行計畫：

* 查詢會寫入任何資料或鎖定任何資料庫資料列。如果查詢在最上層或 CTE 中包含資料修改操作，就不會為該查詢產生平行計畫。作為例外，下列建立新資料表並填入資料的指令，可以對查詢中底層的 `SELECT` 部分使用平行計畫：

  * `CREATE TABLE ... AS`
  * `SELECT INTO`
  * `CREATE MATERIALIZED VIEW`
  * `REFRESH MATERIALIZED VIEW`
* 查詢在執行期間可能會被暫停。在系統認為可能會發生部分或增量執行的任何情況下，都不會產生平行計畫。例如，以 [DECLARE CURSOR](../../reference/sql-commands/sql-declare.md) 建立的游標永遠不會使用平行計畫。同樣地，`FOR x IN query LOOP .. END LOOP` 形式的 PL/pgSQL 迴圈也永遠不會使用平行計畫，因為平行查詢系統無法驗證迴圈中的程式碼在平行查詢作用期間執行是否安全。
* 查詢使用了任何標記為 `PARALLEL UNSAFE` 的函式。大多數系統定義的函式都是 `PARALLEL SAFE`，但使用者自訂的函式預設會被標記為 `PARALLEL UNSAFE`。請參閱[第 15.4 節](parallel-safety.md)的討論。
* 查詢是在另一個已經在平行執行的查詢中執行。例如，如果平行查詢所呼叫的函式本身又發出 SQL 查詢，該查詢永遠不會使用平行計畫。這是目前實作的限制，但移除這項限制未必是理想的，因為那可能導致單一查詢使用非常大量的程序。

即使為特定查詢產生了平行查詢計畫，在執行時仍有幾種情況會使該計畫無法平行執行。如果發生這種情況，領導程序會完全自行執行 `Gather` 節點以下的那部分計畫，幾乎就像 `Gather` 節點不存在一樣。只要符合下列任一條件，就會發生這種情況：

* 由於背景工作程序總數不能超過 [max_worker_processes](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 的限制，而無法取得任何背景工作程序。
* 由於為平行查詢目的而啟動的背景工作程序總數不能超過 [max_parallel_workers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS) 的限制，而無法取得任何背景工作程序。
* 用戶端傳送了取回數量不為零的 Execute 訊息。請參閱[延伸查詢協定](../../internals/protocol/protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)的討論。由於 [libpq](../../client-interfaces/libpq/README.md) 目前沒有提供傳送這種訊息的方式，這種情況只會在使用不依賴 libpq 的用戶端時發生。如果這種情況經常發生，在可能發生的工作階段中將 [max_parallel_workers_per_gather](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) 設為零或許是個好主意，以避免產生在循序執行時可能不是最佳的查詢計畫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/when-can-parallel-query-be-used.html)（原文版本：18.6；核對日期：2026-09-11）
