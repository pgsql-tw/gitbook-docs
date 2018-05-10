# LOAD

LOAD — 載入共享函式庫檔案

### 語法

```text
LOAD 'filename'
```

### 說明

此命令將共享函式庫檔案載入到 PostgreSQL 伺服器的定址空間中。如果檔案已經被載入，那麼此命令就不會進行任何操作。包含 C 函數的共享函式庫檔案只要呼叫其中一個函數就會自動載入。因此，LOAD 通常只需要載入一個透過「hook」修改伺服器行為而不是提供一組函數的函式庫。

函式庫檔案名通常只是一個檔案名稱，在伺服器的函式庫搜尋路徑（由 [dynamic\_library\_path](../../server-administration/runtime-config/runtime-config-client.md#19-11-4-qi-ta-ding-ji-qi-zhi) 設定）中尋找。或者，它可以以完整的路徑名稱給予。無論哪種情況，平台的標準共享庫文件延伸名稱都可以省略。有關該主題的更多訊息，請參閱[第 37.9.1 節](../../server-programming/extending-sql/c-language-functions.md#37-9-1-dynamic-loading)。

非超級使用者只能將 LOAD 用於位於 $libdir/plugins/ 中的函式庫檔案 - 指定的檔案名稱必須以該字串開頭。（資料庫管理員有責任確保在那裡只安裝「安全」函式庫。）

### 相容性

`LOAD`是 PostgreSQL 的延伸功能。

### 參閱

[CREATE FUNCTION](create-function.md)

