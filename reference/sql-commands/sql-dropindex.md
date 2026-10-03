<a id="SQL-DROPINDEX"></a><a id="id-1.9.3.116.1"></a>

## DROP INDEX

DROP INDEX — 移除索引

<a id="id-1.9.3.116.4"></a>

## 語法

```

DROP INDEX [ CONCURRENTLY ] [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.116.5"></a>

## 說明

`DROP INDEX` 會從資料庫系統中移除現有的索引。若要執行此命令，你必須是該索引的擁有者。

<a id="id-1.9.3.116.6"></a>

## 參數

`CONCURRENTLY`
:   移除索引時，不會封鎖該索引所屬資料表上並行的選取、插入、更新與刪除操作。一般的 `DROP INDEX` 會在資料表上取得 `ACCESS EXCLUSIVE` 鎖定，阻擋其他存取，直到索引移除能夠完成為止。使用此選項時，命令改為等待相衝突的交易完成。

    使用此選項時有幾項需要注意的限制。只能指定一個索引名稱，且不支援 `CASCADE` 選項。（因此，支援 `UNIQUE` 或 `PRIMARY KEY` 限制條件的索引無法以這種方式移除。）此外，一般的 `DROP INDEX` 命令可以在交易區塊內執行，但 `DROP INDEX CONCURRENTLY` 不行。最後，分割資料表上的索引無法使用此選項移除。

    對於暫存資料表，`DROP INDEX` 一律以非並行方式執行，因為其他工作階段都無法存取暫存資料表，而且非並行的索引移除成本較低。

`IF EXISTS`
:   索引不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之索引的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該索引的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該索引則拒絕移除。這是預設行為。

<a id="id-1.9.3.116.7"></a>

## 範例

此命令會移除索引 `title_idx`：

```

DROP INDEX title_idx;
```

<a id="id-1.9.3.116.8"></a>

## 相容性

`DROP INDEX` 是 PostgreSQL 的語言擴充功能。SQL 標準中沒有任何關於索引的規定。

<a id="id-1.9.3.116.9"></a>

## 另請參閱

[CREATE INDEX](sql-createindex.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropindex.html)（原文版本：18.6；核對日期：2026-10-03）
