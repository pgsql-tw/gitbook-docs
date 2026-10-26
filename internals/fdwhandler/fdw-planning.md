<a id="FDW-PLANNING"></a>

## 58.4. 外部資料包裝器查詢規劃 [#](#fdw-planning) <a href="#fdw-planning" id="fdw-planning"></a>

FDW 回呼函式 `GetForeignRelSize`、
`GetForeignPaths`、`GetForeignPlan`、
`PlanForeignModify`、`GetForeignJoinPaths`、
`GetForeignUpperPaths` 與 `PlanDirectModify`
必須配合 PostgreSQL 規劃器的運作方式。
以下是關於它們必須做哪些事的一些說明。

`root` 與 `baserel` 中的資訊可用來
減少必須從外部資料表擷取的資訊量（從而降低成本）。
`baserel->baserestrictinfo` 特別值得注意，因為
它包含應該用來篩選要擷取之資料列的限制條件（quals，即 `WHERE` 子句）。
（FDW 本身不一定要強制執行這些條件，因為核心執行器可以代為檢查。）
`baserel->reltarget->exprs` 可用來判斷哪些
欄位需要擷取；但請注意，它只列出必須由
`ForeignScan` 計畫節點輸出的欄位，而不包括
用於條件求值、但不由查詢輸出的欄位。

有多個私有欄位可供 FDW 規劃函式
保存資訊。一般而言，你存放在 FDW 私有欄位中的任何內容
都應該以 palloc 配置，以便在規劃結束時被回收。

`baserel->fdw_private` 是一個 `void` 指標，
可供 FDW 規劃函式存放與該特定外部資料表相關的資訊。
核心規劃器除了在建立 `RelOptInfo` 節點時將它初始化為 NULL 之外，不會碰觸它。
它可用於把資訊從
`GetForeignRelSize` 往後傳給 `GetForeignPaths`，以及／或從
`GetForeignPaths` 傳給 `GetForeignPlan`，藉此
避免重複計算。

`GetForeignPaths` 可以透過在
`ForeignPath` 節點的 `fdw_private` 欄位中存放私有資訊，
來識別不同存取路徑的意義。
`fdw_private` 宣告為 `List` 指標，但
實際上可以包含任何內容，因為核心規劃器不會碰觸
它。不過，最佳做法是使用可由
`nodeToString` 傾印的表示方式，以便搭配
後端中可用的除錯支援使用。

`GetForeignPlan` 可以檢查所選 `ForeignPath` 節點的 `fdw_private`
欄位，並可以產生
`fdw_exprs` 與 `fdw_private` 串列，
放入 `ForeignScan` 計畫節點中，讓它們在
執行時可供使用。這兩個串列都必須以
`copyObject` 知道如何複製的形式表示。
`fdw_private` 串列沒有其他限制，
核心後端也不會以任何方式解讀它。
`fdw_exprs` 串列若不為 NIL，則預期包含
要在執行時執行的運算式樹。這些
運算式樹會經過規劃器的後處理，使其成為完全
可執行的形式。

在 `GetForeignPlan` 中，傳入的目標清單通常可以
原封不動地複製到計畫節點中。傳入的 `scan_clauses` 串列
包含與 `baserel->baserestrictinfo` 相同的子句，
但可能為了更好的執行效率而重新排序。在簡單的情況下，
FDW 只需從 `scan_clauses` 串列中去除 `RestrictInfo` 節點
（使用 `extract_actual_clauses`），然後把
所有子句放入計畫節點的條件串列，這表示所有
子句都會在執行時由執行器檢查。較複雜的 FDW
可能能夠在內部檢查部分子句，此時這些
子句可以從計畫節點的條件串列中移除，讓
執行器不必浪費時間重新檢查它們。

舉例來說，FDW 可能會識別出某些形式為
*`foreign_variable`* `=`
*`sub_expression`* 的限制子句，並判定在給定
*`sub_expression`* 於本地求得的值之後，這些子句可以在
遠端伺服器上執行。這類子句的實際識別
應該在 `GetForeignPaths` 期間進行，因為它會
影響該路徑的成本估算。該路徑的
`fdw_private` 欄位可能會包含指向
已識別子句之 `RestrictInfo` 節點的指標。接著
`GetForeignPlan` 會從 `scan_clauses` 中移除該子句，
但將 *`sub_expression`* 加入 `fdw_exprs`，
以確保它會被轉換成可執行的形式。它可能
也會在計畫節點的
`fdw_private` 欄位中放入控制資訊，告訴執行函式在
執行時要做什麼。傳送到遠端伺服器的查詢會
包含類似 `WHERE foreign_variable =
$1` 的內容，其參數值在執行時由
`fdw_exprs` 運算式樹求值取得。

任何從計畫節點條件串列中移除的子句，都必須改為加入
`fdw_recheck_quals`，或由
`RecheckForeignScan` 重新檢查，以確保在
`READ COMMITTED` 隔離等級下行為正確。當查詢中涉及的
其他資料表發生並行更新時，執行器
可能需要針對該元組（tuple），驗證所有原始條件是否仍然成立，
而且可能是針對一組不同的參數值。使用
`fdw_recheck_quals` 通常比在
`RecheckForeignScan` 中實作檢查容易，但當外部連接（outer join）已被下推時，
這種方法就不足夠了，因為在該情況下，連接元組
可能會有某些欄位變成 NULL，而不是整個元組
被拒絕。

