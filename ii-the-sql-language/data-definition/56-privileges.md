# 5.6. 權限[^1]

當一個資料庫物件被建立時，它會先指定存取權限給擁有者，而擁有者一般來說就是執行建立指令的使用者。對大多數的資料庫物件來說，其預設的狀態就是只有擁有者（或超級使用者）可以對該物件進行所有操作。要讓給其他使用者來操作的話，就必須進行授權的動作。

有很多不同種類的權限：SELECT、INSERT、UPDATE、DELETE、TRUNCATE、REFERENCES、TRIGGER、CREATE、CONNECT、TEMPORARY、EXECUTE、USAGE。這些權限對於不同物件的效果，會因為是哪一種物件而有所差別（表格、函式...等等）。要瞭解完整在 PostgreSQL 中所支援的各種物件權限，請參考 [GRANT](/vi-reference/i-sql-commands/grant.md) 語法頁面。這裡的內容主要說明如何使用。

修改和移除一個資料庫物件，是只有擁有者才具備的權力。

要把一個物件被指派給一個新的擁有者的話，使用該物件的 ALTER 指令，例如：[ALTER TABLE](/vi-reference/i-sql-commands/alter-table.md)。超級使用者也可以做指派的動作；原來的擁有者如果它仍是該物件的管理群組一員的話，當然也可以；再來就管理群組新的成員。

要進行授權行為的話，請使用 GRANT 指令。舉例來說，如果 joe 是一個使用者，而 accounts 是一個表格，要讓他可以獲得更新表格資料的權力：

```
GRANT UPDATE ON accounts TO joe;
```

使用 ALL 的權限，就代表授權所有可設定的權限。

有一個特別的使用者是 PUBLIC，代表的是系統內的所有使用者。當資料庫內有很多使用者時，可以制定「群組（group）」來簡化管理。這部份詳細的說明請參閱[第 21 章](/iii-server-administration/database-roles.md)。

要移除權限，請使用 REVOKE 指令：

```
REVOKE ALL ON accounts FROM PUBLIC;
```

物件擁有者的特殊權限（例如DROP、GRANT、REVOKE...等）都是和擁有者一起設定，而無法單獨授權。不過，擁有者可以選擇移除自己的權限，例如建立一個唯讀的表格，讓自己和其他人一樣。

回到前面所說的，只有物件的擁有者（或超級使用者）可以變更該物件的權限。然而，也可以使用「with grant option」讓另一個使用者可以代授權給其他使用者。不過如果這個「grant option」被移除時，所有被代授權的使用者都會同時喪失該權限。更詳細的說明請參閱 [GRANT](/vi-reference/i-sql-commands/grant.md) 及 [REVOKE](/vi-reference/i-sql-commands/revoke.md) 說明頁面。

---

[^1]: [PostgreSQL: Documentation: 10: 5.6. Privileges](https://www.postgresql.org/docs/10/static/ddl-priv.html)

