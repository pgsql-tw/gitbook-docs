<a id="id-1.9.3.150.1"></a>

## GRANT

GRANT — 定義存取權限

<a id="id-1.9.3.150.2"></a>

## 語法

```

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } routine_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SET | ALTER SYSTEM } [, ... ] | ALL [ PRIVILEGES ] }
    ON PARAMETER configuration_parameter [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT role_name [, ...] TO role_specification [, ...]
    [ WITH { ADMIN | INHERIT | SET } { OPTION | TRUE | FALSE } ]
    [ GRANTED BY role_specification ]

where role_specification can be:

    [ GROUP ] role_name
  | PUBLIC
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

<a id="SQL-GRANT-DESCRIPTION"></a>

## 說明

`GRANT` 指令有兩種基本形式：一種是針對資料庫物件（資料表、欄位、檢視表、外部資料表、序列、資料庫、外部資料包裝器、外部伺服器、函式、程序、程序語言、大型物件、組態參數、綱要、表空間或型別）授予權限，另一種則是授予角色的成員資格。這兩種形式在許多方面相似，但差異足以分開說明。

<a id="SQL-GRANT-DESCRIPTION-OBJECTS"></a>

### 資料庫物件上的 GRANT

`GRANT` 指令的這種形式，會將資料庫物件上的特定權限授予一個或多個角色。這些權限會加到既有已授予的權限之上（如果有的話）。

關鍵字 `PUBLIC` 表示要將權限授予所有角色，包括日後才建立的角色。`PUBLIC` 可以看成是一個隱含定義、永遠包含所有角色的群組。任何特定角色所擁有的權限，是直接授予它本身的權限、授予它目前所屬任一角色的權限，以及授予 `PUBLIC` 的權限之總和。

若指定了 `WITH GRANT OPTION`，取得該權限的人可以再將此權限授予其他人。若沒有授予選項，取得者就無法這麼做。授予選項無法授予給 `PUBLIC`。

若指定了 `GRANTED BY`，所指定的授予者必須是目前使用者。這個子句目前僅為了符合 SQL 相容性才存在。

不需要對物件的擁有者（通常是建立該物件的使用者）授予權限，因為擁有者預設就擁有所有權限。（不過，擁有者可以選擇撤銷自己的部分權限以策安全。）

刪除物件或以任何方式變更其定義的權利，並不視為可授予的權限；這是擁有者所固有的，無法授予或撤銷。（不過，透過授予或撤銷擁有該物件之角色的成員資格，可以達到類似的效果；請參閱下文。）擁有者也隱含擁有該物件的所有授予選項。

可能的權限有：

`SELECT`<br>`INSERT`<br>`UPDATE`<br>`DELETE`<br>`TRUNCATE`<br>`REFERENCES`<br>`TRIGGER`<br>`CREATE`<br>`CONNECT`<br>`TEMPORARY`<br>`EXECUTE`<br>`USAGE`<br>`SET`<br>`ALTER SYSTEM`<br>`MAINTAIN`
:   特定類型的權限，定義於[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。

`TEMP`
:   `TEMPORARY` 的替代拼法。

`ALL PRIVILEGES`
:   授予該物件類型所有可用的權限。在 PostgreSQL 中，`PRIVILEGES` 關鍵字是選用的，不過嚴格的 SQL 標準要求必須使用。

`FUNCTION` 語法適用於一般函式、聚合函式與視窗函式，但不適用於程序；程序請使用 `PROCEDURE`。或者，也可以使用 `ROUTINE` 來泛指函式、聚合函式、視窗函式或程序，而不論其確切類型。

此外，也可以對一個或多個綱要中所有相同類型的物件授予權限。這項功能目前僅支援資料表、序列、函式與程序。`ALL TABLES` 也會影響檢視表與外部資料表，就像針對特定物件的 `GRANT` 指令一樣。`ALL FUNCTIONS` 也會影響聚合函式與視窗函式，但不含程序，同樣就像針對特定物件的 `GRANT` 指令一樣。若要包含程序，請使用 `ALL ROUTINES`。

<a id="SQL-GRANT-DESCRIPTION-ROLES"></a>

### 角色上的 GRANT

`GRANT` 指令的這種形式，會將某個角色的成員資格授予一個或多個其他角色，並可修改成員資格選項 `SET`、`INHERIT` 與 `ADMIN`；詳情請參閱[第 21.3 節](../../server-administration/user-manag/role-membership.md)。角色的成員資格之所以重要，是因為它可能讓該角色的每個成員取得授予該角色的權限，也可能讓成員取得變更該角色本身的能力。不過，實際被授予的權限取決於與該次授予相關聯的選項。若要修改既有成員資格的選項，只要以更新後的選項值再次指定該成員資格即可。

以下描述的每個選項都可以設為 `TRUE` 或 `FALSE`。關鍵字 `OPTION` 可作為 `TRUE` 的同義字，因此 `WITH ADMIN OPTION` 等同於 `WITH ADMIN TRUE`。變更既有成員資格時，若省略某個選項，會保留其目前的值。

`ADMIN` 選項讓該成員可以再將該角色的成員資格授予其他人，也可以撤銷該角色的成員資格。若沒有管理選項，一般使用者無法這麼做。角色本身並不會被視為對自己擁有 `WITH ADMIN OPTION`。資料庫超級使用者可以將任何角色的成員資格授予任何人，或是從任何人撤銷。此選項預設為 `FALSE`。

`INHERIT` 選項控制新成員資格的繼承狀態；繼承的詳情請參閱[第 21.3 節](../../server-administration/user-manag/role-membership.md)。若設為 `TRUE`，會讓新成員繼承被授予角色的權限。若設為 `FALSE`，新成員則不會繼承。若在建立新的角色成員資格時未指定，預設會採用新成員本身的繼承屬性。

`SET` 選項若設為 `TRUE`，會讓該成員可以使用 [`SET ROLE`](sql-set-role.md) 指令切換為被授予的角色。若某角色是透過間接方式成為另一個角色的成員，則只有在整條授予鏈上每一步都具備 `SET TRUE` 時，它才能使用 `SET ROLE` 切換為該角色。此選項預設為 `TRUE`。

若要建立由其他角色擁有的物件，或是將既有物件的擁有權轉移給其他角色，你必須具備 `SET ROLE` 成該角色的能力；否則諸如 `ALTER ... OWNER TO` 或 `CREATE DATABASE ... OWNER` 之類的指令都會失敗。不過，繼承了某角色權限、但不具備 `SET ROLE` 成該角色能力的使用者，仍可能藉由操縱該角色所擁有的既有物件來取得該角色的完整存取權（例如，重新定義既有函式使其如同特洛伊木馬般運作）。因此，若某角色的權限要被繼承、但不應該可以透過 `SET ROLE` 存取，就不應該讓該角色擁有任何 SQL 物件。

若指定了 `GRANTED BY`，該次授予會被記錄為由指定的角色所執行。使用者只有在擁有該角色的權限時，才能將授予歸屬於該角色。被記錄為授予者的角色，除非是啟動超級使用者，否則必須對目標角色具備 `ADMIN OPTION`。當某次授予被記錄為授予者非啟動超級使用者時，此授予會依賴授予者持續對該角色擁有 `ADMIN OPTION`；因此，若 `ADMIN OPTION` 遭撤銷，依賴它的授予也必須一併撤銷。

與權限的情況不同，角色的成員資格無法授予給 `PUBLIC`。另請注意，這種形式的指令不允許在 *`role_specification`* 中使用贅字 `GROUP`。

<a id="SQL-GRANT-NOTES"></a>

## 注意事項

[`REVOKE`](sql-revoke.md) 指令用於撤銷存取權限。

自 PostgreSQL 8.1 起，使用者與群組的概念已統一為單一種類的實體，稱為角色。因此，不再需要使用關鍵字 `GROUP` 來標明被授予者是使用者還是群組。指令中仍可使用 `GROUP`，但它只是個贅字。

若使用者對某個欄位或其所屬整個資料表擁有該項權限，即可對該欄位執行 `SELECT`、`INSERT` 等操作。在資料表層級授予權限、再針對單一欄位撤銷該權限，並不會達到預期的效果：資料表層級的授予不會受到欄位層級操作的影響。

當物件的非擁有者嘗試對該物件執行 `GRANT` 時，若該使用者對該物件完全沒有任何權限，指令會直接失敗。只要有任何權限可用，指令就會繼續執行，但只會授予該使用者擁有授予選項的那些權限。若未持有任何授予選項，`GRANT ALL PRIVILEGES` 形式會發出警告訊息；至於其他形式，若指令中明確指名的權限中有任何一項未持有授予選項，也會發出警告。（原則上這些說明也適用於物件擁有者，但由於擁有者一律被視為持有所有授予選項，這類情況永遠不會發生。）

值得注意的是，資料庫超級使用者可以存取所有物件，而不受物件權限設定的限制。這類似於 Unix 系統中 `root` 的權限。和 `root` 一樣，除非絕對必要，否則不宜以超級使用者身分操作。

若超級使用者選擇發出 `GRANT` 或 `REVOKE` 指令，該指令會被視為由受影響物件的擁有者所發出。具體來說，透過這類指令授予的權限，會顯示為由物件擁有者所授予。（就角色成員資格而言，該成員資格會顯示為由啟動超級使用者所授予。）

`GRANT` 與 `REVOKE` 也可以由某個角色執行——只要該角色本身並非受影響物件的擁有者，但屬於擁有該物件之角色的成員，或是屬於對該物件持有 `WITH GRANT OPTION` 權限之角色的成員。在此情況下，該權限會被記錄為由實際擁有該物件、或實際持有 `WITH GRANT OPTION` 權限的角色所授予。舉例來說，若資料表 `t1` 由角色 `g1` 擁有，而角色 `u1` 是該角色的成員，那麼 `u1` 可以將 `t1` 上的權限授予 `u2`，但這些權限會顯示為由 `g1` 直接授予。角色 `g1` 的其他任何成員之後都可以撤銷這些權限。

若執行 `GRANT` 的角色是透過一條以上的角色成員資格路徑間接持有所需權限，則會由哪個包含角色被記錄為執行該次授予是不確定的。在這類情況下，最佳做法是使用 `SET ROLE` 切換為你想要以其身分執行 `GRANT` 的特定角色。

對資料表授予權限，並不會自動將權限延伸到該資料表所使用的任何序列，包括與 `SERIAL` 欄位相關聯的序列。序列上的權限必須另外設定。

關於特定權限類型的更多資訊，以及如何檢視物件的權限，請參閱[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。

<a id="SQL-GRANT-EXAMPLES"></a>

## 範例

將資料表 `films` 的 insert 權限授予所有使用者：

```

