# GRANT

GRANT — 賦予存取權限

## 語法

```text
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } routine_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]

GRANT role_name [, ...] TO role_specification [, ...]
    [ WITH ADMIN OPTION ]
    [ GRANTED BY role_specification ]

where role_specification can be:

    [ GROUP ] role_name
  | PUBLIC
  | CURRENT_USER
  | SESSION_USER
```

## 說明

GRANT 指令有兩個基本用法：一個是授予資料庫物件（資料表、欄位、檢視表、外部資料表、序列、資料庫、外部資料封裝、外部伺服器、函數、程序語言、綱要或資料表空間）的權限；另一個則是授予角色成員資格的人。這些用法在許多方面類似，但它們的不同之處將會單獨描述。

**在資料庫物件上的 GRANT**

GRANT 指令的這個用法為資料庫物件提供了對一個或多個角色的特定權限。這些權限將會附加到已授予的權限（如果有的話）。

還有一個選項可以在一個或多個綱要中為相同類型的所有物件授予權限。目前僅有資料、序列和函數支援此功能（但請注意，ALL TABLES 被視為包括檢視圖和外部資料表）。

關鍵字 PUBLIC 表示將權限授予所有角色，包括稍後可能建立的角色。 PUBLIC 可以被視為一個隱性定義的群組，它包含了所有角色。任何特定角色都將擁有直接授予它的權限總和，也就是授予其目前成員的任何角色的權限，加上授予 PUBLIC 的權限。

如果指定了 WITH GRANT OPTION，則權限的被授予者可以將該權限授予其他人。如果沒有授權選項，被授予者就無法執行此操作。授權選項不能授予 PUBLIC。

毌須向物件的所有者（通常是建立它的使用者）授予權限，因為預設情況下所有者具備所有權限。 （但是，所有者可以選擇撤銷他們自己的一些安全權限。）

刪除物件或以任何方式變更其定義的權利將不被視為可授予的權限；它是所有者固有的，不能被授予或撤銷。（但是，透過授予或撤銷擁有該物件的角色成員資格可以獲得類似的效果；請參閱下文。）所有者也隱含地擁有該物件的所有授權選項。

PostgreSQL 將某些類型物件的預設權限授予 PUBLIC。預設情況下，對資料表、資料表欄位、序列、外部資料封裝、外部伺服器、大型物件、綱要或資料表空間不會授予 PUBLIC 權限。對於其他類型的物件，授予 PUBLIC 的預設權限如下：CONNECT 和 TEMPORARY（建立臨時資料表）資料庫權限；函數的 EXECUTE 權限；以及語言和資料型別（包括 domain）的 USAGE 權限。當然，物件所有者可以撤銷預設和明確授予的權限。（為了最大限度地提高安全性，請在建立物件的同一交易事務中發出 REVOKE；如此就沒有其他用戶可以使用該物件的窗口。）此外，可以使用 [ALTER DEFAULT PRIVILEGES](alter-default-privileges.md) 指令更改這些初始預設權限設定。

可以設定的權限如下：

`SELECT`  
`INSERT`  
`UPDATE`  
`DELETE`  
`TRUNCATE`  
`REFERENCES`  
`TRIGGER`  
`CREATE`  
`CONNECT`  
`TEMPORARY`  
`EXECUTE`  
`USAGE`

個別特定的權限說明，如[第 5.7 節](../../the-sql-language/ddl/privileges.md)中所定義。

`TEMP`

TEMPORARY 的另一種寫法。

`ALL PRIVILEGES`

授予該物件型別的所有可用權限。PRIVILEGES 關鍵字在 PostgreSQL 中是選擇性的，但它在嚴格的 SQL 中是必要的。

The `FUNCTION` syntax works for plain functions, aggregate functions, and window functions, but not for procedures; use `PROCEDURE` for those. Alternatively, use `ROUTINE` to refer to a function, aggregate function, window function, or procedure regardless of its precise type.

There is also an option to grant privileges on all objects of the same type within one or more schemas. This functionality is currently supported only for tables, sequences, functions, and procedures. `ALL TABLES` also affects views and foreign tables, just like the specific-object `GRANT` command. `ALL FUNCTIONS` also affects aggregate and window functions, but not procedures, again just like the specific-object `GRANT` command. Use `ALL ROUTINES` to include procedures.

#### GRANT on Roles

GRANT 指令也可以用於將角色加入成為其他角色的成員。角色的成員意義重大，因為它可以將授予角色的權限也同等授予給每個成員。

如果指定了 WITH ADMIN OPTION，則該成員就可以將角色的成員資格再授予其他人，也可以撤銷該角色的成員資格。如果沒有 admin 選項，普通使用者就無法做到上述的行為。 角色不被視為對自身持有 WITH ADMIN OPTION，但它可以從連線使用者與角色匹配的資料庫連線中授予或撤銷其自身的成員資格。資料庫的超級使用者可以向任何人授予或撤銷任何角色的成員資格。具有 CREATEROLE 權限的角色可以授予或撤銷任何非超級使用者角色的成員資格。

