<a id="SQL-ALTERSTATISTICS"></a><a id="id-1.9.3.32.1"></a>

## ALTER STATISTICS

ALTER STATISTICS — 變更擴充統計資訊物件的定義

<a id="id-1.9.3.32.4"></a>

## 語法

```

ALTER STATISTICS name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER STATISTICS name RENAME TO new_name
ALTER STATISTICS name SET SCHEMA new_schema
ALTER STATISTICS name SET STATISTICS { new_target | DEFAULT }
```

<a id="id-1.9.3.32.5"></a>

## 說明

`ALTER STATISTICS` 會變更現有擴充統計資訊物件的參數。未在 `ALTER STATISTICS` 命令中特別設定的參數，都會保留原先的設定。

你必須擁有該統計資訊物件，才能使用 `ALTER STATISTICS`。若要變更統計資訊物件的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該統計資訊物件所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立統計資訊物件而做到的事。不過，超級使用者無論如何都可以變更任何統計資訊物件的擁有權。）

<a id="id-1.9.3.32.6"></a>

## 參數

*`name`*
:   要變更的統計資訊物件名稱（可選擇以綱要限定）。

*`new_owner`*
:   統計資訊物件新擁有者的使用者名稱。

*`new_name`*
:   統計資訊物件的新名稱。

*`new_schema`*
:   統計資訊物件的新綱要。

*`new_target`*
:   此統計資訊物件在後續 [`ANALYZE`](sql-analyze.md) 操作中的統計資訊收集目標。目標可以設定在 0 到 10000 的範圍內。將它設為 `DEFAULT`，即可改回使用系統預設的統計目標（[default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)）。（設為 -1 的值是取得相同結果的過時寫法。）有關 PostgreSQL 查詢規劃器如何使用統計資訊的更多資訊，請參閱[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)。

<a id="id-1.9.3.32.7"></a>

## 相容性

SQL 標準中沒有 `ALTER STATISTICS` 命令。

<a id="id-1.9.3.32.8"></a>

## 另請參閱

[CREATE STATISTICS](sql-createstatistics.md), [DROP STATISTICS](sql-dropstatistics.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterstatistics.html)（原文版本：18.6；核對日期：2026-10-05）
