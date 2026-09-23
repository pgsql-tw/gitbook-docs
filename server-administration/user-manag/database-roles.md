<a id="DATABASE-ROLES"></a>

## 21.1. 資料庫角色 [#](#DATABASE-ROLES)

<a id="id-1.6.8.5.2"></a><a id="id-1.6.8.5.3"></a><a id="id-1.6.8.5.4"></a><a id="id-1.6.8.5.5"></a>

就概念而言，資料庫角色與作業系統使用者是完全分開的。
在實務上，讓兩者維持對應關係或許很方便，
但這並非必要。資料庫角色是整個資料庫叢集安裝
共用的全域物件（而非依個別資料庫而定）。若要建立角色，
請使用 [`CREATE ROLE`](../../reference/sql-commands/sql-createrole.md) SQL 指令：

```

CREATE ROLE name;
```

*`name`* 遵循 SQL 識別字的規則：可以是不加修飾、
不含特殊字元的形式，也可以是以雙引號括住的形式。
（在實務上，您通常會想為此指令加上額外選項，
例如 `LOGIN`；更多細節請見下文。）若要移除既有角色，
請使用對應的
[`DROP ROLE`](../../reference/sql-commands/sql-droprole.md) 指令：

```

DROP ROLE name;
```

<a id="id-1.6.8.5.7"></a><a id="id-1.6.8.5.8"></a>

為方便起見，系統也提供了
[createuser](../../reference/reference-client/app-createuser.md)
與 [dropuser](../../reference/reference-client/app-dropuser.md) 程式，
作為這些 SQL 指令的包裝程式，可從 shell 命令列呼叫：

```

createuser name
dropuser name
```

若要確認目前存在哪些角色，可以查詢 `pg_roles`
系統目錄，例如：

```

SELECT rolname FROM pg_roles;
```

或者，若只想查看能夠登入的角色：

```

SELECT rolname FROM pg_roles WHERE rolcanlogin;
```

[psql](../../reference/reference-client/app-psql.md) 程式的
`\du` 元指令（meta-command），
在列出現有角色時也相當實用。

為了啟動（bootstrap）整個資料庫系統，一個剛初始化完成的
系統，一律會包含一個預先定義、具備登入能力的角色。此角色
一律是「超級使用者」，除非另外指定不同的名稱，
否則其名稱會與使用 `initdb` 初始化該資料庫叢集的
作業系統使用者相同。此角色通常命名為
`postgres`。若要建立更多角色，
您必須先以此初始角色連線。

對資料庫伺服器的每一次連線，都是以某個特定角色的名稱建立的，
而該角色，決定了在該連線中所發出指令的初始存取權限。
用於某個特定資料庫連線的角色名稱，是由發起連線請求的
用戶端，以特定應用程式的方式指出的。舉例來說，
`psql` 程式使用 `-U` 命令列選項，
指出要以哪個角色連線。許多應用程式（包括
`createuser` 與 `psql`），
預設會採用目前作業系統使用者的名稱。因此，
在角色與作業系統使用者之間，維持命名上的對應關係，
通常相當方便。

某個特定用戶端連線，可以哪些資料庫角色的身分連線，
是由用戶端驗證設定所決定的，如
[第 20 章](../client-authentication/README.md)所述。
（因此，用戶端並不受限於只能以符合其作業系統使用者的角色連線，
就如同一個人的登入名稱，不必與他或她的真實姓名相符。）
由於角色身分，決定了已連線用戶端可用的權限集合，
因此在建立多使用者環境時，謹慎地設定權限相當重要。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/database-roles.html)（原文版本：18.6；核對日期：2026-09-22）
