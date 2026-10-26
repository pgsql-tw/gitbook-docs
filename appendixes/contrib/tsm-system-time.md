<a id="TSM-SYSTEM-TIME"></a>

## F.47. tsm_system_time — `TABLESAMPLE` 的 `SYSTEM_TIME` 取樣方法 [#](#tsm-system-time) <a href="#tsm-system-time" id="tsm-system-time"></a>

[F.47.1. 範例](tsm-system-time.md#TSM-SYSTEM-TIME-EXAMPLES)

<a id="id-1.11.7.57.2"></a>

`tsm_system_time` 模組提供資料表取樣方法 `SYSTEM_TIME`，可用於 [`SELECT`](../../reference/sql-commands/sql-select.md) 命令的 `TABLESAMPLE` 子句。

此資料表取樣方法接受單一浮點數引數，表示讀取資料表時最多可花費的毫秒數。這讓你可以直接控制查詢所需的時間，代價是樣本的大小變得難以預測。產生的樣本會包含在指定時間內能讀取的所有資料列，除非整個資料表已先讀取完畢。

與內建的 `SYSTEM` 取樣方法一樣，`SYSTEM_TIME` 執行區塊層級的取樣，因此樣本並非完全隨機，而可能受到群聚效應影響，尤其是只選取少量資料列時。

`SYSTEM_TIME` 不支援 `REPEATABLE` 子句。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="TSM-SYSTEM-TIME-EXAMPLES"></a>

### F.47.1. 範例 [#](#TSM-SYSTEM-TIME-EXAMPLES)

以下是使用 `SYSTEM_TIME` 選取資料表樣本的範例。首先安裝擴充功能：

```

CREATE EXTENSION tsm_system_time;
```

接著即可在 `SELECT` 命令中使用它，例如：

```

SELECT * FROM my_table TABLESAMPLE SYSTEM_TIME(1000);
```

此命令會傳回 `my_table` 在 1 秒（1000 毫秒）內所能讀取的最大樣本。當然，若整個資料表能在小於 1 秒的時間內讀完，就會傳回其所有資料列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tsm-system-time.html)（原文版本：18.6；核對日期：2026-10-22）
