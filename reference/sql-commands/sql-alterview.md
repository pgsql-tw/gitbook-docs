<a id="SQL-ALTERVIEW"></a><a id="id-1.9.3.45.1"></a>

## ALTER VIEW

ALTER VIEW — 變更檢視表的定義

<a id="id-1.9.3.45.4"></a>

## 語法

```

ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name SET DEFAULT expression
ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name DROP DEFAULT
ALTER VIEW [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER VIEW [ IF EXISTS ] name RENAME [ COLUMN ] column_name TO new_column_name
ALTER VIEW [ IF EXISTS ] name RENAME TO new_name
ALTER VIEW [ IF EXISTS ] name SET SCHEMA new_schema
ALTER VIEW [ IF EXISTS ] name SET ( view_option_name [= view_option_value] [, ... ] )
ALTER VIEW [ IF EXISTS ] name RESET ( view_option_name [, ... ] )
```

<a id="id-1.9.3.45.5"></a>

## 說明

`ALTER VIEW` 會變更檢視表的各種輔助屬性。（若你想修改檢視表的定義查詢，請使用 `CREATE OR REPLACE VIEW`。）

你必須擁有該檢視表，才能使用 `ALTER VIEW`。若要變更檢視表的綱要，你還必須擁有新綱要的 `CREATE` 權限。若要變更擁有者，你必須能對新的擁有者角色執行 `SET ROLE`，且該角色必須擁有該檢視表所在綱要的 `CREATE` 權限。（這些限制確保變更擁有者不會做到任何你無法藉由移除並重新建立檢視表而做到的事。不過，超級使用者無論如何都可以變更任何檢視表的擁有權。）

<a id="id-1.9.3.45.6"></a>

## 參數

*`name`*
:   現有檢視表的名稱（可選擇以綱要限定）。

*`column_name`*
:   現有欄位的名稱。

*`new_column_name`*
:   現有欄位的新名稱。

`IF EXISTS`
:   檢視表不存在時不擲出錯誤；此情況會發出 notice。

`SET`/`DROP DEFAULT`
:   這些形式會設定或移除欄位的預設值。檢視表欄位的預設值，會在套用該檢視表的任何規則或觸發程序之前，代入任何以該檢視表為目標的 `INSERT` 或 `UPDATE` 命令中。因此，檢視表的預設值會優先於底層關聯中的任何預設值。

*`new_owner`*
:   檢視表新擁有者的使用者名稱。

*`new_name`*
:   檢視表的新名稱。

*`new_schema`*
:   檢視表的新綱要。

`SET ( view_option_name [= view_option_value] [, ... ] )`<br>`RESET ( view_option_name [, ... ] )`
:   設定或重設檢視表選項。目前支援的選項有：

    `check_option` (`enum`)
    :   變更檢視表的檢查選項。值必須是 `local` 或 `cascaded`。

    `security_barrier` (`boolean`)
    :   變更檢視表的安全屏障（security-barrier）屬性。值必須是布林值，例如 `true` 或 `false`。

    `security_invoker` (`boolean`)
    :   變更檢視表的呼叫者權限檢查（security-invoker）屬性。值必須是布林值，例如 `true` 或 `false`。

<a id="id-1.9.3.45.7"></a>

## 注意事項

基於歷史因素，`ALTER TABLE` 也可以用於檢視表；但允許用於檢視表的 `ALTER TABLE` 變體，只有與上面所示形式等效的那些。

<a id="id-1.9.3.45.8"></a>

## 範例

將檢視表 `foo` 重新命名為 `bar`：

```

ALTER VIEW foo RENAME TO bar;
```

為可更新的檢視表附加欄位預設值：

```

CREATE TABLE base_table (id int, ts timestamptz);
CREATE VIEW a_view AS SELECT * FROM base_table;
ALTER VIEW a_view ALTER COLUMN ts SET DEFAULT now();
INSERT INTO base_table(id) VALUES(1);  -- ts will receive a NULL
INSERT INTO a_view(id) VALUES(2);  -- ts will receive the current time
```

<a id="id-1.9.3.45.9"></a>

## 相容性

`ALTER VIEW` 是 PostgreSQL 對 SQL 標準的擴充。

<a id="id-1.9.3.45.10"></a>

## 另請參閱

[CREATE VIEW](sql-createview.md), [DROP VIEW](sql-dropview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterview.html)（原文版本：18.6；核對日期：2026-10-04）
