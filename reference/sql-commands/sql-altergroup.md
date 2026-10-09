<a id="SQL-ALTERGROUP"></a><a id="id-1.9.3.15.1"></a>

## ALTER GROUP

ALTER GROUP — 變更角色名稱或成員資格

<a id="id-1.9.3.15.4"></a>

## 語法

```

ALTER GROUP role_specification ADD USER user_name [, ... ]
ALTER GROUP role_specification DROP USER user_name [, ... ]

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER

ALTER GROUP group_name RENAME TO new_name
```

<a id="id-1.9.3.15.5"></a>

## 說明

`ALTER GROUP` 會變更使用者群組的屬性。這是一個已過時的命令，但為了向後相容性仍然接受，因為群組（以及使用者）已被更一般化的角色概念所取代。

前兩種形式會將使用者加入群組，或從群組中移除使用者。（就此用途而言，任何角色都可以扮演「使用者」或「群組」的角色。）這些形式實際上等同於授予或撤銷被指名為「群組」之角色的成員資格；因此，較建議的做法是使用 [`GRANT`](sql-grant.md) 或 [`REVOKE`](sql-revoke.md)。請注意，`GRANT` 與 `REVOKE` 具有此命令所沒有的額外選項，例如授予與撤銷 `ADMIN OPTION` 的能力，以及指定授予者的能力。

第三種形式會變更群組的名稱。這完全等同於使用 [`ALTER ROLE`](sql-alterrole.md) 重新命名該角色。

<a id="id-1.9.3.15.6"></a>

## 參數

*`group_name`*
:   要修改的群組（角色）名稱。

*`user_name`*
:   要加入群組或從群組中移除的使用者（角色）。這些使用者必須已經存在；`ALTER GROUP` 不會建立或移除使用者。

*`new_name`*
:   群組的新名稱。

<a id="id-1.9.3.15.7"></a>

## 範例

將使用者加入群組：

```

ALTER GROUP staff ADD USER karl, john;
```

從群組中移除一個使用者：

```

ALTER GROUP workers DROP USER beth;
```

<a id="id-1.9.3.15.8"></a>

## 相容性

SQL 標準中沒有 `ALTER GROUP` 陳述式。

<a id="id-1.9.3.15.9"></a>

## 另請參閱

[GRANT](sql-grant.md), [REVOKE](sql-revoke.md), [ALTER ROLE](sql-alterrole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altergroup.html)（原文版本：18.6；核對日期：2026-10-05）
