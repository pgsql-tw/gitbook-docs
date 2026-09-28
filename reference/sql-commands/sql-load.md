<a id="id-1.9.3.154.1"></a>

## LOAD

LOAD — 載入共享函式庫檔案

## 語法

```

LOAD 'filename'
```

<a id="SQL-LOAD-DESCRIPTION"></a>

## 說明

此指令會將共享函式庫檔案載入 PostgreSQL 伺服器的位址空間。若該檔案已經載入過，此指令則不做任何事。包含 C 函式的共享函式庫檔案，會在其中任一函式被呼叫時自動載入。因此，通常只有在要載入透過「掛鉤（hook）」而非提供一組函式來修改伺服器行為的函式庫時，才需要明確使用 `LOAD`。

函式庫檔案名稱通常只需給定一個單純的檔案名稱，系統會在伺服器的函式庫搜尋路徑（由 [dynamic_library_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH) 設定）中尋找。也可以改為給定完整路徑名稱。無論哪種方式，都可以省略該平台標準的共享函式庫檔案副檔名。關於此主題的更多資訊，請參閱[第 36.10.1 節](../../server-programming/extend/xfunc-c.md#XFUNC-C-DYNLOAD)。

<a id="id-1.9.3.154.5.4"></a>

非超級使用者只能對位於 `$libdir/plugins/` 的函式庫檔案套用 `LOAD` — 所指定的 *`filename`* 必須恰好以此字串開頭。（確保該處只安裝「安全」的函式庫，是資料庫管理員的責任。）

<a id="SQL-LOAD-COMPAT"></a>

## 相容性

`LOAD` 是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.154.7"></a>

## 另請參閱

[CREATE FUNCTION](sql-createfunction.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-load.html)（原文版本：18.6；核對日期：2026-09-28）
