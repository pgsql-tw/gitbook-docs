---
description: 版本：11
---

# DROP LANGUAGE

DROP LANGUAGE — 移除程序語言

### 語法

```
DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

### 說明

DROP LANGUAGE 移除先前註冊的程序語言定義。您必須是超級使用者或語言的所有者才能使用 DROP LANGUAGE。

#### 注意

從 PostgreSQL 9.1 開始，大多數程序語言都被製作成「extension」，因此，應該使用 [DROP EXTENSION](drop-extension.md) 而不是 DROP LANGUAGE 來移除。

### 參數

`IF EXISTS`

如果該語言不存在，請不要拋出錯誤。而在這種情況下發出 NOTICE。

_`name`_

現有程序語言的名稱。為了相容性，名稱可以用單引號括起來。

`CASCADE`

自動移除相依於語言的物件（例如語言中的函數），以及相依於這些物件的所有物件（參閱[第 5.13 節](../../the-sql-language/ddl/dependency-tracking.md)）。

`RESTRICT`

如果任何物件相依於它，則拒絕移除。這是預設選項。

### 範例

此命令會移除程序語言 plsample：

```
DROP LANGUAGE plsample;
```

### 相容性

SQL 標準中沒有 DROP LANGUAGE 語句。

### 參閱

[ALTER LANGUAGE](alter-language.md), [CREATE LANGUAGE](create-language.md)
