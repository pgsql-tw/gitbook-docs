<a id="PARALLEL-SAFETY"></a>

## 15.4. 平行安全性 [#](#PARALLEL-SAFETY)

[15.4.1. 函式與彙總函式的平行標記](parallel-safety.md#PARALLEL-LABELING)

規劃器會將查詢中涉及的操作分類為*平行安全*（parallel safe）、*平行受限*（parallel restricted）或*平行不安全*（parallel unsafe）。平行安全的操作是與使用平行查詢不衝突的操作。平行受限的操作是不能在平行工作程序中執行，但在使用平行查詢時可以在領導程序中執行的操作。因此，平行受限的操作永遠不會出現在 `Gather` 或 `Gather Merge` 節點之下，但可以出現在包含這類節點之計畫的其他位置。平行不安全的操作則是在使用平行查詢時完全不能執行的操作，即使在領導程序中也不行。當查詢包含任何平行不安全的內容時，該查詢就會完全停用平行查詢。

下列操作一律是平行受限的：

* 掃描通用資料表運算式（CTE）。
* 掃描暫存資料表。
* 掃描外部資料表，除非外部資料包裝器（foreign data wrapper）有 `IsForeignScanParallelSafe` API 指出並非如此。
* 參照相關 `SubPlan` 的計畫節點。

<a id="PARALLEL-LABELING"></a>

### 15.4.1. 函式與彙總函式的平行標記 [#](#PARALLEL-LABELING)

規劃器無法自動判定使用者自訂的函式或彙總函式是平行安全、平行受限還是平行不安全的，因為這需要預測函式可能執行的每一項操作。一般而言，這等同於停機問題（Halting Problem），因此是不可能的。即使對於可以想像能夠判定的簡單函式，我們也不會嘗試，因為這樣做的成本很高而且容易出錯。取而代之的是，除非另有標記，所有使用者自訂的函式都會被假定為平行不安全。使用 [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) 或 [ALTER FUNCTION](../../reference/sql-commands/sql-alterfunction.md) 時，可以視情況指定 `PARALLEL SAFE`、`PARALLEL RESTRICTED` 或 `PARALLEL UNSAFE` 來設定標記。使用 [CREATE AGGREGATE](../../reference/sql-commands/sql-createaggregate.md) 時，可以為 `PARALLEL` 選項指定對應的值 `SAFE`、`RESTRICTED` 或 `UNSAFE`。

如果函式與彙總函式會寫入資料庫、改變交易狀態（使用子交易進行錯誤復原的情況除外）、存取序列（sequence），或對設定進行持久性的變更，就必須標記為 `PARALLEL UNSAFE`。同樣地，如果函式會存取暫存資料表、用戶端連線狀態、游標、預備陳述式，或系統無法在工作程序之間同步的其他後端本地狀態，就必須標記為 `PARALLEL RESTRICTED`。例如，`setseed` 與 `random` 就是因為最後這個原因而屬於平行受限。

一般而言，如果函式實際上是受限或不安全的，卻被標記為安全；或者實際上是不安全的，卻被標記為受限，那麼在平行查詢中使用時，它可能會拋出錯誤或產生錯誤的答案。如果 C 語言函式被錯誤標記，理論上可能會表現出完全未定義的行為，因為系統無法防範任意的 C 程式碼；但在最可能的情況下，結果並不會比任何其他函式更糟。如果有疑慮，最好將函式標記為 `UNSAFE`。

如果在平行工作程序中執行的函式取得了領導程序並未持有的鎖定（例如查詢了查詢中未參照的資料表），這些鎖定會在工作程序結束時釋放，而不是在交易結束時釋放。如果你撰寫的函式會這樣做，而這種行為差異對你很重要，請將這類函式標記為 `PARALLEL RESTRICTED`，以確保它們只在領導程序中執行。

請注意，查詢規劃器不會為了取得更好的計畫，而考慮延後查詢中所涉及之平行受限函式或彙總函式的求值。因此，例如，如果套用在某個資料表上的 `WHERE` 子句是平行受限的，查詢規劃器就不會考慮在計畫的平行部分中掃描該資料表。在某些情況下，將該資料表的掃描納入查詢的平行部分，並延後 `WHERE` 子句的求值，讓它發生在 `Gather` 節點之上，是可能的（甚至可能很有效率）。不過，規劃器並不會這樣做。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/parallel-safety.html)（原文版本：18.6；核對日期：2026-09-11）
