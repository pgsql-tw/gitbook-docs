# ALTER SYSTEM

ALTER SYSTEM — 變更伺服器組態設定

### 語法

```
ALTER SYSTEM SET configuration_parameter { TO | = } { value | 'value' | DEFAULT }

ALTER SYSTEM RESET configuration_parameter
ALTER SYSTEM RESET ALL
```

### 說明

ALTER SYSTEM 用於變更整個資料庫叢集的伺服器組態參數。它比手動編輯 postgresql.conf 檔案的傳統方法更為方便。ALTER SYSTEM 將設定的參數設定寫入到 postgresql.auto.conf 檔案中，該檔案是在 postgresql.conf 之外讀取的。將參數設定為 DEFAULT 或使用 RESET 變體，將從 postgresql.auto.conf 檔案中刪除該設定項目。使用 RESET ALL 刪除所有此類設定項目。

在下一次伺服器組態重新載入之後，或者對於只能在伺服器啟動時變更的參數，在下一次伺服器重新啟動之後，使用 ALTER SYSTEM 設定的值將會生效。可以透過呼叫 SQL 函數 pg\_reload\_conf()，執行 pg\_ctl reload 或向主伺服器程序發送 SIGHUP 信號來命令伺服器組態重新載入。

只有超級使用者才能使用 ALTER SYSTEM。另外，由於此命令直接作用於檔案系統且無法回溯，因此不允許在交易區塊或函數內部使用此指令。

### 參數

_`configuration_parameter`_

可設定的組態參數的名稱。可用參數的說明在[第 19 章](../../server-administration/server-configuration/)之中。

_`value`_

參數的新值。可以將值指定為字串常數、指標、數字或以逗號分隔的列表，配合參數的要求。可以使用 DEFAULT 以從 postgresql.auto.conf 中刪除參數及其值。

### 注意

此命令不能用於設定 [data\_directory](../../server-administration/server-configuration/file-locations.md#data\_directory-string)，也不能用於設定 postgresql.conf 中不允許的參數（例如，[preset options](../../server-administration/server-configuration/19.15.-yu-xian-pei-zhi-de-can-shu.md)）。

有關其他設定參數的方法，請參閱[第 19.1 節](../../server-administration/server-configuration/setting-parameters.md)。

### 範例

設定 wal\_level：

```
ALTER SYSTEM SET wal_level = replica;
```

取消該設定，恢復在 postgresql.conf 中的設定：

```
ALTER SYSTEM RESET wal_level;
```

### 相容性

ALTER SYSTEM 語句是 PostgreSQL 的延伸功能。

### 參閱

[SET](set.md), [SHOW](show.md)
