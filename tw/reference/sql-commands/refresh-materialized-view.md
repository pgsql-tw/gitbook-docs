# REFRESH MATERIALIZED VIEW

REFRESH MATERIALIZED VIEW — 更新具體化檢視表（materialized view）的內容

## 語法

```text
REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] name
    [ WITH [ NO ] DATA ]
```

## 說明

REFRESH MATERIALIZED VIEW 完全更新具體化檢視表的內容。舊的內容將會被丟棄。如果指定了 WITH DATA（預設），則會執行檢視表上的查詢以産生新資料，並且使具體化檢視表處於可掃描查詢的狀態。如果指定了 WITH NO DATA，則不會産生新的資料，並且具體化檢視表將處於不可掃描查詢的狀態。

CONCURRENTLY 和 WITH NO DATA 不能同時使用。

## 參數

`CONCURRENTLY`

更新具體化檢視表而不鎖定具體化檢視表上同時進行的 SELECT。如果沒有使用這個選項的話，如果有很多資料列會更新時，將傾向於使用更少的資源並且更快地完成，但可能會阻止嘗試從具體化檢視表中讀取的其他連線。在只有少數資料列受到影響的情況下，此選項則可能會更快。

具體化檢視表上至少有一個唯一索引且僅使用欄位名稱並包含所有資料列時，才允許使用此選項；也就是說，它不能以任何表示式建立索引，也不能包含 WHERE 子句。

當具體化檢視表尚未填入資料時，不能使用此選項。

即使使用此選項，每次也只有一個 REFRESH 對一個具體化檢視表執行。

_`name`_

要更新的具體化檢視表的名稱（可以加上綱要名稱）。

## 注意

儘管保留了未來 [CLUSTER](cluster.md) 操作的預設索引，但 REFRESH MATERIALIZED VIEW 並不會根據此屬性對産生的資料列進行排序。如果您希望在産生後對資料進行排序，則必須在檢視表的查詢中使用 ORDER BY 子句。

## 範例

此命令將更新名為 order\_summary 的具體化檢視表定義的查詢結果內容，並將其設定為可掃描查詢狀態：

```text
REFRESH MATERIALIZED VIEW order_summary;
```

該命令將釋放與具體化檢視表 annual\_statistics\_basis 相關的儲存空間，並使其處於不可掃描查詢的狀態：

```text
REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

## 相容性

`REFRESH MATERIALIZED VIEW` 是 PostgreSQL 的延伸指令。

## 參閱

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [ALTER MATERIALIZED VIEW](alter-materialized-view.md), [DROP MATERIALIZED VIEW](drop-materialized-view.md)

