<a id="SQL-ALTERINDEX"></a><a id="id-1.9.3.16.1"></a>

## ALTER INDEX

ALTER INDEX — 變更索引的定義

<a id="id-1.9.3.16.4"></a>

## 語法

```

ALTER INDEX [ IF EXISTS ] name RENAME TO new_name
ALTER INDEX [ IF EXISTS ] name SET TABLESPACE tablespace_name
ALTER INDEX name ATTACH PARTITION index_name
ALTER INDEX name [ NO ] DEPENDS ON EXTENSION extension_name
ALTER INDEX [ IF EXISTS ] name SET ( storage_parameter [= value] [, ... ] )
ALTER INDEX [ IF EXISTS ] name RESET ( storage_parameter [, ... ] )
ALTER INDEX [ IF EXISTS ] name ALTER [ COLUMN ] column_number
    SET STATISTICS integer
ALTER INDEX ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]
```

<a id="id-1.9.3.16.5"></a>

## 說明

`ALTER INDEX` 會變更現有索引的定義。它有下列幾種子形式。請注意，每種子形式所需的鎖定層級可能不同。除非另有明確說明，否則會持有 `ACCESS EXCLUSIVE` 鎖定。若列出了多個子命令，所持有的鎖定會是所有子命令所需鎖定中最嚴格的那一個。

`RENAME`

`RENAME` 形式會變更索引的名稱。若該索引與某個資料表限制條件（`UNIQUE`、`PRIMARY KEY` 或 `EXCLUDE`）相關聯，該限制條件也會一併重新命名。這對已儲存的資料沒有影響。

重新命名索引會取得 `SHARE UPDATE EXCLUSIVE` 鎖定。

`SET TABLESPACE`
:   此形式會將索引的資料表空間變更為指定的資料表空間，並將與該索引相關聯的資料檔案移到新的資料表空間。要變更索引的資料表空間，你必須是該索引的擁有者，並且具有新資料表空間的 `CREATE` 權限。使用 `ALL IN TABLESPACE` 形式，可以移動目前資料庫中位於某個資料表空間內的所有索引；此形式會先鎖定所有要移動的索引，然後再逐一移動。此形式也支援 `OWNED BY`，只會移動由指定角色所擁有的索引。若指定了 `NOWAIT` 選項，則當無法立即取得所有需要的鎖定時，命令就會失敗。請注意，此命令不會移動系統目錄；如有需要，請改用 `ALTER DATABASE` 或明確的 `ALTER INDEX` 呼叫。另請參閱 [`CREATE TABLESPACE`](sql-createtablespace.md)。

`ATTACH PARTITION index_name`

使指定的索引（可能以綱要限定）附加到被修改的索引。指定的索引必須位於包含被修改索引之資料表的某個分割區上，並且具有等價的定義。已附加的索引不能單獨移除，而且在其父索引被移除時會自動移除。

若指定的索引已經附加到被修改的索引，而父索引目前為無效（invalid）狀態，此命令會嘗試驗證父索引。

`DEPENDS ON EXTENSION extension_name`<br>`NO DEPENDS ON EXTENSION extension_name`
:   此形式會將索引標記為相依於該擴充功能；若指定了 `NO`，則標記為不再相依於該擴充功能。被標記為相依於某個擴充功能的索引，會在該擴充功能被移除時自動移除。

`SET ( storage_parameter [= value] [, ... ] )`
:   此形式會變更索引的一個或多個索引方法特定的儲存參數。可用參數的詳細資訊請參閱 [`CREATE INDEX`](sql-createindex.md)。請注意，此命令不會立即修改索引內容；視參數而定，你可能需要使用 [`REINDEX`](sql-reindex.md) 重建索引，才能得到想要的效果。

`RESET ( storage_parameter [, ... ] )`
:   此形式會將一個或多個索引方法特定的儲存參數重設為預設值。與 `SET` 相同，可能需要執行 `REINDEX` 才能完整更新索引。

`ALTER [ COLUMN ] column_number SET STATISTICS integer`
:   此形式會為後續的 [`ANALYZE`](sql-analyze.md) 操作設定各欄位的統計資訊收集目標，但只能用於定義為運算式的索引欄位。由於運算式沒有唯一的名稱，我們使用索引欄位的序數來參照它們。目標可設定的範圍為 0 到 10000；或者，將它設為 -1 以恢復使用系統預設的統計目標（[default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)）。關於 PostgreSQL 查詢規劃器如何使用統計資訊的詳細資訊，請參閱[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)。

<a id="id-1.9.3.16.6"></a>

## 參數

`IF EXISTS`
:   索引不存在時不擲出錯誤；此情況會發出 notice。

*`column_number`*
:   序數是指索引欄位的序數位置（由左至右）。

*`name`*
:   要修改的現有索引名稱（可能以綱要限定）。

*`new_name`*
:   索引的新名稱。

*`tablespace_name`*
:   索引將被移入的資料表空間。

*`extension_name`*
:   索引要相依的擴充功能名稱。

*`storage_parameter`*
:   索引方法特定的儲存參數名稱。

*`value`*
:   索引方法特定儲存參數的新值。視參數而定，這可能是一個數字或一個單字。

<a id="id-1.9.3.16.7"></a>

## 注意事項

這些操作也可以使用 [`ALTER TABLE`](sql-altertable.md) 進行。事實上，`ALTER INDEX` 只是 `ALTER TABLE` 中適用於索引之形式的別名。

以前曾有 `ALTER INDEX OWNER` 變體，但現在會被忽略（並發出警告）。索引的擁有者不能與其資料表的擁有者不同。變更資料表的擁有者時，索引的擁有者也會自動跟著變更。

不允許變更系統目錄索引的任何部分。

<a id="id-1.9.3.16.8"></a>

## 範例

重新命名現有索引：

```

ALTER INDEX distributors RENAME TO suppliers;
```

將索引移到不同的資料表空間：

```

ALTER INDEX distributors SET TABLESPACE fasttablespace;
```

變更索引的填充因子（假設該索引方法支援）：

```

ALTER INDEX distributors SET (fillfactor = 75);
REINDEX INDEX distributors;
```

為運算式索引設定統計資訊收集目標：

```

CREATE INDEX coord_idx ON measured (x, y, (z + t));
ALTER INDEX coord_idx ALTER COLUMN 3 SET STATISTICS 1000;
```

<a id="id-1.9.3.16.9"></a>

## 相容性

`ALTER INDEX` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.16.10"></a>

## 另請參閱

[CREATE INDEX](sql-createindex.md), [REINDEX](sql-reindex.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterindex.html)（原文版本：18.6；核對日期：2026-10-05）
