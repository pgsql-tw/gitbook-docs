<a id="TSM-SYSTEM-ROWS"></a>

## F.46. tsm_system_rows — `TABLESAMPLE` 的 `SYSTEM_ROWS` 取樣方法 [#](#tsm-system-rows) <a href="#tsm-system-rows" id="tsm-system-rows"></a>

[F.46.1. 範例](tsm-system-rows.md#tsm-system-rows-examples)

<a id="id-1.11.7.56.2"></a>

`tsm_system_rows` 模組提供資料表取樣方法 `SYSTEM_ROWS`，可用於 [`SELECT`](../../reference/sql-commands/sql-select.md) 命令的 `TABLESAMPLE` 子句。

此資料表取樣方法接受單一整數引數，表示要讀取的最大資料列數。產生的樣本一定會恰好包含該數量的資料列，除非資料表沒有足夠的資料列，此時會選取整個資料表。

與內建的 `SYSTEM` 取樣方法一樣，`SYSTEM_ROWS` 執行區塊層級的取樣，因此樣本並非完全隨機，而可能受到群聚效應影響，尤其是只要求少量資料列時。

`SYSTEM_ROWS` 不支援 `REPEATABLE` 子句。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="TSM-SYSTEM-ROWS-EXAMPLES"></a>

### F.46.1. 範例 [#](#tsm-system-rows-examples) <a href="#tsm-system-rows-examples" id="tsm-system-rows-examples"></a>

以下是使用 `SYSTEM_ROWS` 選取資料表樣本的範例。首先安裝擴充功能：

```

CREATE EXTENSION tsm_system_rows;
```

接著即可在 `SELECT` 命令中使用它，例如：

```

SELECT * FROM my_table TABLESAMPLE SYSTEM_ROWS(100);
```

此命令會從資料表 `my_table` 傳回 100 筆資料列的樣本（除非該資料表沒有 100 筆可見的資料列，此時會傳回其所有資料列）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tsm-system-rows.html)（原文版本：18.6；核對日期：2026-10-22）
