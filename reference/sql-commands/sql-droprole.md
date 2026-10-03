<a id="SQL-DROPROLE"></a><a id="id-1.9.3.126.1"></a>

## DROP ROLE

DROP ROLE — 移除資料庫角色

<a id="id-1.9.3.126.4"></a>

## 語法

```

DROP ROLE [ IF EXISTS ] name [, ...]
```

<a id="id-1.9.3.126.5"></a>

## 說明

`DROP ROLE` 會移除指定的角色。若要移除超級使用者角色，你自己必須是超級使用者；若要移除非超級使用者角色，你必須具有 `CREATEROLE` 權限，並且已被授予該角色的 `ADMIN OPTION`。

若角色仍在叢集中的任何資料庫內被參照，就無法移除；若是如此，會引發錯誤。移除角色之前，必須先移除它擁有的所有物件（或重新指派這些物件的擁有權），並撤銷該角色在其他物件上被授予的所有權限。[`REASSIGN OWNED`](sql-reassign-owned.md) 與 [`DROP OWNED`](sql-drop-owned.md) 命令可能有助於達成此目的；更多討論請參閱[第 21.4 節](../../server-administration/user-manag/role-removal.md)。

不過，不需要移除涉及該角色的角色成員資格；`DROP ROLE` 會自動撤銷目標角色在其他角色中的所有成員資格，以及其他角色在目標角色中的成員資格。這些其他角色既不會被移除，也不會受到其他影響。

<a id="id-1.9.3.126.6"></a>

## 參數

`IF EXISTS`
:   角色不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之角色的名稱。

<a id="id-1.9.3.126.7"></a>

## 注意事項

PostgreSQL 提供一個程式 [dropuser](../reference-client/app-dropuser.md)，其功能與此命令相同（事實上，它會呼叫此命令），但可以從命令 shell 執行。

<a id="id-1.9.3.126.8"></a>

## 範例

移除一個角色：

```

DROP ROLE jonathan;
```

<a id="id-1.9.3.126.9"></a>

## 相容性

SQL 標準定義了 `DROP ROLE`，但它一次只允許移除一個角色，而且它規定的權限要求與 PostgreSQL 所用的不同。

<a id="id-1.9.3.126.10"></a>

## 另請參閱

[CREATE ROLE](sql-createrole.md), [ALTER ROLE](sql-alterrole.md), [SET ROLE](sql-set-role.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droprole.html)（原文版本：18.6；核對日期：2026-10-03）
