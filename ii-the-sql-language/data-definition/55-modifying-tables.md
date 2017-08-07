# 5.5. 表格變更[^1]

當你建立了一個表格，而你發現出了點錯，或者應用需求有一些改變，那麼你可以移除它再重新建立。但這可能不會一個好的選擇，當表格中已經儲存了許多資料時，或者表格正在被其他的資料庫物件所參考中（例如外部鍵參考）。所以 PostgreSQL 提供了一系列的指令來修改現存的表格。注意到這和更新表格內資料的概念是不同的：在這裡，我們主要針對的是調整表格的定義或結構。

你可以：

* 加入欄位
* 移除欄位
* 加入限制條件
* 移除限制條件
* 改變預設值
* 改變欄位資料型別
* 變更欄位名稱
* 變更表格名稱

所有這些動作都透過 [ALTER TABLE](/vi-reference/i-sql-commands/alter-table.md) 指令來進行，你可以參考該頁面取得詳細資訊。

### 5.5.1. Adding a Column

To add a column, use a command like:

```
ALTER TABLE products ADD COLUMN description text;
```

The new column is initially filled with whatever default value is given \(null if you don't specify a`DEFAULT`clause\).

You can also define constraints on the column at the same time, using the usual syntax:

```
ALTER TABLE products ADD COLUMN description text CHECK (description 
<
>
 '');
```

In fact all the options that can be applied to a column description in`CREATE TABLE`can be used here. Keep in mind however that the default value must satisfy the given constraints, or the`ADD`will fail. Alternatively, you can add constraints later \(see below\) after you've filled in the new column correctly.

### Tip

Adding a column with a default requires updating each row of the table \(to store the new column value\). However, if no default is specified,PostgreSQLis able to avoid the physical update. So if you intend to fill the column with mostly nondefault values, it's best to add the column with no default, insert the correct values using`UPDATE`, and then add any desired default as described below.

### 5.5.2. Removing a Column

To remove a column, use a command like:

```
ALTER TABLE products DROP COLUMN description;
```

Whatever data was in the column disappears. Table constraints involving the column are dropped, too. However, if the column is referenced by a foreign key constraint of another table,PostgreSQLwill not silently drop that constraint. You can authorize dropping everything that depends on the column by adding`CASCADE`:

```
ALTER TABLE products DROP COLUMN description CASCADE;
```

See[Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)for a description of the general mechanism behind this.

### 5.5.3. Adding a Constraint

To add a constraint, the table constraint syntax is used. For example:

```
ALTER TABLE products ADD CHECK (name 
<
>
 '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

To add a not-null constraint, which cannot be written as a table constraint, use this syntax:

```
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

The constraint will be checked immediately, so the table data must satisfy the constraint before it can be added.

### 5.5.4. Removing a Constraint

To remove a constraint you need to know its name. If you gave it a name then that's easy. Otherwise the system assigned a generated name, which you need to find out. Thepsqlcommand`\d`\_`tablename`\_can be helpful here; other interfaces might also provide a way to inspect table details. Then the command is:

```
ALTER TABLE products DROP CONSTRAINT some_name;
```

\(If you are dealing with a generated constraint name like`$2`, don't forget that you'll need to double-quote it to make it a valid identifier.\)

As with dropping a column, you need to add`CASCADE`if you want to drop a constraint that something else depends on. An example is that a foreign key constraint depends on a unique or primary key constraint on the referenced column\(s\).

This works the same for all constraint types except not-null constraints. To drop a not null constraint use:

```
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

\(Recall that not-null constraints do not have names.\)

### 5.5.5. Changing a Column's Default Value

To set a new default for a column, use a command like:

```
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

Note that this doesn't affect any existing rows in the table, it just changes the default for future`INSERT`commands.

To remove any default value, use:

```
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

This is effectively the same as setting the default to null. As a consequence, it is not an error to drop a default where one hadn't been defined, because the default is implicitly the null value.

### 5.5.6. Changing a Column's Data Type

To convert a column to a different data type, use a command like:

```
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

This will succeed only if each existing entry in the column can be converted to the new type by an implicit cast. If a more complex conversion is needed, you can add a`USING`clause that specifies how to compute the new values from the old.

PostgreSQLwill attempt to convert the column's default value \(if any\) to the new type, as well as any constraints that involve the column. But these conversions might fail, or might produce surprising results. It's often best to drop any constraints on the column before altering its type, and then add back suitably modified constraints afterwards.

### 5.5.7. Renaming a Column

To rename a column:

```
ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

### 5.5.8. Renaming a Table

To rename a table:

```
ALTER TABLE products RENAME TO items;
```

---

[^1]: [PostgreSQL: Documentation: 10: 5.5. Modifying Tables](https://www.postgresql.org/docs/10/static/ddl-alter.html)

