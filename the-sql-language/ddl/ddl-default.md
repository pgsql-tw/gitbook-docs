<a id="DDL-DEFAULT"></a>

## 5.2. 預設值 [#](#DDL-DEFAULT)

<a id="id-1.5.4.4.2"></a>

欄位可以被指定一個預設值。當建立新的資料列，而某些欄位沒有指定值時，這些欄位就會填入各自的預設值。資料操作指令也可以明確地要求將某個欄位設為它的預設值，而不需要知道那個值究竟是什麼。（資料操作指令的細節請參閱[第 6 章](../dml/README.md)。）

<a id="id-1.5.4.4.4.1"></a>
如果沒有明確宣告預設值，預設值就是空值。這通常是合理的，因為空值可以視為代表未知的資料。

在資料表定義中，預設值列在欄位資料型別之後。例如：

```

CREATE TABLE products (
    product_no integer,
    name text,
    price numeric DEFAULT 9.99
);
```

預設值可以是一個運算式，它會在每次插入預設值時被求值（*而不是*在資料表建立時）。常見的例子是讓 `timestamp` 欄位的預設值為 `CURRENT_TIMESTAMP`，這樣它就會被設成資料列插入時的時間。另一個常見的例子是為每一筆資料列產生「序號」。在 PostgreSQL 中，這通常是以類似下面的方式來完成：

```

CREATE TABLE products (
    product_no integer DEFAULT nextval('products_product_no_seq'),
    ...
);
```

其中 `nextval()` 函式會從*序列物件*提供接續的值（請參閱[第 9.17 節](../functions/functions-sequence.md)）。這種安排相當常見，因此有一個特別的簡寫方式：

```

CREATE TABLE products (
    product_no SERIAL,
    ...
);
```

`SERIAL` 簡寫在[第 8.1.4 節](../datatype/datatype-numeric.md#DATATYPE-SERIAL)中有進一步的說明。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-default.html)（原文版本：18.6；核對日期：2026-09-13）