GRANT INSERT ON films TO PUBLIC;
```

將檢視表 `kinds` 的所有可用權限授予使用者 `manuel`：

```

GRANT ALL PRIVILEGES ON kinds TO manuel;
```

請注意，若由超級使用者或 `kinds` 的擁有者執行上述指令，確實會授予所有權限；但若由其他人執行，則只會授予該使用者擁有授予選項的那些權限。

將角色 `admins` 的成員資格授予使用者 `joe`：

```

GRANT admins TO joe;
```

<a id="SQL-GRANT-COMPATIBILITY"></a>

## 相容性

根據 SQL 標準，`ALL PRIVILEGES` 中的 `PRIVILEGES` 關鍵字是必要的。SQL 標準不支援在單一指令中對多個物件設定權限。

PostgreSQL 允許物件擁有者撤銷自己一般的權限：例如，資料表擁有者可以撤銷自己的 `INSERT`、`UPDATE`、`DELETE` 與 `TRUNCATE` 權限，讓該資料表對自己而言變成唯讀。這在 SQL 標準中是不可能的。原因在於 PostgreSQL 將擁有者的權限視為由擁有者授予給自己；因此擁有者也可以撤銷這些權限。在 SQL 標準中，擁有者的權限是由一個假設的實體「_SYSTEM」所授予。由於擁有者並非「_SYSTEM」，因此無法撤銷這些權利。

根據 SQL 標準，授予選項可以授予給 `PUBLIC`；PostgreSQL 僅支援將授予選項授予給角色。

SQL 標準允許 `GRANTED BY` 選項僅指定 `CURRENT_USER` 或 `CURRENT_ROLE`。其他形式都是 PostgreSQL 的擴充功能。

SQL 標準對其他種類的物件提供了 `USAGE` 權限：字元集、定序（collation）、轉換（translation）。

在 SQL 標準中，序列只有 `USAGE` 權限，用來控制 `NEXT VALUE FOR` 運算式的使用，該運算式等同於 PostgreSQL 中的函式 `nextval`。序列的 `SELECT` 與 `UPDATE` 權限是 PostgreSQL 的擴充功能。將序列的 `USAGE` 權限套用到 `currval` 函式，同樣也是 PostgreSQL 的擴充功能（該函式本身亦然）。

資料庫、表空間、綱要、語言以及組態參數上的權限，都是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.150.9"></a>

## 另請參閱

[REVOKE](sql-revoke.md), [ALTER DEFAULT PRIVILEGES](sql-alterdefaultprivileges.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-grant.html)（原文版本：18.6；核對日期：2026-09-28）
