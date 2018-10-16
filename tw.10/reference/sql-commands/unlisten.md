# UNLISTEN

UNLISTEN — 停止監聽通知

### 語法

```text
UNLISTEN { channel | * }
```

### 說明

UNLISTEN 用於移除現有已註冊的 NOTIFY 事件。UNLISTEN 取消目前 PostgreSQL 連線的任何現有註冊，名稱為 channel 的通知通道上的監聽器。特殊符號 \* 為取消目前連線已註冊的所有監聽器。

[NOTIFY](notify.md) 包含了對 LISTEN 和 NOTIFY 使用上更廣泛的討論。

### 參數

_`channel`_

通知通道的名稱（任何標識字）。

`*`

清除此連線目前已註冊的所有監聽。

### 注意

你可以取消你不要監聽的東西；不會出現警告或錯誤。

在每個連線結束時，UNLISTEN \* 會自動執行。

已執行 UNLISTEN 的事務無法為兩階段提交做準備。

### 範例

進行註冊：

```text
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

一旦執行了 UNLISTEN，將忽略之後的 NOTIFY 訊息：

```text
UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

### 相容性

SQL 標準中沒有 UNLISTEN 指令。

### 參閱

[LISTEN](listen.md), [NOTIFY](notify.md)

