<a id="id-1.9.3.153.1"></a>

## LISTEN

LISTEN — 監聽通知

## 語法

```

LISTEN channel
```

<a id="id-1.9.3.153.5"></a>

## 說明

`LISTEN` 會將目前的工作階段註冊為名為 *`channel`* 的通知頻道之監聽者。若目前的工作階段已註冊為此通知頻道的監聽者，則不做任何事。

每當這個工作階段或連線到同一資料庫的另一個工作階段呼叫 `NOTIFY channel` 指令時，目前所有正在監聽該通知頻道的工作階段都會收到通知，而每個工作階段接著又會通知其所連接的用戶端應用程式。

可以使用 `UNLISTEN` 指令取消某個工作階段對指定通知頻道的註冊。當工作階段結束時，該工作階段的監聽註冊會自動清除。

用戶端應用程式偵測通知事件所須使用的方法，取決於它所使用的 PostgreSQL 應用程式設計介面。使用 libpq 函式庫時，應用程式會像一般 SQL 指令那樣發出 `LISTEN`，然後必須定期呼叫函式 `PQnotifies`，以得知是否已收到任何通知事件。其他介面，例如 libpgtcl，則提供了處理通知事件的更高階方法；事實上，使用 libpgtcl 時，應用程式開發者甚至不應該直接發出 `LISTEN` 或 `UNLISTEN`。詳情請參閱你所使用介面的相關文件。

<a id="id-1.9.3.153.6"></a>

## 參數

*`channel`*
:   通知頻道的名稱（任意識別字）。

<a id="id-1.9.3.153.7"></a>

## 注意事項

`LISTEN` 會在交易提交時生效。若 `LISTEN` 或 `UNLISTEN` 是在稍後回復（roll back）的交易中執行，則正在監聽的通知頻道集合不會有任何變化。

已執行過 `LISTEN` 的交易，無法為兩階段提交準備（prepare）。

初次設定監聽工作階段時，存在一個競態條件：若有正在並行提交的交易正在傳送通知事件，新設定的監聽工作階段究竟會收到其中哪些通知？答案是：該工作階段會收到在該交易提交步驟中某一瞬間之後所提交的所有事件。但這個時間點會比該交易在查詢中所能觀察到的任何資料庫狀態都稍晚一些。由此可得出使用 `LISTEN` 的下列原則：先執行（並且提交！）該指令，接著在新的交易中依應用程式邏輯所需檢視資料庫狀態，然後才依賴通知來得知資料庫狀態的後續變化。一開始收到的少數幾個通知，可能是關於在最初的資料庫檢視中已經觀察到的更新，但這通常無傷大雅。

[NOTIFY](sql-notify.md) 對 `LISTEN` 與 `NOTIFY` 的使用方式有更詳盡的討論。

<a id="id-1.9.3.153.8"></a>

## 範例

在 psql 中設定並執行一段 listen/notify 序列：

```

LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

<a id="id-1.9.3.153.9"></a>

## 相容性

SQL 標準中沒有 `LISTEN` 陳述式。

<a id="id-1.9.3.153.10"></a>

## 另請參閱

[NOTIFY](sql-notify.md), [UNLISTEN](sql-unlisten.md), [max_notify_queue_pages](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-NOTIFY-QUEUE-PAGES)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-listen.html)（原文版本：18.6；核對日期：2026-09-28）