If `GRANTED BY` is specified, the grant is recorded as having been done by the specified role. Only database superusers may use this option, except when it names the same role executing the command.

Unlike the case with privileges, membership in a role cannot be granted to `PUBLIC`. Note also that this form of the command does not allow the noise word `GROUP` in _`role_specification`_.

### Notes

REVOKE 指令用於撤銷存取權限.

Since PostgreSQL 8.1, the concepts of users and groups have been unified into a single kind of entity called a role. It is therefore no longer necessary to use the keyword `GROUP` to identify whether a grantee is a user or a group. `GROUP` is still allowed in the command, but it is a noise word.

A user may perform `SELECT`, `INSERT`, etc. on a column if they hold that privilege for either the specific column or its whole table. Granting the privilege at the table level and then revoking it for one column will not do what one might wish: the table-level grant is unaffected by a column-level operation.

When a non-owner of an object attempts to `GRANT` privileges on the object, the command will fail outright if the user has no privileges whatsoever on the object. As long as some privilege is available, the command will proceed, but it will grant only those privileges for which the user has grant options. The `GRANT ALL PRIVILEGES` forms will issue a warning message if no grant options are held, while the other forms will issue a warning if grant options for any of the privileges specifically named in the command are not held. \(In principle these statements apply to the object owner as well, but since the owner is always treated as holding all grant options, the cases can never occur.\)

It should be noted that database superusers can access all objects regardless of object privilege settings. This is comparable to the rights of `root` in a Unix system. As with `root`, it's unwise to operate as a superuser except when absolutely necessary.

If a superuser chooses to issue a `GRANT` or `REVOKE` command, the command is performed as though it were issued by the owner of the affected object. In particular, privileges granted via such a command will appear to have been granted by the object owner. \(For role membership, the membership appears to have been granted by the containing role itself.\)

`GRANT` and `REVOKE` can also be done by a role that is not the owner of the affected object, but is a member of the role that owns the object, or is a member of a role that holds privileges `WITH GRANT OPTION` on the object. In this case the privileges will be recorded as having been granted by the role that actually owns the object or holds the privileges `WITH GRANT OPTION`. For example, if table `t1` is owned by role `g1`, of which role `u1` is a member, then `u1` can grant privileges on `t1` to `u2`, but those privileges will appear to have been granted directly by `g1`. Any other member of role `g1` could revoke them later.

If the role executing `GRANT` holds the required privileges indirectly via more than one role membership path, it is unspecified which containing role will be recorded as having done the grant. In such cases it is best practice to use `SET ROLE` to become the specific role you want to do the `GRANT` as.

Granting permission on a table does not automatically extend permissions to any sequences used by the table, including sequences tied to `SERIAL` columns. Permissions on sequences must be set separately.

See [Section 5.7](https://www.postgresql.org/docs/13/ddl-priv.html) for more information about specific privilege types, as well as how to inspect objects' privileges.

## 範例

把向資料表 film 插入資料的權限授予所有使用者：

```text
GRANT INSERT ON films TO PUBLIC;
```

把所有檢視表 kind 可用的權限授予使用者 manuel：

```text
GRANT ALL PRIVILEGES ON kinds TO manuel;
```

請注意，雖然如果由超級使用者或該型別的擁有者執行，上述內容確實會授予所有權限；但當由其他人執行時，它將僅授予其他人其所擁有授權選項的權限。

將角色 admin 的成員資格授予使用者 joe：

```text
GRANT admins TO joe;
```

## 相容性

根據 SQL 標準，ALL PRIVILEGES 中的 PRIVILEGES 關鍵字是需要的。SQL 標準不支援在指令設定多個物件的權限。

PostgreSQL 允許物件擁有者撤銷他們自己的普通權限：例如，資料表擁有者可以透過撤銷自己的 INSERT，UPDATE，DELETE 和 TRUNCATE 權限使資料表對自己而言是唯讀。但根據 SQL 標準，這是不可能的。原因是 PostgreSQL 將擁有者的權限視為已由擁有者授予他們自己；因此他們自己也可以撤銷它們。在 SQL 標準中，擁有者的權限由假設上的實體「\_SYSTEM」授予。由於不是「\_SYSTEM」，擁有者就不能撤銷這些權利。

根據 SQL 標準，可以向 PUBLIC 授予授權選項；PostgreSQL 僅支援向角色授予授權選項。

SQL 標準為其他型別的物件提供 USAGE 權限：字元集，排序規則，翻譯。

在 SQL 標準中，序列只有 USAGE 權限，它控制 NEXT VALUE FOR 表示式的使用，這相當於 PostgreSQL 中的 nextval 函數。序列權限 SELECT 和 UPDATE 是 PostgreSQL 的延伸功能。將序列 USAGE 權限套用於 currval 函數也是 PostgreSQL 的延伸功能（函數本身也是如此）。

資料庫，資料表空間，綱要和語言的權限都是 PostgreSQL 的延伸功能。

## 參閱

[REVOKE](revoke.md), [ALTER DEFAULT PRIVILEGES](alter-default-privileges.md)

