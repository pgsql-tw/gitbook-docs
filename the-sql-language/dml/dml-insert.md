<a id="DML-INSERT"></a>

## 6.1. 插入資料 [#](#DML-INSERT)

<a id="id-1.5.5.3.2"></a><a id="id-1.5.5.3.3"></a>

資料表剛建立時不包含任何資料。資料庫要能發揮作用，第一件要做的事就是插入資料。資料是一次插入一筆資料列的。你也可以在單一命令中插入多筆資料列，但無法插入不完整的資料列。即使你只知道部分欄位的值，也必須建立一筆完整的資料列。

要建立新的資料列，請使用 [INSERT](../../reference/sql-commands/sql-insert.md) 命令。這個命令需要資料表名稱與欄位值。例如，考慮[第 5 章](../ddl/README.md)中的 products 資料表：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

插入一筆資料列的範例命令如下：

```

INSERT INTO products VALUES (1, 'Cheese', 9.99);
```

資料值依照欄位在資料表中出現的順序列出，並以逗號分隔。資料值通常是字面值（常數），但也可以使用純量運算式。

上面這種語法的缺點是，你必須知道資料表中欄位的順序。為了避免這一點，你也可以明確列出欄位。例如，下面兩個命令的效果都與上面的命令相同：

```

INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
INSERT INTO products (name, price, product_no) VALUES ('Cheese', 9.99, 1);
```

許多使用者認為一律列出欄位名稱是好的做法。

如果你沒有所有欄位的值，可以省略其中一些。在這種情況下，這些欄位會填入它們的預設值。例如：

```

INSERT INTO products (product_no, name) VALUES (1, 'Cheese');
INSERT INTO products VALUES (1, 'Cheese');
```

第二種形式是 PostgreSQL 的擴充功能。它會從左邊開始，依照所給的值數量填入欄位，其餘的欄位則使用預設值。

為了清楚起見，你也可以針對個別欄位或整筆資料列明確要求使用預設值：

```

INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
INSERT INTO products DEFAULT VALUES;
```

你可以在單一命令中插入多筆資料列：

```

INSERT INTO products (product_no, name, price) VALUES
    (1, 'Cheese', 9.99),
    (2, 'Bread', 1.99),
    (3, 'Milk', 2.99);
```

也可以插入查詢的結果（可能是零筆、一筆或多筆資料列）：

```

INSERT INTO products (product_no, name, price)
  SELECT product_no, name, price FROM new_products
    WHERE release_date = 'today';
```

這讓你可以運用 SQL 查詢機制（[第 7 章](../queries/README.md)）的完整能力來計算要插入的資料列。

### 提示

同時插入大量資料時，請考慮使用 [COPY](../../reference/sql-commands/sql-copy.md) 命令。它不如 [INSERT](../../reference/sql-commands/sql-insert.md) 命令靈活，但更有效率。關於提升大量載入效能的更多資訊，請參閱[第 14.4 節](../performance-tips/populate.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dml-insert.html)（原文版本：18.6；核對日期：2026-09-11）
