<a id="SQL-ALTERDEFAULTPRIVILEGES"></a><a id="id-1.9.3.8.1"></a>

## ALTER DEFAULT PRIVILEGES

ALTER DEFAULT PRIVILEGES — 定義預設存取權限

<a id="id-1.9.3.8.4"></a>

## 語法

```

ALTER DEFAULT PRIVILEGES
    [ FOR { ROLE | USER } target_role [, ...] ]
    [ IN SCHEMA schema_name [, ...] ]
    abbreviated_grant_or_revoke

where abbreviated_grant_or_revoke is one of:

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
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

GRANT { { USAGE | CREATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECTS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
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
    { { USAGE | CREATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECTS
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]
```

<a id="SQL-ALTERDEFAULTPRIVILEGES-DESCRIPTION"></a>

## 說明

`ALTER DEFAULT PRIVILEGES` 讓你可以設定將套用於日後所建立之物件的權限。（它不會影響已指派給既有物件的權限。）權限可以全域設定（亦即，套用於目前資料庫中建立的所有物件），也可以只套用於在指定綱要中建立的物件。

雖然你可以變更自己的預設權限，以及你所屬角色的預設權限，但在建立物件時，新物件的權限只會受到目前角色之預設權限的影響，而不會從目前角色所屬的任何角色繼承。

如[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)所述，任何物件類型的預設權限通常會將所有可授予的權限授予物件擁有者，也可能將某些權限授予 `PUBLIC`。不過，可以透過使用 `ALTER DEFAULT PRIVILEGES` 修改全域預設權限來變更此行為。

目前只能修改綱要、資料表（包括檢視表與外部資料表）、序列、函式、型別（包括網域）以及大型物件的權限。就此命令而言，函式包括彙總函式與程序。在此命令中，`FUNCTIONS` 與 `ROUTINES` 這兩個字是等價的。（今後建議使用 `ROUTINES`，作為合稱函式與程序的標準用語。在較早的 PostgreSQL 版本中，只允許使用 `FUNCTIONS` 這個字。無法分別為函式與程序設定預設權限。）

依綱要指定的預設權限，會加到該物件類型既有的全域預設權限之上。這表示若權限是全域授予的（無論是預設如此，或是依據先前一個未指定綱要的 `ALTER
DEFAULT PRIVILEGES` 命令），你就無法依綱要撤銷這些權限。依綱要執行的 `REVOKE` 只能用來撤回先前依綱要執行之 `GRANT` 的效果。

<a id="id-1.9.3.8.5.7"></a>

### 參數

*`target_role`*
:   變更由 *`target_role`* 所建立之物件的預設權限；若未指定，則為目前角色。

*`schema_name`*
:   現有綱要的名稱。若有指定，則會修改日後在該綱要中建立之物件的預設權限。若省略 `IN SCHEMA`，則會修改全域預設權限。為綱要與大型物件設定權限時，不允許使用 `IN SCHEMA`，因為綱要不能巢狀，而大型物件不屬於任何綱要。

*`role_name`*
:   要授予或撤銷其權限之現有角色的名稱。此參數以及 *`abbreviated_grant_or_revoke`* 中的所有其他參數，其作用皆如 [GRANT](sql-grant.md) 或 [REVOKE](sql-revoke.md) 中所述，差別在於這裡是為一整類物件設定權限，而不是為特定的具名物件設定權限。

<a id="SQL-ALTERDEFAULTPRIVILEGES-NOTES"></a>

## 注意事項

使用 [psql](../reference-client/app-psql.md) 的 `\ddp` 命令可以取得現有預設權限指派的資訊。權限顯示的意義與[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)中對 `\dp` 的說明相同。

若你想要移除一個預設權限已被修改過的角色，就必須撤回其預設權限的變更，或使用 `DROP OWNED BY` 清除該角色的預設權限項目。

<a id="SQL-ALTERDEFAULTPRIVILEGES-EXAMPLES"></a>

## 範例

對於你日後在綱要 `myschema` 中建立的所有資料表（以及檢視表），將 SELECT 權限授予所有人，並允許角色 `webuser` 也能對它們執行 INSERT：

```

ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT SELECT ON TABLES TO PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT INSERT ON TABLES TO webuser;
```

撤回上述設定，讓日後建立的資料表不會具有超出一般情況的權限：

```

ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE SELECT ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE INSERT ON TABLES FROM webuser;
```

對於角色 `admin` 日後建立的所有函式，移除通常會授予函式的公開 EXECUTE 權限：

```

ALTER DEFAULT PRIVILEGES FOR ROLE admin REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

不過請注意，你*無法*使用限定於單一綱要的命令達到這個效果。除非是在撤回相符的 `GRANT`，否則下列命令沒有作用：

```

ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

這是因為依綱要設定的預設權限只能在全域設定之上增加權限，而不能移除全域設定所授予的權限。

<a id="id-1.9.3.8.8"></a>

## 相容性

SQL 標準中沒有 `ALTER DEFAULT PRIVILEGES` 陳述式。

<a id="id-1.9.3.8.9"></a>

## 另請參閱

[GRANT](sql-grant.md), [REVOKE](sql-revoke.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)（原文版本：18.6；核對日期：2026-10-05）
