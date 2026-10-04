<a id="SQL-ALTERTABLESPACE"></a><a id="id-1.9.3.36.1"></a>

## ALTER TABLESPACE

ALTER TABLESPACE — 變更資料表空間的定義

<a id="id-1.9.3.36.4"></a>

## 語法

```

ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
```

<a id="id-1.9.3.36.5"></a>

## 說明

`ALTER TABLESPACE` 可用來變更資料表空間的定義。

你必須擁有該資料表空間，才能變更其定義。若要變更擁有者，你還必須能夠 `SET ROLE` 成為新的擁有者角色。（請注意，超級使用者自動具有這些權限。）

<a id="id-1.9.3.36.6"></a>

## 參數

*`name`*
:   現有資料表空間的名稱。

*`new_name`*
:   資料表空間的新名稱。新名稱不能以 `pg_` 開頭，因為這類名稱保留給系統資料表空間使用。

*`new_owner`*
:   資料表空間的新擁有者。

*`tablespace_option`*
:   要設定或重設的資料表空間參數。目前可用的參數只有 `seq_page_cost`、`random_page_cost`、`effective_io_concurrency` 與 `maintenance_io_concurrency`。為特定資料表空間設定這些值，會覆寫規劃器對於讀取該資料表空間中資料表之頁面成本的一般估計，以及發出多少個並行 I/O 的一般估計；這些一般估計是由同名的設定參數所決定（請參閱 [seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST)、[random_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-RANDOM-PAGE-COST)、[effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY)、[maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)）。若某個資料表空間位於比 I/O 子系統其餘部分更快或更慢的磁碟上，這可能很有用。

<a id="id-1.9.3.36.7"></a>

## 範例

將資料表空間 `index_space` 重新命名為 `fast_raid`：

```

ALTER TABLESPACE index_space RENAME TO fast_raid;
```

變更資料表空間 `index_space` 的擁有者：

```

ALTER TABLESPACE index_space OWNER TO mary;
```

<a id="id-1.9.3.36.8"></a>

## 相容性

SQL 標準中沒有 `ALTER TABLESPACE` 陳述式。

<a id="id-1.9.3.36.9"></a>

## 另請參閱

[CREATE TABLESPACE](sql-createtablespace.md), [DROP TABLESPACE](sql-droptablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertablespace.html)（原文版本：18.6；核對日期：2026-10-04）