FDW 可以填入的另一個 `ForeignScan` 欄位
是 `fdw_scan_tlist`，它描述 FDW 為此計畫節點
傳回的元組。對於簡單的外部資料表掃描，它可以
設為 `NIL`，表示傳回的元組具有
為該外部資料表宣告的資料列型別。非 `NIL` 的值必須是一個
目標清單（`TargetEntry` 的串列），其中包含表示傳回欄位的 Var 和／或
運算式。例如，這可用來
表示 FDW 已省略了某些它注意到
查詢不需要的欄位。此外，如果 FDW 計算查詢所用運算式的成本
比在本地計算更低，它可以把
這些運算式加入 `fdw_scan_tlist`。請注意，連接
計畫（由 `GetForeignJoinPaths` 所產生的路徑建立而來）必須
一律提供 `fdw_scan_tlist`，以描述它們將傳回的
欄位集合。

FDW 應該一律建構至少一個只相依於
資料表限制子句的路徑。在連接查詢中，它也可能選擇
建構相依於連接子句的路徑，例如
*`foreign_variable`* `=`
*`local_variable`*。這類子句不會出現在
`baserel->baserestrictinfo` 中，而必須在
該關聯的連接串列中尋找。使用這類子句的路徑稱為
「參數化路徑」（parameterized path）。它必須以適當的
`param_info` 值，識別所選連接子句中使用的其他關聯；
請使用 `get_baserel_parampathinfo`
來計算該值。在 `GetForeignPlan` 中，
連接子句的 *`local_variable`* 部分會被加入
`fdw_exprs`，然後在執行時，這種情況的處理方式
就與一般的限制子句相同。

如果 FDW 支援遠端連接，`GetForeignJoinPaths` 應該
為可能的遠端連接產生 `ForeignPath`，方式大致
與 `GetForeignPaths` 處理基礎資料表相同。
關於預定連接的資訊，可以用上述相同的方式往後傳給
`GetForeignPlan`。
不過，`baserestrictinfo` 與連接
關聯無關；特定連接的相關連接子句，會改以獨立參數
（`extra->restrictlist`）傳給 `GetForeignJoinPaths`。

FDW 還可以支援直接執行某些位於
掃描與連接層級之上的計畫動作，例如分組或
彙總。為了提供這類選項，FDW 應該產生路徑，並
將它們插入適當的*上層關聯*（upper relation）。例如，
代表遠端彙總的路徑應該使用 `add_path` 插入
`UPPERREL_GROUP_AGG` 關聯。
此路徑會與透過讀取外部關聯之簡單掃描路徑來執行的本地彙總
進行成本比較（請注意，這樣的路徑也必須提供，
否則在規劃時會發生錯誤）。如果遠端彙總路徑勝出（通常會如此），
它會以一般方式，透過
呼叫 `GetForeignPlan` 轉換為計畫。產生
這類路徑的建議位置是 `GetForeignUpperPaths`
回呼函式；若查詢的所有基礎關聯
都來自同一個 FDW，系統就會為每個上層關聯（也就是每個
掃描／連接後的處理步驟）呼叫此函式。

`PlanForeignModify` 與
[第 58.2.4 節](fdw-callbacks.md#fdw-callbacks-update)所述的其他回呼函式，其設計基於以下假設：
外部關聯會以一般方式被掃描，然後
由本地的 `ModifyTable`
計畫節點驅動個別資料列的更新。對於更新除了外部資料表之外
還需要讀取本地資料表的一般性情況，這種做法是必要的。
然而，如果該操作可以完全由外部
伺服器執行，FDW 可以產生代表該操作的路徑，並將它插入
`UPPERREL_FINAL` 上層關聯，讓它
與 `ModifyTable` 做法相互競爭。這種做法
也可用於實作遠端 `SELECT FOR UPDATE`，
而不使用
[第 58.2.6 節](fdw-callbacks.md#fdw-callbacks-row-locking)所述的資料列鎖定回呼函式。請記住，
插入 `UPPERREL_FINAL` 的路徑必須負責
實作該查詢的*所有*行為。

在規劃 `UPDATE` 或 `DELETE` 時，
`PlanForeignModify` 與 `PlanDirectModify`
可以查詢該外部資料表的 `RelOptInfo`
結構，並利用先前由
掃描規劃函式建立的 `baserel->fdw_private` 資料。不過，在 `INSERT` 中，目標
資料表不會被掃描，因此沒有它的 `RelOptInfo`。
`PlanForeignModify` 所傳回的 `List`，
與 `ForeignScan` 計畫節點的 `fdw_private` 串列
有相同的限制，也就是它只能包含
`copyObject` 知道如何複製的結構。

帶有 `ON CONFLICT` 子句的 `INSERT` 不
支援指定衝突目標，因為遠端資料表上的唯一性限制條件或
排除限制條件在本地是未知的。這
進一步表示不支援 `ON CONFLICT DO UPDATE`，
因為在那裡必須指定衝突目標。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fdw-planning.html)（原文版本：18.6；核對日期：2026-10-17）
