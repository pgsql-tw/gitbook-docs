# ALTER DEFAULT PRIVILEGES

ALTER DEFAULT PRIVILEGES — 設定預設的存取權限

### 語法

```text
ALTER DEFAULT PRIVILEGES
    [ FOR { ROLE | USER } target_role [, ...] ]
    [ IN SCHEMA schema_name [, ...] ]
    abbreviated_grant_or_revoke

where abbreviated_grant_or_revoke is one of:

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | CREATE | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | CREATE | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]
```

### 說明

ALTER DEFAULT PRIVILEGES 使您可以設定將套用於未來建立物件的權限。（它不會影響指派給已存在物件的權限。）目前，只能變更改綱要、資料表（包括檢視表和外部資料表）、序列、函數和型別（包括 domain）的權限。對於此命令，函數包括彙總函數和程序函數。在這個命令中，單詞 FUNCTIONS 和 ROUTINES 是等效的。（ROUTINES 優先作為函數和程序的標準術語。在早期的 PostgreSQL 版本中，只允許使用單詞 FUNCTIONS。不可能單獨為函數和程序設定預設權限。）

您只能為將由您自己或您所屬角色建立的物件變更預設權限。可以全域設定權限（意即，對於在目前資料庫中建立的所有物件），或僅為在指定綱要中建立的物件設定權限。每個綱要指定的預設權限將指派到特定物件類型的全域預設權限。

如 [GRANT](grant.md) 中所述，任何物件類型的預設權限通常都會從物件所有者授予所有可授予的權限，並且還可以從 PUBLIC 授予某些權限。但是，可以透過使用 ALTER DEFAULT PRIVILEGES 變更全域預設權限來變更此行為。

#### 參數

_`target_role`_

目前角色所屬的現有角色的名稱。 如果省略 FOR ROLE，則假設為目前角色。

_`schema_name`_

現有綱要的名稱。如果有指定的話，則會為稍後在該綱要中建立的物件變更預設權限。如果省略 IN SCHEMA，則變更全域的預設權限。使用 ON SCHEMAS 時不允許使用 IN SCHEMA，因為無法嵌套綱要。

_`role_name`_

授予或撤消權限的現有角色名稱。此參數以及 abbreviated\_grant\_or\_revoke 中的所有其他參數的行為與 [GRANT](grant.md) 或 [REVOKE](revoke.md) 中所述相同，只是一個是為整個物件類別而不是特定的命名物件設定權限。

### 注意

使用 [psql ](../client-applications/psql.md)的 \ddp 指令獲取有關現有預設權限指派的資訊。權限的含義與 [GRANT](grant.md) 中 \dp 的解釋相同。

如果您希望移除已變更預設權限的角色，則必須撤消其預設權限的變更，或使用 DROP OWNED BY 刪除該角色的預設權限項目。

### 範例

為隨後在綱要 myschema 中所建立的所有資料表（和檢視表）授予每個人 SELECT 權限，並使角色 webuser 具備 INSERT 權限：

```text
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT SELECT ON TABLES TO PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT INSERT ON TABLES TO webuser;
```

撤消上述內容，以便後續建立的資料表不會有更大於正常的權限：

```text
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE SELECT ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE INSERT ON TABLES FROM webuser;
```

對於角色 admin 隨後建立的所有函數，移除一般會在函數上授予給 PUBLIC 的 EXECUTE 權限：

```text
ALTER DEFAULT PRIVILEGES FOR ROLE admin REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

### 相容性

SQL標準中沒有 ALTER DEFAULT PRIVILEGES 語句。

### 參閱

[GRANT](grant.md), [REVOKE](revoke.md)

