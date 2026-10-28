<a id="APP-CREATEUSER"></a><a id="id-1.9.4.5.1"></a>

## createuser

createuser — 定義新的 PostgreSQL 使用者帳號

<a id="id-1.9.4.5.4"></a>

## 語法

<a id="id-1.9.4.5.4.1"></a>

`createuser` [*`connection-option`*...] [*`option`*...] [*`username`*]

<a id="id-1.9.4.5.5"></a>

## 說明

createuser 會建立一個新的 PostgreSQL 使用者（更精確地說，是一個角色）。只有超級使用者與具有 `CREATEROLE` 權限的使用者才能建立新使用者，因此 createuser 必須由能以超級使用者或具有 `CREATEROLE` 權限之使用者身分連線的人來呼叫。

若你想建立具有 `SUPERUSER`、`REPLICATION` 或 `BYPASSRLS` 權限的角色，你必須以超級使用者身分連線，僅具有 `CREATEROLE` 權限是不夠的。身為超級使用者意味著能夠略過資料庫內所有的存取權限檢查，因此不應輕易授予超級使用者存取權。`CREATEROLE` 同樣賦予[非常廣泛的權限](../../server-administration/user-manag/role-attributes.md#ROLE-CREATION)。

createuser 是 SQL 命令 [`CREATE ROLE`](../sql-commands/sql-createrole.md) 的包裝程式。透過此工具程式建立使用者，與透過其他存取伺服器的方法建立使用者，實際上沒有任何差別。

<a id="id-1.9.4.5.6"></a>

## 選項

createuser 接受下列命令列引數：

*`username`*
:   指定要建立的 PostgreSQL 使用者名稱。此名稱必須與此 PostgreSQL 安裝中所有現有的角色都不同。

`-a role`<br>`--with-admin=role`
:   指定一個現有角色，該角色會自動以 admin option 加入成為新角色的成員，使其有權將新角色的成員資格授予他人。寫多個 `-a` 參數即可指定多個現有角色。

`-c number`<br>`--connection-limit=number`
:   設定新使用者的最大連線數。預設為不設限制。

`-d`<br>`--createdb`
:   新使用者將被允許建立資料庫。

`-D`<br>`--no-createdb`
:   新使用者將不被允許建立資料庫。這是預設行為。

`-e`<br>`--echo`
:   回顯 createuser 產生並送往伺服器的命令。

`-E`<br>`--encrypted`
:   此選項已過時，但為了向後相容性仍然接受。

`-g role`<br>`--member-of=role`<br>`--role=role`（已棄用）
:   指定新角色應自動加入成為指定之現有角色的成員。寫多個 `-g` 參數即可指定多個現有角色。

`-i`<br>`--inherit`
:   新角色將自動繼承其所屬角色的權限。這是預設行為。

`-I`<br>`--no-inherit`
:   新角色將不會自動繼承其所屬角色的權限。

`--interactive`
:   若命令列上未指定使用者名稱，則提示輸入使用者名稱；對於 `-d`/`-D`、`-r`/`-R`、`-s`/`-S` 這幾組選項中命令列上未指定的任何一組，也會提示輸入。（直到 PostgreSQL 9.1 為止，這都是預設行為。）

`-l`<br>`--login`
:   新使用者將被允許登入（也就是說，該使用者名稱可以用作初始的工作階段使用者識別碼）。這是預設行為。

`-L`<br>`--no-login`
:   新使用者將不被允許登入。（沒有登入權限的角色仍然可以作為管理資料庫權限的一種方式。）

`-m role`<br>`--with-member=role`
:   指定一個現有角色，該角色會自動加入成為新角色的成員。寫多個 `-m` 參數即可指定多個現有角色。

`-P`<br>`--pwprompt`
:   若指定此選項，createuser 會發出提示，要求輸入新使用者的密碼。若你不打算使用密碼驗證，則不需要此選項。

`-r`<br>`--createrole`
:   新使用者將被允許建立、修改、移除其他角色，為其他角色加上註解，以及變更其他角色的安全標籤；也就是說，此使用者將具有 `CREATEROLE` 權限。關於此權限所賦予之能力的更多細節，請參閱[角色建立](../../server-administration/user-manag/role-attributes.md#ROLE-CREATION)。

`-R`<br>`--no-createrole`
:   新使用者將不被允許建立新角色。這是預設行為。

`-s`<br>`--superuser`
:   新使用者將成為超級使用者。

`-S`<br>`--no-superuser`
:   新使用者將不會成為超級使用者。這是預設行為。

`-v timestamp`<br>`--valid-until=timestamp`
:   設定一個日期與時間，在此之後該角色的密碼不再有效。預設為不設定密碼到期日。

`-V`<br>`--version`
:   印出 createuser 的版本後結束。

`--bypassrls`
:   新使用者將略過所有資料列層級安全性（RLS）政策。

`--no-bypassrls`
:   新使用者將不會略過資料列層級安全性（RLS）政策。這是預設行為。

`--replication`
:   新使用者將具有 `REPLICATION` 權限，此權限在 [CREATE ROLE](../sql-commands/sql-createrole.md) 的文件中有更完整的說明。

`--no-replication`
:   新使用者將不具有 `REPLICATION` 權限，此權限在 [CREATE ROLE](../sql-commands/sql-createrole.md) 的文件中有更完整的說明。這是預設行為。

`-?`<br>`--help`
:   顯示 createuser 命令列引數的說明後結束。

createuser 也接受下列用於連線參數的命令列引數：

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會被當作 Unix 網域通訊端的目錄。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱（不是要建立的使用者名稱）。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試將會失敗。此選項在沒有使用者可以輸入密碼的批次作業與腳本中可能很有用。

`-W`<br>`--password`

強制 createuser 提示輸入密碼（用於連線到伺服器，而不是新使用者的密碼）。

此選項從來都不是必要的，因為若伺服器要求密碼驗證，createuser 會自動提示輸入密碼。不過，createuser 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

<a id="id-1.9.4.5.7"></a>

## 環境

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數

`PG_COLOR`
:   指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

此工具程式和大多數其他 PostgreSQL 工具程式一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

<a id="id-1.9.4.5.8"></a>

## 診斷

若遇到困難，請參閱 [CREATE ROLE](../sql-commands/sql-createrole.md) 與 [psql](app-psql.md) 中關於潛在問題與錯誤訊息的討論。資料庫伺服器必須在目標主機上執行。此外，libpq 前端函式庫所使用的任何預設連線設定與環境變數也都適用。

<a id="id-1.9.4.5.9"></a>

## 範例

在預設資料庫伺服器上建立使用者 `joe`：

```

$ createuser joe
```

在預設資料庫伺服器上建立使用者 `joe`，並提示輸入一些額外的屬性：

```

$ createuser --interactive joe
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

使用主機 `eden`、連接埠 5000 上的伺服器建立同一個使用者 `joe`，並明確指定屬性，同時查看底層實際執行的命令：

```

$ createuser -h eden -p 5000 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
```

將使用者 `joe` 建立為超級使用者，並立即設定密碼：

```

$ createuser -P -s -e joe
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE joe PASSWORD 'SCRAM-SHA-256$4096:44560wPMLfjqiAzyPDZ/eQ==$4CA054rZlSFEq8Z3FEhToBTa2X6KnWFxFkPwIbKoDe0=:L/nbSZRCjp6RhOhKK56GoR1zibCCSePKshCJ9lnl3yw=' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN NOREPLICATION NOBYPASSRLS;
```

在上面的範例中，新密碼在輸入時實際上並不會回顯，但為了清楚起見，我們顯示了所輸入的內容。如你所見，密碼在傳送給伺服器之前就已經加密（原文此處寫作 sent to the client，但實際上是 createuser 在用戶端處理密碼後，將產生的 SCRAM 密碼驗證資訊傳送給伺服器）。

<a id="id-1.9.4.5.10"></a>

## 另請參閱

[dropuser](app-dropuser.md), [CREATE ROLE](../sql-commands/sql-createrole.md), [createrole_self_grant](../../server-administration/runtime-config/runtime-config-client.md#GUC-CREATEROLE-SELF-GRANT)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-createuser.html)（原文版本：18.6；核對日期：2026-10-10）
