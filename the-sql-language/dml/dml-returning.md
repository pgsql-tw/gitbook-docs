<a id="DML-RETURNING"></a>

## 6.4. 從修改的資料列回傳資料 [#](#DML-RETURNING)

<a id="id-1.5.5.6.2"></a><a id="id-1.5.5.6.3"></a><a id="id-1.5.5.6.4"></a><a id="id-1.5.5.6.5"></a><a id="id-1.5.5.6.6"></a>

有時候，在操作資料列的同時取得被修改之資料列的資料會很有用。`INSERT`、`UPDATE`、`DELETE` 與 `MERGE` 命令都有一個選用的 `RETURNING` 子句來支援這一點。使用 `RETURNING` 可以避免為了收集資料而額外執行一次資料庫查詢，而在原本難以可靠地識別出被修改之資料列的情況下，它尤其有價值。

`RETURNING` 子句允許的內容，與 `SELECT` 命令的輸出清單相同（請參閱[第 7.3 節](../queries/queries-select-lists.md)）。它可以包含命令之目標資料表的欄位名稱，或使用這些欄位的值運算式。一種常見的簡寫是 `RETURNING *`，它會依序選取目標資料表的所有欄位。

在 `INSERT` 中，`RETURNING` 預設可用的資料是剛插入的那筆資料列。這在一般的插入中不太有用，因為它只是重複用戶端所提供的資料。但在依賴計算出來的預設值時，它會非常方便。例如，當使用 [`serial`](../datatype/datatype-numeric.md#DATATYPE-SERIAL) 欄位來提供唯一識別碼時，`RETURNING` 可以回傳指派給新資料列的 ID：

```

CREATE TABLE users (firstname text, lastname text, id serial primary key);

INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;
```

`RETURNING` 子句搭配 `INSERT ... SELECT` 使用也非常有用。

在 `UPDATE` 中，`RETURNING` 預設可用的資料是被修改之資料列的新內容。例如：

```

UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, price AS new_price;
```

在 `DELETE` 中，`RETURNING` 預設可用的資料是被刪除之資料列的內容。例如：

```

DELETE FROM products
  WHERE obsoletion_date = 'today'
  RETURNING *;
```

在 `MERGE` 中，`RETURNING` 預設可用的資料是來源資料列的內容，再加上被插入、更新或刪除之目標資料列的內容。由於來源與目標有許多相同欄位的情況相當常見，指定 `RETURNING *` 可能會產生許多重複的欄位，因此加以限定、只回傳來源或目標資料列，往往更有用。例如：

```

MERGE INTO products p USING new_products n ON p.product_no = n.product_no
  WHEN NOT MATCHED THEN INSERT VALUES (n.product_no, n.name, n.price)
  WHEN MATCHED THEN UPDATE SET name = n.name, price = n.price
  RETURNING p.*;
```

在上述每一種命令中，也都可以明確回傳被修改之資料列的舊內容與新內容。例如：

```

UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, old.price AS old_price, new.price AS new_price,
            new.price - old.price AS price_change;
```

在這個範例中，寫 `new.price` 和直接寫 `price` 是一樣的，但前者讓意義更清楚。

這種回傳舊值與新值的語法，可以用在 `INSERT`、`UPDATE`、`DELETE` 與 `MERGE` 命令中，但通常 `INSERT` 的舊值會是 `NULL`，而 `DELETE` 的新值會是 `NULL`。不過，在某些情況下，它對這些命令仍然可能有用。例如，在帶有 [`ON CONFLICT DO UPDATE`](../../reference/sql-commands/sql-insert.md#SQL-ON-CONFLICT) 子句的 `INSERT` 中，發生衝突之資料列的舊值會是非 `NULL` 的。同樣地，如果 `DELETE` 被[改寫規則](../../reference/sql-commands/sql-createrule.md)轉換成 `UPDATE`，新值可能會是非 `NULL` 的。

如果目標資料表上有觸發程序（[第 37 章](../../server-programming/triggers/README.md)），`RETURNING` 可用的資料就是經過觸發程序修改之後的資料列。因此，檢視由觸發程序計算出的欄位，是 `RETURNING` 的另一個常見用途。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dml-returning.html)（原文版本：18.6；核對日期：2026-09-11）
