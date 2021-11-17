# dropuser

dropuser — 移除 PostgreSQL 使用者帳戶

### 語法

`dropuser` \[_`connection-option`_...] \[_`option`_...] \[_`username`_]

### 說明

dropuser 移除現有的 PostgreSQL 使用者。只有具有 CREATEROLE 權限的超級使用者或一般使用者才能移除 PostgreSQL 使用者。（但要移除超級使用者，您還必須自己是超級使用者。）

dropuser 是 SQL 指令 [DROP ROLE](../sql-commands/drop-role.md) 的一個封裝。透過此實用工具和透過存取伺服器的其他方法移除使用者，之間沒有區別。

### 參數

dropuser 接受以下的命令列參數：

_`username`_

指定要移除的 PostgreSQL 使用者的名稱。如果在命令列中沒有指定名稱，則會提示您輸入名稱，如同使用 -i / -interactive。

`-e`\
`--echo`

顯示 dropuser 發送到伺服器的指令。

`-i`\
`--interactive`

在實際移除使用者之前提示確認，如果沒有在命令列中指定使用者名稱，會提示輸入。

`-V`\
`--version`

輸出 dropuser 版本然後退出。

`--if-exists`

如果使用者不存在，請不要拋出錯誤。在這種情況下發布 NOTICE。

`-?`\
`--help`

顯示有關 dropuser 命令列參數的說明，然後退出。

dropuser 還接受連線有關的以下命令列參數：

`-h `_`host`_\
`--host=`_`host`_

指定運行伺服器的主機名。如果以斜線開頭，則將其視為 Unix domain socket 的目錄。

`-p `_`port`_\
`--port=`_`port`_

指定伺服器正在監聽連線的 TCP 連接埠或本地 Unix domain socket 檔案延伸名稱。

`-U `_`username`_\
`--username=`_`username`_

要連線的使用者名稱（不是要移除的使用者名稱）。

`-w`\
`--no-password`

避免發出密碼提示。如果伺服器需要密碼驗證，請透過其他方式（如 .pgpass 檔案），無法使用密碼的話，則連線嘗試將會失敗。此選項可用於沒有使用者輸入密碼的批次處理作業和腳本。

`-W`\
`--password`

強制 dropuser 在連線到資料庫之前提示輸入密碼。

此選項從來不是必須的，因為如果伺服器需要密碼認證，dropuser 將自動提示輸入密碼。然而，dropuser 會浪費連線嘗試發現伺服器想要密碼。在某些情況下，值得輸入 -W 以避免額外的連線嘗試。

### 環境變數

`PGHOST`\
`PGPORT`\
`PGUSER`

預設連線參數

與其他大多數 PostgreSQL 實用工具一樣，此工具也使用 libpq 支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

### 診斷

如果遇到困難，請參閱 [DROP ROLE](../sql-commands/drop-role.md) 和 [psql](psql.md)，以便討論潛在問題和錯誤訊息。資料庫伺服器必須在目標主機上運行。此外，libpq 前端函式庫使用的任何預設連線設定和環境變數都將適用。

### 範例

要從預設資料庫伺服器中移除使用者 joe：

```
$ dropuser joe
```

使用主機 eden 的連接埠 5000 上的服務移除使用者 joe，驗證並查看基礎指令：

```
$ dropuser -p 5000 -h eden -i -e joe
Role "joe" will be permanently removed.
Are you sure? (y/n) y
DROP ROLE joe;
```

### 參閱

[createuser](createuser.md), [DROP ROLE](../sql-commands/drop-role.md)
