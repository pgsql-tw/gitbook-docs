# DROP ROLE

DROP ROLE — 移除資料庫角色

### 語法

```text
DROP ROLE [ IF EXISTS ] name [, ...]
```

### 說明

DROP ROLE 移除指定的角色。要移除超級使用者角色的話，您必須自己成為超級用戶；要刪除非超級使用者角色，您必須具有 CREATEROLE 權限。

如果角色在叢集的任何資料庫中仍被引用，則無法移除該角色；如果執行的話，會出現錯誤。在移除角色之前，您必須移除其擁有的所有物件（或重新分配其所有權），並撤銷該角色已授予其他角色的任何權限。REASSIGN OWNED 和 DROP OWNED 指令可用於此目的；更多討論請參閱[第 21.4 節](../../server-administration/user-manag/dropping-roles.md)。

但是，沒有必要刪除涉及角色的角色成員。DROP ROLE 會自動撤銷其他角色中的目標角色以及目標角色中的其他角色的任何成員資格。其他角色不會被丟棄或受到其他影響。

### Parameters

`IF EXISTS`

Do not throw an error if the role does not exist. A notice is issued in this case._`name`_

The name of the role to remove.

### Notes

PostgreSQL includes a program [dropuser](https://www.postgresql.org/docs/10/static/app-dropuser.html) that has the same functionality as this command \(in fact, it calls this command\) but can be run from the command shell.

### Examples

To drop a role:

```text
DROP ROLE jonathan;
```

### Compatibility

The SQL standard defines `DROP ROLE`, but it allows only one role to be dropped at a time, and it specifies different privilege requirements than PostgreSQL uses.

### See Also

[CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html), [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html), [SET ROLE](https://www.postgresql.org/docs/10/static/sql-set-role.html)

