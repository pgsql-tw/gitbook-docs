# 5.3. 限制條件[^1]

資料型別是一種限制資料如何被儲存在表格中的方式。然而，對許多應用來說，這樣的限制還是不夠細膩。舉個例子，一個欄位包含了產品價格，當然它必須只能是正整數，但並沒有標準的資料型別可以只限制在正整數。另一個需求是，你可能想要限制的條件是依據其他的資料而定。舉例來說，在表格中的產品資訊，每一個產品編號都不能重覆。

所以，SQL 允許你在表格和欄位上定義額外的限制條件，它幫助你對資料有更多的控制能力。當某個使用者輸入資料時，違反了限制條件，錯誤訊息就會產生。這些限制條件也會限制預設值的設定。

### 5.3.1. 檢查

使用 CHECK 是最普遍的限制條件製定方式，它可以允許你指定某個欄位必須符合某個布林條件式的判斷。舉個例子，要滿足產品價格是正數的話，你可以使用這樣的語法：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

如同你所看到的，限制條件會接在資料型別之後，就像是預設值的設定一樣。預設值和限制條件的設定，在語法撰寫上沒有先後次序。檢查限制條件使用關鍵字 CHECK，然後接著是一組以括號括起來的條件式。其條件式應該要包含被限制的欄位，不然就沒有任何意義。

你也可以讓該限制條件擁有另一個名稱，這樣的好處是，當錯誤訊息發生時，你可以明確得到是哪一個限制被違反了：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric 
CONSTRAINT positive_price CHECK (price > 0)
);
```

如上，給予這個限制條件一個名稱，使用關鍵字 CONSTRAINT，緊接著一個限制條件的定義。（如果你沒有自行命名，系統也會自動取一個名字）

一個限制條件可以參考多個欄位。例如你設定了標準價格和優惠價格，而你需要確保優惠價格一定是比標準價格要便宜的話：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

前兩個限制條件和前述很類似，而第三個是新的語法。它並不是只參考某個特定的欄位，而是以逗號分隔列出所有需要遵守的條件。欄位的定義和限制條件的定義，撰寫上沒有規定次序。

我們會說前兩個是欄位的限制，而第三個是表格的限制，因為它是獨立於其他的欄位定義的。欄位限制也可以寫成表格的限制方式，不過反過來通常就不行，因為一個欄位的限制，指的就是只參考到語法上它所接續的欄位而已。（PostgreSQL 並沒有強制這樣做，但如果你的語法與其他資料庫共用的話，最好還是依這樣的語法避免混用。）上面的例子也可以改寫成如此：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

或等同於：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
);
```

都可以照你所喜愛的語法撰寫。

命名表格的限制條件和欄位限制條件的命名是一樣的：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),

    CONSTRAINT valid_discount CHECK (price > discounted_price)
);
```

應該要注意的是，檢查限制條件是否成立，端看條件表示式在運算後是真值（true）還是空值（null）。因為當有運算元是空值時，多數的運算結果都是空值，所以可能會有空值產生在想要限制條件的欄位之中。要確保欄位中不會出現空值的話，請參閱下一段的說明。

### 5.3.2. Not-Null Constraints

A not-null constraint simply specifies that a column must not assume the null value. A syntax example:

```
CREATE TABLE products (
    product_no integer 
NOT NULL
,
    name text 
NOT NULL
,
    price numeric
);
```

A not-null constraint is always written as a column constraint. A not-null constraint is functionally equivalent to creating a check constraint`CHECK (`\_`column_name`\_IS NOT NULL\), but inPostgreSQLcreating an explicit not-null constraint is more efficient. The drawback is that you cannot give explicit names to not-null constraints created this way.

Of course, a column can have more than one constraint. Just write the constraints one after another:

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price 
>
 0)
);
```

The order doesn't matter. It does not necessarily determine in which order the constraints are checked.

The`NOT NULL`constraint has an inverse: the`NULL`constraint. This does not mean that the column must be null, which would surely be useless. Instead, this simply selects the default behavior that the column might be null. The`NULL`constraint is not present in the SQL standard and should not be used in portable applications. \(It was only added toPostgreSQLto be compatible with some other database systems.\) Some users, however, like it because it makes it easy to toggle the constraint in a script file. For example, you could start with:

```
CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);
```

and then insert the`NOT`key word where desired.

### Tip

In most database designs the majority of columns should be marked not null.

### 5.3.3. Unique Constraints

Unique constraints ensure that the data contained in a column, or a group of columns, is unique among all the rows in the table. The syntax is:

```
CREATE TABLE products (
    product_no integer 
UNIQUE
,
    name text,
    price numeric
);
```

when written as a column constraint, and:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,

UNIQUE (product_no)

);
```

when written as a table constraint.

To define a unique constraint for a group of columns, write it as a table constraint with the column names separated by commas:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,

UNIQUE (a, c)

);
```

