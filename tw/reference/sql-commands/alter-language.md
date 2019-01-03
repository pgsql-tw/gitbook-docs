---
description: 版本：11
---

# ALTER LANGUAGE

ALTER LANGUAGE — 變更程序語言的宣告

### 語法

```text
ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
```

### 說明

ALTER LANGUAGE 變更程序語言的宣告。唯一的功能是將語言重新命名或分配新的所有者。您必須是該語言所有者或超級使用者才能使用 ALTER LANGUAGE。

### 參數

_`name`_

語言名稱

_`new_name`_

語言的新名稱

_`new_owner`_

語言的新所有者e

### 相容性

SQL 標準中沒有 ALTER LANGUAGE 語句。

### 參閱

[CREATE LANGUAGE](create-language.md), [DROP LANGUAGE](drop-language.md)  


