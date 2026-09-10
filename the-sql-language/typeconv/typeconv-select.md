## 10.6. `SELECT` 輸出欄位 [#](#TYPECONV-SELECT)

<a id="id-1.5.9.11.2"></a>

前幾節所述的規則會為 SQL 查詢中的所有運算式指派非 `unknown` 資料型別，但不包括以 `SELECT` 命令簡單輸出欄位出現的未指定型別字面值。例如，在

```

SELECT 'Hello World';
```

沒有資訊可判定字串字面值應採用何種型別。在此情況下，PostgreSQL 會將字面值的型別解析為 `text`。

當 `SELECT` 是 `UNION`（或 `INTERSECT` 或 `EXCEPT`）結構的一個分支，或出現在 `INSERT ... SELECT` 內時，這項規則不適用，因為前幾節的規則具有優先權。第一種情況下，未指定型別字面值可從另一個 `UNION` 分支取得型別；第二種情況則從目標欄位取得型別。

在此目的下，`RETURNING` 清單與 `SELECT` 輸出清單採相同處理方式。

### 注意

在 PostgreSQL 10 之前，這項規則不存在，`SELECT` 輸出清單中的未指定型別字面值會保留為 `unknown` 型別。這會造成各種不良後果，因此已變更此行為。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv-select.html)（原文版本：18.6；核對日期：2026-09-10）
