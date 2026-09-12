<a id="DDL-SYSTEM-COLUMNS"></a>

## 5.6. 系統欄位 [#](#DDL-SYSTEM-COLUMNS)

每個資料表都有數個由系統隱含定義的*系統欄位*（system column）。因此，這些名稱不能用作使用者自訂欄位的名稱。（請注意，這些限制與該名稱是否為關鍵字無關；為名稱加上引號並不能讓你避開這些限制。）你其實不需要關心這些欄位；只要知道它們存在就好。

<a id="id-1.5.4.8.3"></a>

<a id="DDL-SYSTEM-COLUMNS-TABLEOID"></a>

`tableoid` [#](#DDL-SYSTEM-COLUMNS-TABLEOID)
:   <a id="id-1.5.4.8.4.1.2.1"></a>

    包含這筆資料列之資料表的 OID。對於從分割資料表（請參閱[第 5.12 節](ddl-partitioning.md)）或繼承階層（請參閱[第 5.11 節](ddl-inherit.md)）中選取資料的查詢，這個欄位特別方便，因為沒有它的話，就很難分辨某筆資料列來自哪一個個別的資料表。可以將 `tableoid` 與 `pg_class` 的 `oid` 欄位聯結，以取得資料表名稱。
<a id="DDL-SYSTEM-COLUMNS-XMIN"></a>

`xmin` [#](#DDL-SYSTEM-COLUMNS-XMIN)
:   <a id="id-1.5.4.8.4.2.2.1"></a>

    插入這個資料列版本之交易的識別碼（交易 ID）。（資料列版本是資料列的某個個別狀態；每次更新資料列，都會為同一筆邏輯資料列建立一個新的資料列版本。）
<a id="DDL-SYSTEM-COLUMNS-CMIN"></a>

`cmin` [#](#DDL-SYSTEM-COLUMNS-CMIN)
:   <a id="id-1.5.4.8.4.3.2.1"></a>

    在執行插入的交易中的命令識別碼（從零開始）。
<a id="DDL-SYSTEM-COLUMNS-XMAX"></a>

`xmax` [#](#DDL-SYSTEM-COLUMNS-XMAX)
:   <a id="id-1.5.4.8.4.4.2.1"></a>

    執行刪除之交易的識別碼（交易 ID）；對於未被刪除的資料列版本則為零。這個欄位在可見的資料列版本中有可能不為零。這通常表示執行刪除的交易尚未提交，或是嘗試進行的刪除已被回復。
<a id="DDL-SYSTEM-COLUMNS-CMAX"></a>

`cmax` [#](#DDL-SYSTEM-COLUMNS-CMAX)
:   <a id="id-1.5.4.8.4.5.2.1"></a>

    在執行刪除的交易中的命令識別碼，或為零。
<a id="DDL-SYSTEM-COLUMNS-CTID"></a>

`ctid` [#](#DDL-SYSTEM-COLUMNS-CTID)
:   <a id="id-1.5.4.8.4.6.2.1"></a>

    資料列版本在其資料表中的實體位置。請注意，雖然 `ctid` 可以用來非常快速地找到資料列版本，但如果資料列被更新或被 `VACUUM FULL` 移動，它的 `ctid` 就會改變。因此，`ctid` 不應該用作資料列識別碼。應該使用主鍵來識別邏輯資料列。

交易識別碼也是 32 位元的數值。在長期運作的資料庫中，交易 ID 有可能發生迴繞（wraparound）。只要有適當的維護程序，這並不是致命的問題；詳情請參閱[第 24 章](../../server-administration/maintenance/README.md)。不過，長期依賴交易 ID 的唯一性（超過十億筆交易）是不明智的。

命令識別碼也是 32 位元的數值。這為單一交易中的 SQL 命令數量設下了 2^32（40 億）個的硬性上限。在實務上，這個上限並不是問題——請注意，這個上限針對的是 SQL 命令的數量，而不是處理的資料列數。此外，只有實際修改資料庫內容的命令才會消耗命令識別碼。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-system-columns.html)（原文版本：18.6；核對日期：2026-09-11）
