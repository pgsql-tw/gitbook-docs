---
description: 版本：10
---

# TRUNCATE

TRUNCATE — 清空一個資料表或一堆資料表

### 語法

```text
TRUNCATE [ TABLE ] [ ONLY ] name [ * ] [, ... ]
    [ RESTART IDENTITY | CONTINUE IDENTITY ] [ CASCADE | RESTRICT ]
```

### 說明

TRUNCATE 快速移除一堆資料表中的所有資料列。它與每個資料表上的無差別 DELETE 具有相同的效果，但由於它實際上不掃描資料表，因此速度更快。此外，它會立即回收磁碟空間，而不是需要後續的 VACUUM 操作。這對大型資料表非常有用。

### 參數

_`name`_

要清空的資料表名稱（可選用綱要名稱）。如果在資料表名稱之前指定了 ONLY，則僅清空此資料表。如果未指定 ONLY，則會清空此表及其所有後代資料表（如果有的話）。也可以在資料表名稱後指定 \* 以明確指示包含後代資料表。

`RESTART IDENTITY`

自動重置清空資料表的欄位所擁有的序列。

`CONTINUE IDENTITY`

不要變更序列的值。這是預設值。

`CASCADE`

自動清空所有對任何對此資料表具有外部鍵引用的資料表，或者由於 CASCADE 而加入群組的資料表。

`RESTRICT`

如果任何資料表具有未在命令中列出的資料表外部鍵引用，則拒絕清空。這是預設值。

### Notes

You must have the `TRUNCATE` privilege on a table to truncate it.

`TRUNCATE` acquires an `ACCESS EXCLUSIVE` lock on each table it operates on, which blocks all other concurrent operations on the table. When `RESTART IDENTITY` is specified, any sequences that are to be restarted are likewise locked exclusively. If concurrent access to a table is required, then the `DELETE` command should be used instead.

`TRUNCATE` cannot be used on a table that has foreign-key references from other tables, unless all such tables are also truncated in the same command. Checking validity in such cases would require table scans, and the whole point is not to do one. The `CASCADE` option can be used to automatically include all dependent tables — but be very careful when using this option, or else you might lose data you did not intend to!

`TRUNCATE` will not fire any `ON DELETE` triggers that might exist for the tables. But it will fire `ON TRUNCATE` triggers. If `ON TRUNCATE` triggers are defined for any of the tables, then all `BEFORE TRUNCATE` triggers are fired before any truncation happens, and all `AFTER TRUNCATE` triggers are fired after the last truncation is performed and any sequences are reset. The triggers will fire in the order that the tables are to be processed \(first those listed in the command, and then any that were added due to cascading\).

`TRUNCATE` is not MVCC-safe. After truncation, the table will appear empty to concurrent transactions, if they are using a snapshot taken before the truncation occurred. See [Section 13.5](https://www.postgresql.org/docs/10/static/mvcc-caveats.html) for more details.

`TRUNCATE` is transaction-safe with respect to the data in the tables: the truncation will be safely rolled back if the surrounding transaction does not commit.

When `RESTART IDENTITY` is specified, the implied `ALTER SEQUENCE RESTART` operations are also done transactionally; that is, they will be rolled back if the surrounding transaction does not commit. This is unlike the normal behavior of `ALTER SEQUENCE RESTART`. Be aware that if any additional sequence operations are done on the restarted sequences before the transaction rolls back, the effects of these operations on the sequences will be rolled back, but not their effects on `currval()`; that is, after the transaction `currval()` will continue to reflect the last sequence value obtained inside the failed transaction, even though the sequence itself may no longer be consistent with that. This is similar to the usual behavior of `currval()` after a failed transaction.

`TRUNCATE` is not currently supported for foreign tables. This implies that if a specified table has any descendant tables that are foreign, the command will fail.

### 範例

清空資料表 bigtable 和 fattable：

```text
TRUNCATE bigtable, fattable;
```

同樣，再加上重置任何相關的序列産生器：

```text
TRUNCATE bigtable, fattable RESTART IDENTITY;
```

清空資料表 othertable，串聯清空任何透過外部鍵引用的其他資料表：

```text
TRUNCATE othertable CASCADE;
```

### 相容性

SQL:2008 標準有一個 TRUNCATE 指令，其語法為 TRUNCATE TABLE tablename。子句 CONTINUE IDENTITY / RESTART IDENTITY 也出現在該標準中，但具有略微不同但類似的意義。此指令的某些平行作業行為是由實作定義的，因此應考慮上述註釋，並在必要時與其他實作進行比較。

### 參閱

[DELETE](delete.md)

