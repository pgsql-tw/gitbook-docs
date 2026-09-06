# ALTER POLICY

ALTER POLICY — 變更資料列等級的安全原則定義

## 語法

```
ALTER POLICY name ON table_name RENAME TO new_name

ALTER POLICY name ON table_name
    [ TO { role_name | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

## 描述

ALTER POLICY 用於變更現有資料列層級安全原則的定義。請注意，ALTER POLICY 只允許修改安全原則所適用的使用者們以及調整 USING 和 WITH CHECK 表示式。要更改安全原則的其他屬性，例如原則適用的指令，或者允許及限制原則，則必須刪除並重新建立安全原則。

要使用 ALTER POLICY 的話，你必須擁有該安全原則適用的資料表。

在 ALTER POLICY 的第二種形式中，指定的使用者角色列表、表示式和檢查表示式，將會被獨立替換。當其中一個子句被省略時，其原則相對應部分就不會改變。

## 參數

`name`

變更現有原則的名稱。

`table_name`

該原則所在的資料表名稱（可以加上 schema ）。

`new_name`

原則的新名稱。

`role_name`

原則所適用的使用者角色。可以同時指定多個角色。要將原則應用於所有角色，請使用 PUBLIC。

`using_expression`

原則的 USING 表示式。 有關詳細訊息，請參閱 [CREATE POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-policy.md)。

`check_expression`

原則的 WITH CHECK 表示式。有關詳細訊息，請參閱 [CREATE POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-policy.md)。

## 相容性

ALTER POLICY 是 PostgreSQL 所延伸支援的指令。

## 相關資訊

[CREATE POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-policy.md), [DROP POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/drop-policy.md)
