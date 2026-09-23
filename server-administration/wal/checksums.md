<a id="CHECKSUMS"></a>

## 28.2. 資料校驗和 [#](#CHECKSUMS)

[28.2.1. 離線啟用校驗和](checksums.md#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

<a id="id-1.6.15.4.2"></a>

依預設，資料頁面會受到校驗和（checksum）保護，但也可以選擇針對某個
叢集停用此功能。啟用後，每個資料頁面都會包含一組校驗和，
該校驗和會在頁面寫入時更新，並在每次讀取頁面時進行驗證。只有資料頁面
會受到校驗和保護；內部資料結構與暫存檔案則不會。

校驗和可以在使用 [initdb](../../reference/reference-server/app-initdb.md#APP-INITDB-DATA-CHECKSUMS) 初始化叢集時停用。
之後也可以透過離線操作，在事後啟用或停用校驗和。資料校驗和是在
整個叢集層級啟用或停用，無法針對個別資料庫或資料表分別指定。

叢集中校驗和目前的狀態，可以透過檢視唯讀組態變數
[data_checksums](../runtime-config/runtime-config-preset.md#GUC-DATA-CHECKSUMS) 的值來確認，
方法是執行 `SHOW data_checksums` 指令。

在嘗試從頁面損毀中復原時，可能有必要略過校驗和保護。若要這麼做，
可以暫時設定組態參數
[ignore_checksum_failure](../runtime-config/runtime-config-developer.md#GUC-IGNORE-CHECKSUM-FAILURE)。

<a id="CHECKSUMS-OFFLINE-ENABLE-DISABLE"></a>

### 28.2.1. 離線啟用校驗和 [#](#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

[pg_checksums](../../reference/reference-server/app-pgchecksums.md)
應用程式可用來針對離線叢集啟用或停用資料校驗和，也可以用來驗證校驗和。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/checksums.html)（原文版本：18.6；核對日期：2026-09-22）
