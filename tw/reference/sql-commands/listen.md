# LISTEN

LISTEN — 監聽某個通知

### 語法

```text
LISTEN channel
```

### 說明

LISTEN 將目前連線註冊為名為 channel 的通知通道上的監聽器。如果目前連線已註冊為此通知通道的監聽器，則不執行任何操作。

無論何時透過此連線或連線到同一資料庫的另一個連線呼叫指令 NOTIFY 通道，都會通知目前正在該通知通道上監聽的所有連線，並且每個連線將依次通知其連線的用戶端應用程序。

可以使用 UNLISTEN 指令為給定通知通道取消註冊連線。連線結束時會自動清除連線的監聽註冊。

用戶端應用程序必須用於檢測通知事件的方法取決於它使用的 PostgreSQL 應用程序程式介面。使用 libpq 函式庫，應用程序將 LISTEN 作為普通 SQL 指令送出，然後必須定期呼叫函數 PQnotifies 以查明是否已收到任何通知事件。其他介面（如 libpgtcl）提供了處理通知事件的更高階的方法；實際上，使用 libpgtcl，應用程式設計師甚至不應該直接送出 LISTEN 或 UNLISTEN。有關更多詳細訊息，請參閱所用介面的使用手冊。

[NOTIFY](notify.md) 包含對 LISTEN 及 NOTIFY 使用的更廣泛討論。

### 參數

_`channel`_

通知通道的名稱（任何識別指標）。

### 注意

LISTEN 在事務提交時生效。如果在稍後回復的事務中執行 LISTEN 或 UNLISTEN，則正在監聽的通知通道也不會改變。

已執行 LISTEN 的事務無法為兩階段提交做 prepared。

### 範例

從 psql 配置並執行 listen / notify 指令：

```text
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

### 相容性

SQL 標準中沒有 LISTEN 語句。

### 參閱

[NOTIFY](notify.md), [UNLISTEN](unlisten.md)

