<a id="LIBPQ-THREADING"></a>

## 32.21. 多執行緒程式中的行為 [#](#libpq-threading) <a href="#libpq-threading" id="libpq-threading"></a>

<a id="id-1.7.3.28.2"></a>

從版本 17 起，libpq 一律是可重入（reentrant）且執行緒安全的。不過，有一項限制：不可有兩個執行緒同時嘗試操作同一個 `PGconn` 物件。特別是，你不能從不同的執行緒透過同一個連線物件發出並行的命令。（如果需要執行並行的命令，請使用多個連線。）

`PGresult` 物件在建立之後通常是唯讀的，因此可以在執行緒之間自由傳遞。不過，如果你使用了[第 32.12 節](libpq-misc.md)或[第 32.14 節](libpq-events.md)中所述任何會修改 `PGresult` 的函式，那麼避免對同一個 `PGresult` 進行並行操作，也是你的責任。

在較早的版本中，libpq 可以依編譯器選項編譯為支援或不支援執行緒。下面這個函式可用來查詢 libpq 的執行緒安全狀態：

<a id="LIBPQ-PQISTHREADSAFE"></a>

### `PQisthreadsafe`<a id="id-1.7.3.28.6.1.1.2"></a> [#](#libpq-pqisthreadsafe) <a href="#libpq-pqisthreadsafe" id="libpq-pqisthreadsafe"></a>

傳回 libpq 函式庫的執行緒安全狀態。

```

    int PQisthreadsafe();
```

若 libpq 是執行緒安全的則傳回 1，否則傳回 0。在版本 17 以上一律傳回 1。

已棄用的函式 [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) 與 [`PQoidStatus`](libpq-exec.md#LIBPQ-PQOIDSTATUS) 不是執行緒安全的，不應在多執行緒程式中使用。[`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) 可以用 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 取代。[`PQoidStatus`](libpq-exec.md#LIBPQ-PQOIDSTATUS) 可以用 [`PQoidValue`](libpq-exec.md#LIBPQ-PQOIDVALUE) 取代。

如果你在應用程式中使用 Kerberos（除了 libpq 內部使用之外），你需要在 Kerberos 呼叫的前後進行鎖定，因為 Kerberos 函式不是執行緒安全的。請參閱 libpq 原始碼中的函式 `PQregisterThreadLock`，了解如何在 libpq 與你的應用程式之間進行協同鎖定。

同樣地，如果你在應用程式中使用 Curl，*而且*在啟動新執行緒之前尚未[全域初始化 libcurl](https://curl.se/libcurl/c/curl_global_init.html)，你需要在任何可能初始化 libcurl 的程式碼前後進行協同鎖定（同樣是透過 `PQregisterThreadLock`）。對於建置時已支援執行緒安全初始化的較新版 Curl，這項限制不再適用；這類建置可以從其版本中繼資料是否宣告 `threadsafe` 功能來辨識。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-threading.html)（原文版本：18.6；核對日期：2026-10-17）
