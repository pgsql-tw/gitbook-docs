---
description: 版本：10
---

# REVOKE

REVOKE — 撤銷存取權限

### 語法

```text
REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTION function_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL FUNCTIONS IN SCHEMA schema_name [, ...] }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ ADMIN OPTION FOR ]
    role_name [, ...] FROM role_name [, ...]
    [ CASCADE | RESTRICT ]
```

### 說明

REVOKE 指令從一個或多個角色撤消先前授予的權限。關鍵字 PUBLIC 指的是所有角色的群組。

有關權限類型的含義，請參閱 [GRANT](grant.md) 指令的說明。

請注意，任何特定角色都將擁有直接授予它的權限聯集，授予其目前成員的任何角色的權限，以及授予 PUBLIC 的權限。因此，例如，從 PUBLIC 撤消 SELECT 權限並不一定意味著所有角色都失去了物件的 SELECT 權限：直接授予或透過其他角色授予權限的人仍然擁有它。同樣，如果 PUBLIC 或其他成員身份角色仍具有 SELECT 權限，則從用戶撤消 SELECT 可能無法阻止該使用者使用 SELECT。

如果指定了 GRANT OPTION FOR，則僅撤消該權限的 grant 選項，而不是該權限本身。否則，將撤消權限和授予選項。

如果使用者擁有具有 grant 選項的權限並已將其授予其他使用者，則這些其他使用者所擁有的權限稱為從屬權限。如果第一個使用者持有的權限或授予選項被撤銷且存在相關權限，則如果指定了 CASCADE，則也會撤銷這些相關權限；如果不是，撤銷動作將失敗。此遞迴撤消僅影響透過可跟踪到此 REVOKE 指令使用者的使用者授予權限鏈結。 因此，受影響的使用者可以有效地保留該權限，如果它也是透過其他使用者授予的。

撤消對資料表的權限時，相應的欄位權限（如果有）也會在資料表的每個欄位上自動撤消。另一方面，如果角色已被授予對資料表的權限，則從各個欄位撤消相同的權限將不起作用。

撤消角色中的成員資格時，GRANT OPTION 將被稱為 ADMIN OPTION，但行為類似。另請注意，此指令形式不允許使用 GROUP。

### 注意

使用 [psql](../client-applications/psql.md) 的 \dp 指令顯示在現有資料表和欄位上授予的權限。有關格式的訊息，請參閱 [GRANT](grant.md)。對於非資料表物件，還有其他 \dcommands 可以顯示其權限。

使用者只能撤消該使用者直接授予的權限。例如，如果使用者 A 已向使用者 B 授予了具有 grant 選項的權限，並且使用者 B 已將其授權給使用者 C，則使用者 A 無法直接從 C 撤銷該權限。相反地，使用者 A 可以撤銷使用者 B 的授予選項並使用 CASCADE 選項，以便從使用者 C 撤銷該權限。另一個例子，如果 A 和 B 都授予了與 C 相同的權限，A 可以撤銷他們自己的授權而不是 B 的授權，所以 C 仍然會有效地享有權限。

當物件的非擁有者嘗試 REVOKE 物件的權限時，如果使手者對該物件沒有任何權限，則該指令將會失敗。只要有一些權限可用，該指令就會繼續，但它將僅撤銷使用者具有授權選項的權限。如果沒有保留授權選項，REVOKE ALL PRIVILEGES 語句將發出警告消息，而如果未保留指令中特定指名的任何權限的授予選項，則其他語句將發出警告。 （原則上這些陳述也適用於物件擁有者，但由於擁有者始終被視為持有所有授權選項，因此此案例永遠不會發生。）

如果超級使用者選擇發出 GRANT 或 REVOKE 指令，則執行該指令時，就好像它是受影響物件的擁有者發出的一樣。由於所有權限最終都來自物件擁有者（可能間接透過授權鏈結），超級使用者可以撤銷所有權限，但這可能需要使用 CASCADE，如上所述。

REVOKE 也可以由不是受影響物件的擁有者角色完成，但是是擁有該物件的角色成員，或者是對該角色擁有 WITH GRANT OPTION 權限的角色成員。在這種情況下，執行命令就好像它是由實際擁有該物件的包含角色發出的，或者擁有 WITH GRANT OPTION 權限。例如，如果資料表 t1 由角色 g1 擁有，其中角色 u1 是成員，則 u1 可以撤銷 t1 上記錄為由 g1 授予的權限。這將包括由 u1 以及角色 g1 的其他成員進行的授權。

如果執行 REVOKE 的角色透過多個角色成員資格路徑間接保留權限，則未指定包含角色的角色將用於執行命令。在這種情況下，最佳做法是使用 SET ROLE 成為您要執行 REVOKE 的特定角色。如果不這樣做，可能會導致撤銷您預期權限之外的權限，或者根本未撤消任何權限。

### 範例

在資料表 film 上撤銷 public 的 INSERT 權限：

```text
REVOKE INSERT ON films FROM PUBLIC;
```

在檢視表 kinds 上撤消所有使用者 manuel 的權限：

```text
REVOKE ALL PRIVILEGES ON kinds FROM manuel;
```

請注意，這實際上意味著「撤銷由我所授予的所有權限」。

將使用者 joe 撤消角色 admins 的成員資格：

```text
REVOKE admins FROM joe;
```

### 相容性

[GRANT](grant.md) 指令的相容性說明同樣適用於 REVOKE。根據標準需要指定 RESTRICT 或 CASCADE，但 PostgreSQL 預設採用 RESTRICT。

### 參閱

[GRANT](grant.md)