This specifies that the combination of values in the indicated columns is unique across the whole table, though any one of the columns need not be \(and ordinarily isn't\) unique.

You can assign your own name for a unique constraint, in the usual way:

```
CREATE TABLE products (
    product_no integer 
CONSTRAINT must_be_different
 UNIQUE,
    name text,
    price numeric
);
```

Adding a unique constraint will automatically create a unique B-tree index on the column or group of columns listed in the constraint. A uniqueness restriction covering only some rows cannot be written as a unique constraint, but it is possible to enforce such a restriction by creating a unique[partial index](https://www.postgresql.org/docs/10/static/indexes-partial.html).

In general, a unique constraint is violated if there is more than one row in the table where the values of all of the columns included in the constraint are equal. However, two null values are never considered equal in this comparison. That means even in the presence of a unique constraint it is possible to store duplicate rows that contain a null value in at least one of the constrained columns. This behavior conforms to the SQL standard, but we have heard that other SQL databases might not follow this rule. So be careful when developing applications that are intended to be portable.

### 5.3.4. Primary Keys

A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table. This requires that the values be both unique and not null. So, the following two table definitions accept the same data:

```
CREATE TABLE products (
    product_no integer UNIQUE NOT NULL,
    name text,
    price numeric
);
```

```
CREATE TABLE products (
    product_no integer 
PRIMARY KEY
,
    name text,
    price numeric
);
```

Primary keys can span more than one column; the syntax is similar to unique constraints:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,

PRIMARY KEY (a, c)

);
```

Adding a primary key will automatically create a unique B-tree index on the column or group of columns listed in the primary key, and will force the column\(s\) to be marked`NOT NULL`.

A table can have at most one primary key. \(There can be any number of unique and not-null constraints, which are functionally almost the same thing, but only one can be identified as the primary key.\) Relational database theory dictates that every table must have a primary key. This rule is not enforced byPostgreSQL, but it is usually best to follow it.

Primary keys are useful both for documentation purposes and for client applications. For example, a GUI application that allows modifying row values probably needs to know the primary key of a table to be able to identify rows uniquely. There are also various ways in which the database system makes use of a primary key if one has been declared; for example, the primary key defines the default target column\(s\) for foreign keys referencing its table.

### 5.3.5. Foreign Keys

A foreign key constraint specifies that the values in a column \(or a group of columns\) must match the values appearing in some row of another table. We say this maintains the\_referential integrity\_between two related tables.

Say you have the product table that we have used several times already:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

Let's also assume you have a table storing orders of those products. We want to ensure that the orders table only contains orders of products that actually exist. So we define a foreign key constraint in the orders table that references the products table:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer 
REFERENCES products (product_no)
,
    quantity integer
);
```

Now it is impossible to create orders with non-NULL`product_no`entries that do not appear in the products table.

We say that in this situation the orders table is the\_referencing\_table and the products table is the\_referenced\_table. Similarly, there are referencing and referenced columns.

You can also shorten the above command to:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer 
REFERENCES products
,
    quantity integer
);
```

because in absence of a column list the primary key of the referenced table is used as the referenced column\(s\).

A foreign key can also constrain and reference a group of columns. As usual, it then needs to be written in table constraint form. Here is a contrived syntax example:

```
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,

FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)

);
```

Of course, the number and type of the constrained columns need to match the number and type of the referenced columns.

You can assign your own name for a foreign key constraint, in the usual way.

A table can have more than one foreign key constraint. This is used to implement many-to-many relationships between tables. Say you have tables about products and orders, but now you want to allow one order to contain possibly many products \(which the structure above did not allow\). You could use this table structure:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

Notice that the primary key overlaps with the foreign keys in the last table.

We know that the foreign keys disallow creation of orders that do not relate to any products. But what if a product is removed after an order is created that references it? SQL allows you to handle that as well. Intuitively, we have a few options:

* Disallow deleting a referenced product

* Delete the orders as well

* Something else?

To illustrate this, let's implement the following policy on the many-to-many relationship example above: when someone wants to remove a product that is still referenced by an order \(via`order_items`\), we disallow it. If someone removes an order, the order items are removed as well:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products 
ON DELETE RESTRICT
,
    order_id integer REFERENCES orders 
ON DELETE CASCADE
,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

Restricting and cascading deletes are the two most common options.`RESTRICT`prevents deletion of a referenced row.`NO ACTION`means that if any referencing rows still exist when the constraint is checked, an error is raised; this is the default behavior if you do not specify anything. \(The essential difference between these two choices is that`NO ACTION`allows the check to be deferred until later in the transaction, whereas`RESTRICT`does not.\)`CASCADE`specifies that when a referenced row is deleted, row\(s\) referencing it should be automatically deleted as well. There are two other options:`SET NULL`and`SET DEFAULT`. These cause the referencing column\(s\) in the referencing row\(s\) to be set to nulls or their default values, respectively, when the referenced row is deleted. Note that these do not excuse you from observing any constraints. For example, if an action specifies`SET DEFAULT`but the default value would not satisfy the foreign key constraint, the operation will fail.

Analogous to`ON DELETE`there is also`ON UPDATE`which is invoked when a referenced column is changed \(updated\). The possible actions are the same. In this case,`CASCADE`means that the updated values of the referenced column\(s\) should be copied into the referencing row\(s\).

Normally, a referencing row need not satisfy the foreign key constraint if any of its referencing columns are null. If`MATCH FULL`is added to the foreign key declaration, a referencing row escapes satisfying the constraint only if all its referencing columns are null \(so a mix of null and non-null values is guaranteed to fail a`MATCH FULL`constraint\). If you don't want referencing rows to be able to avoid satisfying the foreign key constraint, declare the referencing column\(s\) as`NOT NULL`.

A foreign key must reference columns that either are a primary key or form a unique constraint. This means that the referenced columns always have an index \(the one underlying the primary key or unique constraint\); so checks on whether a referencing row has a match will be efficient. Since a`DELETE`of a row from the referenced table or an`UPDATE`of a referenced column will require a scan of the referencing table for rows matching the old value, it is often a good idea to index the referencing columns too. Because this is not always needed, and there are many choices available on how to index, declaration of a foreign key constraint does not automatically create an index on the referencing columns.

More information about updating and deleting data is in[Chapter 6](https://www.postgresql.org/docs/10/static/dml.html). Also see the description of foreign key constraint syntax in the reference documentation for[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html).

### 5.3.6. Exclusion Constraints

Exclusion constraints ensure that if any two rows are compared on the specified columns or expressions using the specified operators, at least one of these operator comparisons will return false or null. The syntax is:

```
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

See also[`CREATE TABLE ... CONSTRAINT ... EXCLUDE`](https://www.postgresql.org/docs/10/static/sql-createtable.html#sql-createtable-exclude)for details.

Adding an exclusion constraint will automatically create an index of the type specified in the constraint declaration.

---

[^1]: [PostgreSQL: Documentation: 10: 5.3. Constraints](https://www.postgresql.org/docs/10/static/ddl-constraints.html)

