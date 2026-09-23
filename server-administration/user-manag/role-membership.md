<a id="ROLE-MEMBERSHIP"></a>

## 21.3. 角色成員資格 [#](#ROLE-MEMBERSHIP)

<a id="id-1.6.8.7.2"></a>

為了簡化權限管理，將使用者分組通常相當方便：如此一來，
就能針對整個群組，授予或撤銷權限。在 PostgreSQL 中，
做法是建立一個代表該群組的角色，然後將個別使用者角色，
授予該群組角色中的*成員資格*。

若要建立群組角色，首先建立該角色：

```

CREATE ROLE name;
```

通常，用作群組的角色不會具有 `LOGIN` 屬性，
不過您若願意，仍可以設定此屬性。

一旦群組角色存在，就可以使用
[`GRANT`](../../reference/sql-commands/sql-grant.md) 與
[`REVOKE`](../../reference/sql-commands/sql-revoke.md) 指令，
新增或移除成員：

```

GRANT group_role TO role1, ... ;
REVOKE group_role FROM role1, ... ;
```

您也可以將成員資格授予其他群組角色（因為群組角色
與非群組角色之間，實際上並沒有真正的區別）。資料庫
不允許您建立循環成員資格的迴圈。此外，
也不允許將角色的成員資格，授予 `PUBLIC`。

群組角色的成員，可以透過兩種方式使用該角色的權限。
第一種方式，是已透過 `SET` 選項被授予成員資格的
成員角色，可以執行
[`SET ROLE`](../../reference/sql-commands/sql-set-role.md)，
暫時「變成」該群組角色。在此狀態下，資料庫工作階段
所能使用的，是群組角色的權限，而非原始登入角色的權限，
並且任何建立的資料庫物件，都會被視為由該群組角色所擁有，
而非登入角色所擁有。第二種方式，是已透過
`INHERIT` 選項被授予成員資格的成員角色，
會自動具有其直接或間接所屬角色的權限，
不過這條鏈結，會在遇到不具繼承選項的成員資格時中斷。
舉例來說，假設我們已執行：

```

CREATE ROLE joe LOGIN;
CREATE ROLE admin;
CREATE ROLE wheel;
CREATE ROLE island;
GRANT admin TO joe WITH INHERIT TRUE;
GRANT wheel TO admin WITH INHERIT FALSE;
GRANT island TO joe WITH INHERIT TRUE, SET FALSE;
```

以角色 `joe` 連線之後，資料庫工作階段
會立即擁有直接授予 `joe` 的權限，
加上任何授予 `admin` 與 `island` 的權限，
因為 `joe`「繼承」了這些權限。不過，
授予 `wheel` 的權限則無法使用，因為即使
`joe` 間接是 `wheel` 的成員，
但這項成員資格是透過 `admin` 取得的，
而該項授予是以 `WITH INHERIT FALSE` 完成的。
執行以下指令後：

```

SET ROLE admin;
```

該工作階段就只能使用授予 `admin` 的權限，
而不能使用授予 `joe` 或 `island` 的權限。
執行以下指令後：

```

SET ROLE wheel;
```

該工作階段就只能使用授予 `wheel` 的權限，
而不能使用授予 `joe` 或 `admin` 的權限。
可以透過下列任一指令，恢復原本的權限狀態：

```

SET ROLE joe;
SET ROLE NONE;
RESET ROLE;
```

### 注意

只要成員資格授予的鏈結中，每一項都具有
`SET TRUE`（此為預設值），`SET ROLE` 指令
就一律允許選取原始登入角色直接或間接所屬的任何角色。
因此，在上述範例中，並不需要先變成 `admin`，
才能變成 `wheel`。另一方面，則完全無法變成
`island`；`joe` 只能透過繼承，
存取這些權限。

### 注意

在 SQL 標準中，使用者與角色之間有明確的區別，
使用者不會自動繼承權限，而角色則會。在 PostgreSQL 中，
可以透過將用作 SQL 角色的角色，賦予 `INHERIT` 屬性，
而將用作 SQL 使用者的角色，賦予 `NOINHERIT` 屬性，
來取得這種行為。不過，為了向下相容 8.1 之前的版本
（在該版本中，使用者一律能使用其所屬群組所被授予的權限），
PostgreSQL 預設會賦予所有角色 `INHERIT` 屬性。

`LOGIN`、`SUPERUSER`、`CREATEDB` 與
`CREATEROLE` 這些角色屬性，可以視為特殊權限，
但它們絕不會像資料庫物件上的一般權限那樣被繼承。
您必須實際 `SET ROLE` 至具有這些屬性之一的
特定角色，才能使用該屬性。延續上面的範例，
我們可能會選擇將 `CREATEDB` 與 `CREATEROLE`，
授予 `admin` 角色。如此一來，以角色 `joe`
連線的工作階段，就不會立即擁有這些權限，
必須先執行 `SET ROLE admin` 之後才會擁有。

若要刪除群組角色，請使用
[`DROP ROLE`](../../reference/sql-commands/sql-droprole.md)：

```

DROP ROLE name;
```

該群組角色中的所有成員資格，都會自動被撤銷
（但成員角色本身，不會因此受到其他影響）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/role-membership.html)（原文版本：18.6；核對日期：2026-09-22）
