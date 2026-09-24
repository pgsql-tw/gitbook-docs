<a id="SERVER-SHUTDOWN"></a>

## 18.5. 關閉伺服器 [#](#SERVER-SHUTDOWN)

<a id="id-1.6.5.8.2"></a>

關閉資料庫伺服器的方式有很多種。從底層來看，
這些方式最終都會歸結為：向監督者（supervisor）
`postgres` 程序發送一個信號。

若您使用的是預先封裝的 PostgreSQL 版本，
且您使用了其所提供的方式來啟動伺服器，那麼您也應該
使用其提供的方式來停止伺服器。詳情請參閱套件層級的
相關文件。

在直接管理伺服器時，您可以透過向
`postgres` 程序發送不同的信號，
來控制關閉的方式：

SIGTERM<a id="id-1.6.5.8.5.2.1.1.2"></a>
:   這是*智慧關閉*（Smart Shutdown）模式。
    收到 SIGTERM 之後，伺服器會拒絕新的連線，
    但仍讓既有的工作階段正常完成其工作。
    只有在所有工作階段都終止之後，才會關閉。
    若伺服器在收到智慧關閉請求時正處於復原狀態，
    則只有在所有一般工作階段都終止之後，
    才會停止復原與串流複寫。

SIGINT<a id="id-1.6.5.8.5.2.2.1.2"></a>
:   這是*快速關閉*（Fast Shutdown）模式。
    伺服器會拒絕新的連線，並向所有既有的伺服器程序，
    發送 SIGTERM，這會導致它們中止目前的交易，
    並儘速結束。接著，伺服器會等待所有伺服器程序結束，
    最後才關閉。

SIGQUIT<a id="id-1.6.5.8.5.2.3.1.2"></a>
:   這是*立即關閉*（Immediate Shutdown）模式。
    伺服器會向所有子程序發送 SIGQUIT，
    並等待它們終止。若有任何程序在 5 秒內
    未能終止，就會對其發送 SIGKILL。
    一旦所有子程序都已結束，監督者伺服器程序
    就會立即結束，而不會執行正常的資料庫關閉處理程序。
    這會導致下次啟動時進行復原
    （透過重播 WAL 日誌）。僅建議在緊急情況下使用此模式。

[pg_ctl](../../reference/reference-server/app-pg-ctl.md) 程式，
提供了一個方便的介面，可用來發送這些信號以關閉伺服器。
此外，在非 Windows 系統上，您也可以直接使用
`kill` 發送信號。`postgres`
程序的 PID，可以使用 `ps` 程式查詢，
或從資料目錄中的 `postmaster.pid` 檔案取得。
舉例來說，若要執行快速關閉：

```

$ kill -INT `head -1 /usr/local/pgsql/data/postmaster.pid`
```

### 重要事項

最好不要使用 SIGKILL 來關閉伺服器。這麼做
會導致伺服器無法釋放共享記憶體與號誌。此外，
SIGKILL 會直接終止 `postgres`
程序，而不讓它將該信號轉發給其子程序，
因此可能還需要手動終止個別的子程序。

若要終止個別的工作階段，同時讓其他工作階段繼續執行，
請使用 `pg_terminate_backend()`
（請參閱[表 9.96](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE)），
或者向與該工作階段關聯的子程序，
發送 SIGTERM 信號。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/server-shutdown.html)（原文版本：18.6；核對日期：2026-09-24）
