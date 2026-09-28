<a id="id-1.9.3.161.1"></a>

## REASSIGN OWNED

REASSIGN OWNED — 變更某資料庫角色所擁有的資料庫物件之擁有權

## 語法

```

REASSIGN OWNED BY { old_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...]
               TO { new_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.161.5"></a>

## 說明

`REASSIGN OWNED` 會指示系統，將任一
*`old_roles`* 所擁有的資料庫物件之擁有權，
變更為 *`new_role`*。

<a id="id-1.9.3.161.6"></a>

## 參數

*`old_role`*
:   角色名稱。目前資料庫內、由此角色所擁有的所有物件，以及此角色所擁有的所有共享物件（資料庫、資料表空間），其擁有權都會被重新指派給
    *`new_role`*。

*`new_role`*
:   將成為受影響物件之新擁有者的角色名稱。

<a id="id-1.9.3.161.7"></a>

## 注意

`REASSIGN OWNED` 通常用於為移除一個或多個角色做準備。由於 `REASSIGN OWNED` 不會影響其他資料庫內的物件，因此通常必須在每個包含要移除角色所擁有物件的資料庫中，各自執行一次此指令。

`REASSIGN OWNED` 要求執行者同時具備來源角色與目標角色的成員資格。

[`DROP OWNED`](sql-drop-owned.md) 指令是另一種替代做法，它會直接刪除一個或多個角色所擁有的所有資料庫物件。

`REASSIGN OWNED` 指令不會影響已授予
*`old_roles`* 之、但屬於其他角色所擁有物件上的權限。同樣地，它也不會影響以
`ALTER DEFAULT PRIVILEGES` 所建立的預設權限。若要撤銷這類權限，請使用
`DROP OWNED`。

更多討論請參閱[第 21.4 節](../../server-administration/user-manag/role-removal.md)。

<a id="id-1.9.3.161.8"></a>

## 相容性

`REASSIGN OWNED` 指令是
PostgreSQL 的擴充功能。

<a id="id-1.9.3.161.9"></a>

## 另請參閱

[DROP OWNED](sql-drop-owned.md), [DROP ROLE](sql-droprole.md), [ALTER DATABASE](sql-alterdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-reassign-owned.html)（原文版本：18.6；核對日期：2026-09-28）
