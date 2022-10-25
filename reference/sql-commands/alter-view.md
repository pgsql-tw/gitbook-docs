# ALTER VIEW

ALTER VIEW — 變更檢視表的定義

### 語法

```
ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name SET DEFAULT expression
ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name DROP DEFAULT
ALTER VIEW [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER VIEW [ IF EXISTS ] name RENAME TO new_name
ALTER VIEW [ IF EXISTS ] name SET SCHEMA new_schema
ALTER VIEW [ IF EXISTS ] name SET ( view_option_name [= view_option_value] [, ... ] )
ALTER VIEW [ IF EXISTS ] name RESET ( view_option_name [, ... ] )
```

### 語法

ALTER VIEW 變更檢視表的各種輔助屬性。（如果要修改檢視表的定義查詢，請使用 CREATE OR REPLACE VIEW。）

您必須擁有該檢視表才能使用 ALTER VIEW。要變更檢視表的綱要，您還必須具有新綱要的 CREATE 權限。要變更擁有者，您還必須是新擁有角色的直接或間接成員，並且該角色必須對檢視表的綱要具有 CREATE 權限。（這些限制強制要求變更擁有者不會透過移除和重新建立檢視表來執行任何操作。但是，超級使用者無論如何都可以變更任何檢視表的所有權。）

### 參數

_`name`_

現有檢視表的名稱（可選擇性加上綱要）。

`IF EXISTS`

如果檢視表不存在，請不要拋出錯誤。在這種情況下發出 NOTICE。

`SET`/`DROP DEFAULT`

這些語法設定或移除欄位的預設值。在為檢視表套用任何規則或觸發器之前，檢視表欄位的預設值將替換到引用的 INSERT 或 UPDATE 指令，其目標是檢視表。因此，檢視表的預設值優先於基礎關連的任何預設值。

_`new_owner`_

檢視表新擁有者的使用者名稱。

_`new_name`_

檢視表的新名稱。

_`new_schema`_

檢視表的新綱要。

`SET (`` `_`view_option_name`_ \[= _`view_option_value`_] \[, ... ] )\
`RESET (`` `_`view_option_name`_ \[, ... ] )

設定或重設檢視表選項。目前支援的選項包括：

`check_option` (`string`)

變更檢視表的檢查選項。值必須是 local 或 cascaded。

`security_barrier` (`boolean`)

變更檢視表的 security-barrier 屬性。該值必須是布林值，也就是 true 或 false。

### 注意

由於歷史因素，ALTER TABLE 也可以用於檢視表；但是檢視表能允許的 ALTER TABLE 的語法就等同於上面所列出的語法。

### 範例

要將檢視表 foo 重新命名為 bar：

```
ALTER VIEW foo RENAME TO bar;
```

要將預設欄位值加到可更新檢視表：

```
CREATE TABLE base_table (id int, ts timestamptz);
CREATE VIEW a_view AS SELECT * FROM base_table;
ALTER VIEW a_view ALTER COLUMN ts SET DEFAULT now();
INSERT INTO base_table(id) VALUES(1);  -- ts will receive a NULL
INSERT INTO a_view(id) VALUES(2);  -- ts will receive the current time
```

### 相容性

ALTER VIEW 是基於 SQL 標準的 PostgreSQL 延伸功能。

### 參閱

[CREATE VIEW](create-view.md), [DROP VIEW](drop-view.md)
