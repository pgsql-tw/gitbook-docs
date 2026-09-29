<a id="id-1.9.3.162.1"></a>

## REFRESH MATERIALIZED VIEW

REFRESH MATERIALIZED VIEW — 取代一個具體化檢視表的內容

## 語法

```

REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] name
    [ WITH [ NO ] DATA ]
```

<a id="id-1.9.3.162.5"></a>

## 說明

`REFRESH MATERIALIZED VIEW` 會完全取代一個具體化檢視表的內容。若要執行此指令，你必須在該具體化檢視表上具備
`MAINTAIN`
權限。舊有的內容會被捨棄。如果指定了
`WITH DATA`（或採用預設值），系統會執行其背後的查詢以提供新資料，並讓該具體化檢視表處於可掃描狀態。如果指定了
`WITH NO DATA`，則不會產生新資料，該具體化檢視表會處於不可掃描狀態。

`CONCURRENTLY` 與 `WITH NO DATA` 不可
同時指定。

<a id="id-1.9.3.162.6"></a>

## 參數

`CONCURRENTLY`
:   在重新整理具體化檢視表時，不鎖定對該具體化檢視表的並行查詢（select）。若不使用此選項，影響大量資料列的重新整理往往會使用較少的資源並更快完成，但可能會阻擋其他正嘗試從該具體化檢視表讀取的連線。在只有少量資料列受影響的情況下，此選項可能較快。

    只有在該具體化檢視表上至少存在一個僅使用欄位名稱、且涵蓋所有資料列的
    `UNIQUE` 索引時，才允許使用此選項；也就是說，該索引不能是運算式索引，也不能包含
    `WHERE` 子句。

    此選項只能在該具體化檢視表已經填入資料時使用。

    即使使用此選項，針對任一個具體化檢視表，一次也只能執行一個
    `REFRESH`。

*`name`*
:   要重新整理的具體化檢視表名稱（可加上綱要限定）。

<a id="id-1.9.3.162.7"></a>

## 注意

如果具體化檢視表的定義查詢中包含 `ORDER BY` 子句，該具體化檢視表的原始內容會依此順序排列；但
`REFRESH MATERIALIZED
VIEW` 並不保證會維持這個順序。

在 `REFRESH MATERIALIZED VIEW` 執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog,
pg_temp`。

<a id="id-1.9.3.162.8"></a>

## 範例

以下指令會使用具體化檢視表定義中的查詢，取代名為
`order_summary` 的具體化檢視表之內容，並使其保持在可掃描狀態：

```

REFRESH MATERIALIZED VIEW order_summary;
```

以下指令會釋放具體化檢視表
`annual_statistics_basis` 所佔用的儲存空間，並使其處於不可掃描狀態：

```

REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

<a id="id-1.9.3.162.9"></a>

## 相容性

`REFRESH MATERIALIZED VIEW` 是
PostgreSQL 的擴充功能。

<a id="id-1.9.3.162.10"></a>

## 另請參閱

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-refreshmaterializedview.html)（原文版本：18.6；核對日期：2026-09-28）
