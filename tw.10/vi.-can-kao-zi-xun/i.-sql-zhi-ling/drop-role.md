# DROP ROLE

DROP ROLE — 移除資料庫角色

### 語法

```text
DROP ROLE [ IF EXISTS ] name [, ...]
```

### 說明

DROP ROLE 移除指定的角色。要移除超級使用者角色的話，您必須自己成為超級用戶；要刪除非超級使用者角色，您必須具有 CREATEROLE 權限。

如果角色在叢集的任何資料庫中仍被引用，則無法移除該角色；如果執行的話，會出現錯誤。在移除角色之前，您必須移除其擁有的所有物件（或重新分配其所有權），並撤銷該角色已授予其他角色的任何權限。[REASSIGN OWNED](reassign-owned.md) 和 [DROP OWNED](drop-owned.md) 指令可用於此目的；更多討論請參閱[第 21.4 節](../../server-administration/21.-zi-liao-ku-jiao-se/21.4.-yi-chu-jiao-se.md)。

但是，沒有必要刪除涉及角色的角色成員。DROP ROLE 會自動撤銷其他角色中的目標角色以及目標角色中的其他角色的任何成員資格。其他角色不會被丟棄或受到其他影響。

### 參數

`IF EXISTS`

如果角色不存在，請不要拋出錯誤。在這種情況下會發布通知。

_`name`_

要移除的角色名稱。

### 注意

PostgreSQL 包含一個與此命令具有相同功能的工具程式 [dropuser](../ii.-postgresql-yong-hu-duan-gong-ju/dropuser.md)（實際上，它也呼叫此命令），但可以從終端機的命令列上執行。

### 範例

移除角色：

```text
DROP ROLE jonathan;
```

### 相容性

SQL 標準定義了 DROP ROLE，但它只允許一次移除一個角色，並且它指定了不同於 PostgreSQL 使用的權限要求。

### 參閱

[CREATE ROLE](create-role.md), [ALTER ROLE](alter-role.md), [SET ROLE](set-role.md)

