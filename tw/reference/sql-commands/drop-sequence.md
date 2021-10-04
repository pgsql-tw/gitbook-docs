# DROP SEQUENCE

DROP SEQUENCE — remove a sequence

### Synopsis

```text
DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### Description

`DROP SEQUENCE` removes sequence number generators. A sequence can only be dropped by its owner or a superuser.

### Parameters

`IF EXISTS`

Do not throw an error if the sequence does not exist. A notice is issued in this case.

_`name`_

The name \(optionally schema-qualified\) of a sequence.

`CASCADE`

Automatically drop objects that depend on the sequence, and in turn all objects that depend on those objects \(see [Section 5.14](https://www.postgresql.org/docs/13/ddl-depend.html)\).`RESTRICT`

Refuse to drop the sequence if any objects depend on it. This is the default.

### 範例

要移除序列物件：

```text
DROP SEQUENCE serial;
```

### 相容性

DROP SEQUENCE 符合 SQL 標準，但標準僅允許每個指令移除一個序列，包含除了 IF EXISTS 選項（它是 PostgreSQL 加入的功能）外的部份。

### 參閱

[CREATE SEQUENCE](create-sequence.md), [ALTER SEQUENCE](alter-sequence.md)  


