# RESET

RESET — 將執行時期參數的值還原為預設值

### 語法

```
RESET configuration_parameter
RESET ALL
```

### 說明

RESET 將執行時期參數恢復為其預設值。RESET 另一種寫法是

```
SET configuration_parameter TO DEFAULT
```

有關詳細訊息，請參閱 [SET](set.md)。

如果在目前連線中沒有為它發出 SET，則預設值被定義為參數將具有的值。此值的實際來源可能是已編譯的預設值、組態檔案、命令列選項或每個資料庫、每個使用者的預設設定。這與將其定義為「參數在連線開始時具有的值」略有不同，因為如果值來自組態檔案，它將被重置為組態檔案現在指定的值。詳細訊息請參閱[第 19 章](../../server-administration/server-configuration/)。

RESET 的事務行為與 SET 相同：事務回溯將撤消其效果。

### 參數

_`configuration_parameter`_

可設定的執行時期參數的名稱。可用參數說明在[第 19 章](../../server-administration/server-configuration/)和 [SET](set.md) 參考頁面中。

`ALL`

將所有可設定的執行時期參數重置為預設值。

### 範例

將 timezone 變數設定回其預設值：

```
RESET timezone;
```

### 相容性

RESET 是 PostgreSQL 的延伸功能。

### 參閱

[SET](set.md), [SHOW](show.md)
