<a id="XPROC"></a>
## 36.4. 使用者自訂程序 [#](#XPROC)

<a id="id-1.8.3.7.2"></a>

程序是一種類似函式的資料庫物件。主要差異在於：

* 程序是以 [`CREATE PROCEDURE`](../../reference/sql-commands/sql-createprocedure.md) 命令定義，而不是 `CREATE FUNCTION`。
* 程序不會回傳函式值；因此 `CREATE PROCEDURE` 沒有 `RETURNS` 子句。不過，程序可以改為透過輸出參數把資料回傳給呼叫端。
* 函式是作為查詢或 DML 命令的一部分被呼叫，而程序則是單獨使用 [`CALL`](../../reference/sql-commands/sql-call.md) 命令來呼叫。
* 只要呼叫用的 `CALL` 命令不是明確交易區塊的一部分，程序就可以在執行期間提交或回復交易（接著自動開始一個新交易）。函式無法這麼做。
* 某些函式屬性（例如嚴格性）並不適用於程序。這些屬性所控制的，是函式在查詢中如何被使用，這與程序無關。

以下各節關於如何定義使用者自訂函式的說明，除了上述幾點之外，同樣也適用於程序。

函式與程序合稱為*常式*（routines）<a id="id-1.8.3.7.5.2"></a>。有一些命令，例如 [`ALTER ROUTINE`](../../reference/sql-commands/sql-alterroutine.md) 與 [`DROP ROUTINE`](../../reference/sql-commands/sql-droproutine.md)，可以在不必知道是哪一種的情況下，同時對函式與程序進行操作。不過請注意，並沒有 `CREATE ROUTINE` 這個命令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xproc.html)（原文版本：18.6；核對日期：2026-09-15）
