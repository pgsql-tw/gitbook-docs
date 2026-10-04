<a id="SQL-CLOSE"></a><a id="id-1.9.3.50.1"></a><a id="id-1.9.3.50.2"></a>

## CLOSE

CLOSE — 關閉游標

<a id="id-1.9.3.50.5"></a>

## 語法

```

CLOSE { name | ALL }
```

<a id="id-1.9.3.50.6"></a>

## 說明

`CLOSE` 會釋放與已開啟游標相關聯的資源。游標關閉之後，就不允許再對它進行任何後續操作。游標在不再需要時應該關閉。

當交易以 `COMMIT` 或 `ROLLBACK` 結束時，每個不可保留（non-holdable）的已開啟游標都會被隱含地關閉。若建立可保留（holdable）游標的交易經由 `ROLLBACK` 中止，該游標會被隱含地關閉。若建立它的交易成功提交，可保留游標會維持開啟，直到明確執行 `CLOSE`，或用戶端中斷連線為止。

<a id="id-1.9.3.50.7"></a>

## 參數

*`name`*
:   要關閉的已開啟游標名稱。

`ALL`
:   關閉所有已開啟的游標。

<a id="id-1.9.3.50.8"></a>

## 注意事項

PostgreSQL 沒有明確的 `OPEN` 游標陳述式；游標在宣告時即被視為已開啟。請使用 [`DECLARE`](sql-declare.md) 陳述式宣告游標。

你可以查詢 [`pg_cursors`](../../internals/views/view-pg-cursors.md) 系統檢視表，查看所有可用的游標。

若游標是在某個儲存點之後關閉，而該儲存點之後被回復，則 `CLOSE` 不會被回復；也就是說，該游標仍維持關閉。

<a id="id-1.9.3.50.9"></a>

## 範例

關閉游標 `liahona`：

```

CLOSE liahona;
```

<a id="id-1.9.3.50.10"></a>

## 相容性

`CLOSE` 完全符合 SQL 標準。`CLOSE ALL` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.50.11"></a>

## 另請參閱

[DECLARE](sql-declare.md), [FETCH](sql-fetch.md), [MOVE](sql-move.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-close.html)（原文版本：18.6；核對日期：2026-10-04）
