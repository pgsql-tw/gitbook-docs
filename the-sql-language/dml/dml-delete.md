## 6.3. 刪除資料 [#](#DML-DELETE)

<a id="id-1.5.5.5.2"></a><a id="id-1.5.5.5.3"></a>

到目前為止，我們已說明如何將資料加入資料表及如何變更資料。接下來要討論如何移除不再需要的資料。如同加入資料只能以完整資料列進行，你也只能從資料表移除完整資料列。前一節已說明 SQL 無法直接指定位址到個別資料列。因此，刪除資料列時只能指定資料列必須符合的條件。若資料表有主鍵，你可以指定確切資料列；也可以刪除符合條件的一組資料列，或一次刪除資料表中的所有資料列。

你可以使用 [DELETE](../../reference/sql-commands/sql-delete.md) 命令移除資料列；其語法與 [UPDATE](../../reference/sql-commands/sql-update.md) 命令非常相似。舉例來說，若要從 products 資料表移除所有價格為 10 的資料列，請使用：

```

DELETE FROM products WHERE price = 10;
```

如果只寫：

```

DELETE FROM products;
```

那麼資料表中的所有資料列都會被刪除！請務必小心。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dml-delete.html)（原文版本：18.6；核對日期：2026-09-10）
