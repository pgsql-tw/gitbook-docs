<a id="id-1.9.3.166.1"></a>

## REVOKE

REVOKE — 移除存取權限

<a id="id-1.9.3.166.2"></a>

## 語法

```

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } function_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SET | ALTER SYSTEM } [, ...] | ALL [ PRIVILEGES ] }
    ON PARAMETER configuration_parameter [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ { ADMIN | INHERIT | SET } OPTION FOR ]
    role_name [, ...] FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

where role_specification can be:

    [ GROUP ] role_name
  | PUBLIC
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

<a id="SQL-REVOKE-DESCRIPTION"></a>

## 說明

`REVOKE` 指令會從一個或多個角色，撤銷先前授予的權限。
關鍵字 `PUBLIC` 代表所有角色所隱含構成的群組。

關於各種權限類型的意義，請參閱 [`GRANT`](sql-grant.md) 指令的說明。

請注意，任一特定角色所擁有的權限，是直接授予給它本身的權限、授予給它目前所屬任何角色的權限，以及授予給
`PUBLIC` 的權限三者的總和。因此，舉例來說，從
`PUBLIC` 撤銷 `SELECT` 權限，不見得表示所有角色都失去了對該物件的
`SELECT` 權限：那些直接取得該權限、或透過其他角色取得該權限的角色，仍會保有此權限。同樣地，從某個使用者撤銷
`SELECT` 權限，也不見得能阻止該使用者使用
`SELECT`，如果 `PUBLIC` 或該使用者所屬的另一個角色仍擁有
`SELECT` 權限的話。

如果指定了 `GRANT OPTION FOR`，只有該權限的
授權選項會被撤銷，權限本身則不受影響。
否則，該權限與其授權選項都會一併被撤銷。

如果某位使用者持有附帶授權選項的權限，並已將其授予其他使用者，那麼這些其他使用者所持有的權限就稱為附屬權限。如果第一位使用者所持有的權限或授權選項被撤銷，且存在附屬權限，那麼在指定
`CASCADE` 的情況下，這些附屬權限也會一併被撤銷；如果未指定，
則撤銷操作會失敗。這種遞迴式的撤銷，只會影響透過一連串可追溯到本次
`REVOKE` 指令對象使用者的使用者鏈所授予的權限。
因此，如果受影響的使用者也透過其他使用者取得了該權限，他們實際上仍可能保有這項權限。

當撤銷某個資料表上的權限時，該資料表每個欄位上對應的欄位權限（如果有的話），也會被自動一併撤銷。
另一方面，如果某個角色是在資料表層級被授予權限的，那麼從個別欄位撤銷相同的權限則不會產生任何效果。

當撤銷角色成員資格時，`GRANT OPTION` 會改稱為
`ADMIN OPTION`，但行為與之類似。
請注意，在 PostgreSQL 16 之前的版本中，
角色成員資格授予並不會追蹤附屬權限，因此
`CASCADE` 對角色成員資格沒有任何效果。
現在已不再是這樣。
另請注意，這種形式的指令並不
允許在 *`role_specification`* 中使用贅詞
`GROUP`。

正如可以從既有的角色授予中移除 `ADMIN OPTION`，
同樣也可以撤銷 `INHERIT OPTION`
或 `SET OPTION`。這等同於將對應選項的值
設為 `FALSE`。

<a id="SQL-REVOKE-NOTES"></a>

## 注意

使用者只能撤銷由自己直接授予的權限。舉例來說，如果使用者
A 已將某項附帶授權選項的權限授予使用者 B，而使用者 B
又將其授予了使用者 C，那麼使用者 A 就無法直接從
C 撤銷該權限。
反之，使用者 A 可以從使用者 B 撤銷其授權選項，並搭配使用
`CASCADE` 選項，讓該權限也連帶從使用者
C 撤銷。再舉一個例子，如果 A 與 B 都曾將相同的權限授予
C，A 可以撤銷自己的授予，但無法撤銷 B 的授予，因此
C 仍會實際保有該權限。

當非物件擁有者嘗試對某個物件執行 `REVOKE` 時，如果該使用者對此物件完全沒有任何權限，指令就會直接失敗。只要存在某些可用的權限，指令就會繼續進行，但只會撤銷該使用者持有授權選項的那些權限。`REVOKE ALL
PRIVILEGES` 這種形式，如果未持有任何授權選項，會發出警告訊息；其他形式則會在指令中特別指名的任一權限未持有授權選項時，發出警告。
（原則上這些說明對物件擁有者同樣適用，但由於擁有者一律被視為持有所有授權選項，
這種情況實際上不會發生。）

如果超級使用者選擇發出 `GRANT` 或 `REVOKE`
指令，該指令的執行方式，就如同它是由
受影響物件的擁有者所發出的一樣。（由於角色並沒有擁有者，因此在
`GRANT` 角色成員資格的情況下，該指令的執行方式，
就如同它是由啟動用超級使用者所發出的一樣。）
由於所有權限最終都來自物件的擁有者（可能是透過一連串的授權選項間接取得），
因此超級使用者是有可能撤銷所有權限的，但如前所述，這可能需要搭配使用
`CASCADE`。

`REVOKE` 也可以由並非受影響物件擁有者、
但屬於擁有該物件之角色成員，或屬於在該物件上具備
`WITH GRANT OPTION` 權限之角色成員的角色來執行。在這種情況下，
該指令的執行方式，就如同它是由實際擁有該物件、或持有
`WITH GRANT OPTION` 權限的那個上層角色所發出的一樣。舉例來說，如果資料表
`t1` 由角色 `g1` 擁有，而角色
`u1` 是其成員，那麼 `u1` 就可以撤銷記錄為由
`g1` 授予的、關於 `t1` 的權限。
這會包含由 `u1` 本身，以及角色 `g1`
其他成員所做的授予。

如果執行 `REVOKE` 的角色是透過多重角色成員資格路徑間接持有權限的，
那麼系統會使用哪一個上層角色來執行該指令，是未定義的。在這種情況下，
最佳做法是使用 `SET ROLE` 切換為你想要以其身分執行
`REVOKE` 的特定角色。若不這麼做，可能會導致
撤銷了非預期的權限，或是完全沒有撤銷任何權限。

關於特定權限類型的更多資訊，以及如何檢視物件的權限，請參閱[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。

<a id="SQL-REVOKE-EXAMPLES"></a>

## 範例

撤銷公眾對資料表
`films` 的插入權限：

```

REVOKE INSERT ON films FROM PUBLIC;
```

撤銷使用者 `manuel` 對檢視表
`kinds` 的所有權限：

```

REVOKE ALL PRIVILEGES ON kinds FROM manuel;
```

請注意，這實際上代表「撤銷我所授予的所有權限」。

撤銷使用者 `joe` 對角色 `admins` 的成員資格：

```

REVOKE admins FROM joe;
```

<a id="SQL-REVOKE-COMPATIBILITY"></a>

## 相容性

[`GRANT`](sql-grant.md) 指令的相容性說明，
同樣適用於 `REVOKE`。
標準要求必須使用 `RESTRICT` 或 `CASCADE`
關鍵字，但 PostgreSQL
預設會採用 `RESTRICT`。

<a id="id-1.9.3.166.9"></a>

## 另請參閱

[GRANT](sql-grant.md), [ALTER DEFAULT PRIVILEGES](sql-alterdefaultprivileges.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-revoke.html)（原文版本：18.6；核對日期：2026-09-28）
