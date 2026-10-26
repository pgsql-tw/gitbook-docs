<a id="FDW-ROW-LOCKING"></a>

## 58.5. 外部資料包裝器中的資料列鎖定 [#](#fdw-row-locking) <a href="#fdw-row-locking" id="fdw-row-locking"></a>

如果 FDW 的底層儲存機制有鎖定個別資料列以防止這些資料列被並行更新的概念，
那麼 FDW 通常值得以在實務上盡可能接近一般
PostgreSQL 資料表所用語意的方式來執行資料列層級鎖定。
這當中牽涉到多項考量。

一個關鍵決定是要執行*提早
鎖定*（early locking）還是*延後鎖定*（late locking）。在提早鎖定中，資料列會在
首次從底層儲存區擷取時就被鎖定；而在
延後鎖定中，只有在確知資料列需要被鎖定時才會鎖定它。
（之所以會有差異，是因為有些資料列可能會被
在本地檢查的限制條件或連接條件捨棄。）提早鎖定簡單得多，
也能避免與遠端儲存區之間額外的往返，但它可能導致
鎖定了原本不需要鎖定的資料列，造成並行性降低，
甚至發生非預期的死結。此外，只有在要鎖定的資料列
之後能再被唯一識別時，才可能使用延後鎖定。
資料列識別碼最好能識別資料列的特定版本，
就像 PostgreSQL 的 TID 那樣。

預設情況下，PostgreSQL 在與 FDW 介接時會忽略鎖定方面的考量，
但 FDW 不需要核心程式碼的任何明確支援就能執行提早鎖定。[第 58.2.6 節](fdw-callbacks.md#fdw-callbacks-row-locking)所述的 API 函式
是在 PostgreSQL 9.5 中加入的，它們讓 FDW 在需要時
可以使用延後鎖定。

另一個考量是，在 `READ COMMITTED`
隔離模式下，PostgreSQL 可能需要針對某個
目標元組（tuple）的更新後版本，重新檢查限制條件與連接條件。重新檢查連接條件需要重新取得
先前與該目標元組連接之非目標資料列的副本。
使用標準 PostgreSQL 資料表時，做法是
將非目標資料表的 TID 納入經由連接投影出的欄位清單中，
然後在需要時重新擷取非目標資料列。
這種做法能讓連接的資料集保持精簡，但它
需要低成本的重新擷取能力，以及一個能夠
唯一識別要重新擷取之資料列版本的 TID。因此，
外部資料表預設採用的做法，是將從外部資料表擷取的
整筆資料列副本納入經由連接投影出的欄位清單中。這對 FDW 沒有特別的要求，
但可能導致合併連接與雜湊連接的效能降低。能夠
滿足重新擷取要求的 FDW，可以選擇採用
第一種做法。

對於外部資料表上的 `UPDATE` 或 `DELETE`，
建議目標資料表上的 `ForeignScan` 操作
對它所擷取的資料列執行提早鎖定，或許可以透過
相當於 `SELECT FOR UPDATE` 的方式來進行。FDW 可以在規劃時
透過將資料表的 relid 與 `root->parse->resultRelation` 比較，
或在執行時使用 `ExecRelationIsTargetRelation()`，
來偵測該資料表是否為 `UPDATE`/`DELETE` 的目標。
另一種可行的做法是在
`ExecForeignUpdate` 或 `ExecForeignDelete`
回呼函式中執行延後鎖定，但系統並未為此提供特別的支援。

對於被 `SELECT
FOR UPDATE/SHARE` 命令指定要鎖定的外部資料表，`ForeignScan` 操作
同樣可以透過以相當於
`SELECT FOR UPDATE/SHARE` 的方式擷取元組來執行提早鎖定。若要改為執行延後鎖定，
請提供[第 58.2.6 節](fdw-callbacks.md#fdw-callbacks-row-locking)中定義的
回呼函式。
在 `GetForeignRowMarkType` 中，依據所要求的鎖定強度，選擇 rowmark 選項
`ROW_MARK_EXCLUSIVE`、`ROW_MARK_NOKEYEXCLUSIVE`、
`ROW_MARK_SHARE` 或 `ROW_MARK_KEYSHARE`。
（無論你選擇這四個選項中的哪一個，核心程式碼的行為都相同。）
在其他地方，你可以在規劃時使用 `get_plan_rowmark`，
或在執行時使用 `ExecFindRowMark`，來偵測外部資料表是否
被這類命令指定要鎖定；你不僅必須
檢查是否傳回了非 null 的 rowmark 結構，還必須檢查
其 `strength` 欄位不是 `LCS_NONE`。

最後，對於用在 `UPDATE`、
`DELETE` 或 `SELECT FOR UPDATE/SHARE` 命令中、但
未被指定要鎖定資料列的外部資料表，你可以讓
`GetForeignRowMarkType` 在看到鎖定強度
`LCS_NONE` 時選擇選項 `ROW_MARK_REFERENCE`，
藉此覆寫預設的複製整筆資料列的選擇。這會使 `RefetchForeignRow`
以該值作為 `markType` 被呼叫；接著它應該
在不取得任何新鎖定的情況下重新擷取該資料列。（如果你有
`GetForeignRowMarkType` 函式，但不希望重新擷取
未鎖定的資料列，請為 `LCS_NONE` 選擇選項 `ROW_MARK_COPY`。）

更多資訊請參閱 `src/include/nodes/lockoptions.h`、
`src/include/nodes/plannodes.h` 中
`RowMarkType` 與 `PlanRowMark` 的註解，以及
`src/include/nodes/execnodes.h` 中 `ExecRowMark` 的註解。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdw-row-locking.html)（原文版本：18.6；核對日期：2026-10-17）
