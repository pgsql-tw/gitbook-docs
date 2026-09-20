<a id="LOGICALDECODING-SYNCHRONOUS"></a>
## 47.8. 邏輯解碼的同步複寫支援 [#](#LOGICALDECODING-SYNCHRONOUS)

[47.8.1. 概觀](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

[47.8.2. 注意事項](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

<a id="LOGICALDECODING-SYNCHRONOUS-OVERVIEW"></a>

### 47.8.1. 概觀 [#](#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

邏輯解碼可以用來建構[同步複寫](../../server-administration/high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION)解決方案，其使用者介面與[串流複寫](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)的同步複寫相同。要做到這一點，必須使用串流複寫介面（見[第 47.3 節](logicaldecoding-walsender.md)）來串流輸出資料。用戶端必須傳送 `Standby status update (F)` 訊息（見[第 54.4 節](../../internals/protocol/protocol-replication.md)），就像串流複寫用戶端所做的那樣。

### 注意

透過邏輯解碼接收變更的同步備援副本，其作用範圍僅限於單一資料庫。然而 *`synchronous_standby_names`* 目前是整個伺服器層級的設定，因此如果同時有多個資料庫在使用中，這項技術就無法正常運作。

<a id="LOGICALDECODING-SYNCHRONOUS-CAVEATS"></a>

### 47.8.2. 注意事項 [#](#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

在同步複寫的設定中，如果交易以互斥方式鎖定了［使用者的］目錄資料表，就可能發生死結。關於使用者目錄資料表的資訊，請參閱[第 47.6.2 節](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)。這是因為交易的邏輯解碼在存取目錄資料表時，可能會對它們加鎖。為了避免這種情況，使用者必須避免對［使用者的］目錄資料表取得互斥鎖定。以下幾種方式都可能導致這個問題：

* 在交易中對 `pg_class` 發出明確的 `LOCK`。
* 在交易中對 `pg_class` 執行 `CLUSTER`。
* 對 `pg_class` 執行 `LOCK` 命令後接著執行 `PREPARE TRANSACTION`，並允許對兩階段交易進行邏輯解碼。
* 對 `pg_trigger` 執行 `CLUSTER` 命令後接著執行 `PREPARE TRANSACTION`，並允許對兩階段交易進行邏輯解碼。只有在發佈的資料表擁有觸發程序時，這才會導致死結。
* 在交易中對［使用者的］目錄資料表執行 `TRUNCATE`。

請注意，這些命令不只會對上面列出的系統目錄資料表造成死結，對其他目錄資料表也可能造成死結。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-synchronous.html)（原文版本：18.6；核對日期：2026-09-15）
