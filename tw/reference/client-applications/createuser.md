# createuser

createuser — 定義一個新的 PostgreSQL 使用者帳戶

### 語法

`createuser` \[_`connection-option`_...] \[_`option`_...] \[_`username`_]

### 說明

createuser 建立一個新的 PostgreSQL 使用者（或更確切地說，一個角色）。只有具有 CREATEROLE 權限使用者或超級使用者才能建立新的使用者，因此必須由可以作為超級用戶或具有 CREATEROLE 權限的使用者進行連線使用 createuser。

如果要建立新的超級使用者，則必須以超級使用者身份進行連線，而不僅僅是擁有 CREATEROLE 權限。作為超級使用者意味著能夠繞過資料庫中的所有存取權限檢查，因此不應輕易授予超級使用者權限。

createuser 是 SQL 指令 CREATE ROLE 封裝的工具。透過此實用工具建立使用者和透過其他方法存取伺服器之間沒有任何區別。

### 選項

createuser 接受以下命令列選項：

_`username`_

指定要建立的 PostgreSQL 使用者名稱。此名稱必須與此 PostgreSQL 服務中的所有現有角色不同。

`-c `_`number`_\
`--connection-limit=`_`number`_

設定新使用者的最大連線數。預設為無限制。

`-d`\
`--createdb`

將允許新使用者建立資料庫。

`-D`\
`--no-createdb`

不允許新使用者建立資料庫。這是預設值。

`-e`\
`--echo`

顯示 createuser 産生並發送到伺服器的指令。

`-E`\
`--encrypted`

此選項已過時但仍可接受，為了向下相容。

`-g `_`role`_\
`--role=`_`role`_

表示此角色將作為新成員立即添加到的角色。可以透過加上多個 -g 來指定將此角色添加為成員的多個角色。

`-i`\
`--inherit`

新角色將自動繼承其所屬角色的權限。這是預設值。

`-I`\
`--no-inherit`

新角色不會自動繼承其所屬角色的權限。

`--interactive`

如果在命令列中未指定使用者名稱，則提示輸入使用者名稱，並且還會提示在命令列中未指定 -d/-D，-r/-R，-s/-S 中的任何選項。（這是 PostgreSQL 9.1 的預設行為。）

`-l`\
`--login`

將允許新使用者登入（即，使用者名稱可以用作初始連線使用者）。這是預設值。

`-L`\
`--no-login`

將不允許新使用者登入。（沒有登入權限的角色作為管理資料庫權限的作法仍然很有用。）

`-P`\
`--pwprompt`

如果有此選項，createuser 將發出新使用者密碼的提示。如果您不打算使用密碼身份驗證，則毌須執行此操作。

`-r`\
`--createrole`

將允許新使用者建立新角色（即，此使用者將具有 CREATEROLE 權限）。

`-R`\
`--no-createrole`

不允許新使用者建立新角色。這是預設值。

`-s`\
`--superuser`

新使用者將是超級使用者。

`-S`\
`--no-superuser`

新用戶不是超級用戶。這是預設值。

`-V`\
`--version`

輸出 createuser 版本然後退出。

`--replication`

新使用者將具有 REPLICATION 權限，在 [CREATE ROLE](../sql-commands/create-role.md) 的頁面中對此進行了更全面的描述。

`--no-replication`

新使用者將不會有 REPLICATION 權限，這在 [CREATE ROLE](../sql-commands/create-role.md) 的頁面中有更全面的描述。

`-?`\
`--help`

顯示有關 createuser 命令列選項的協助資訊，然後退出。

createuser 還接受以下連線參數的命令列選項：

`-h `_`host`_\
`--host=`_`host`_

指定運行伺服器的主機名稱。如果以斜槓開頭，則將其用作 Unix domain socke 的目錄。

`-p `_`port`_\
`--port=`_`port`_

指定伺服器正在監聽連線的 TCP 連接埠或本地 Unix domain socket 檔案延伸名稱。

`-U `_`username`_\
`--username=`_`username`_

要連線的使用者名稱（不是要建立的使用者名稱）。

`-w`\
`--no-password`

不要發出密碼提示。如果伺服器需要密碼身份驗證，並且其他方式（例如 .pgpass 檔案）也無法使用密碼，則連線嘗試將會失敗。此選項在沒有使用者輸入密碼的批處理作業和腳本中非常有用。

`-W`\
`--password`

強制 createuser 提示輸入密碼（用於連線伺服器，而不是新使用者的密碼）。

此選項都不是必須的，因為如果伺服器需要密碼身份驗證，createuser 將自動提示輸入密碼。只是，createuser 會浪費連線嘗試，為了發現伺服器需要密碼。在某些情況下，值得輸入 -W 以避免額外的連線嘗試。

### 環境變數

`PGHOST`\
`PGPORT`\
`PGUSER`

預設連線參數

與大多數其他 PostgreSQL 工具程式一樣，此工具也使用 libpq 支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

### 例外

如果遇到困難，請參閱 CREATE ROLE 和 psql 以討論潛在問題和錯誤訊息。資料庫伺服器必須在目標主機上運行。此外，將套用 libpq 前端函式庫使用的任何預鉆水連線設定和環境變數。

### 範例

要在預設的資料庫伺服器上建立使用者 joe：

```
$ createuser joe
```

要在預設的資料庫伺服器上建立使用者 joe，並提示輸入一些其他的屬性：

```
$ createuser --interactive joe
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

要使用主機 eden 上的伺服器（連接埠 5000）建立相同的使用者 joe，並明確指定屬性，屬性請查看基礎指令：

```
$ createuser -h eden -p 5000 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
```

要以超級使用者身份建立使用者 joe，並立即指定密碼：

```
$ createuser -P -s -e joe
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE joe PASSWORD 'md5b5f5ba1a423792b526f799ae4eb3d59e' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
```

在上面的範例中，新密碼在鍵入時實際上並未顯示，但為了清楚起見，我們顯示了鍵入的內容。如您所見，密碼在發送到用戶端之前已經加密過。

### 參閱

[dropuser](dropuser.md), [CREATE ROLE](../sql-commands/create-role.md)
