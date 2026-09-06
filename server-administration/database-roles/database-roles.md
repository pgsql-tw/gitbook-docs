# 22.1. Database Roles

資料庫角色在概念上與作業系統使用者是完全分離的。實務上，維持兩者對應關係可能會比較方便，但這並非必要。資料庫角色在整個資料庫叢集安裝中是全域性的（而不是針對單一資料庫）。要建立一個角色，請使用 [CREATE ROLE](https://www.postgresql.org/docs/12/sql-createrole.html) SQL 指令：

```
CREATE ROLE name;
```

_`name`_ 必須符合 SQL 識別字的命名規則：可以是沒有特殊字元的普通名稱，或是使用雙引號包住的名稱。（實務上，你通常會想在指令中加上額外選項，例如 `LOGIN`。更多細節請見下文。）若要刪除一個既有的角色，請使用對應的 [DROP ROLE](https://www.postgresql.org/docs/12/sql-droprole.html) 指令：

```
DROP ROLE name;
```

為了方便起見，系統提供了 [createuser](https://www.postgresql.org/docs/12/app-createuser.html) 與 [dropuser](https://www.postgresql.org/docs/12/app-dropuser.html) 這兩個程式，它們是這些 SQL 指令的包裝器，可直接從 shell 命令列中呼叫：

```
createuser name
dropuser name
```

若要查詢現有的角色集合，可以查看 `pg_roles` 系統資料表，例如：

```
SELECT rolname FROM pg_roles;
```

[psql](https://www.postgresql.org/docs/12/app-psql.html) 程式的 `\du` 指令也很實用，可用來列出目前已有的角色。

為了初始化資料庫系統，每一個新建的系統都會包含一個預定義的角色。這個角色總是「超級使用者（superuser）」，預設情況下（除非在執行 `initdb` 時變更）會與初始化資料庫叢集的作業系統使用者同名。通常這個角色會被命名為 `postgres`。若要建立更多的角色，你必須先以這個初始角色連線。

每一次連線到資料庫伺服器時，都會使用某個特定角色的名稱，而這個角色會決定該連線中所執行指令的初始存取權限。要使用哪個角色名稱連線，是由發起連線請求的用戶端透過特定應用程式的方式指定。例如，`psql` 程式使用 `-U` 命令列選項來指定要以哪個角色進行連線。許多應用程式預設會使用目前作業系統使用者的名稱（包括 `createuser` 和 `psql`）。因此，維持角色名稱與作業系統使用者名稱一致，通常會比較方便。

某個用戶端連線可以連線為哪些資料庫角色，是由用戶端的認證設定所決定，如 [第 20 章](https://www.postgresql.org/docs/12/client-authentication.html) 所述。（因此，用戶端並不限於只能連線為與其作業系統使用者相同名稱的角色，就像一個人的登入名稱不必與他的真實姓名相同。）由於角色身分會決定已連線用戶端所擁有的權限，因此在建立多用戶環境時，應小心地設定各角色的權限。
