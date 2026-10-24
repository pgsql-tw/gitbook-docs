<a id="LIBPQ-PGSERVICE"></a>

## 32.17. 連線服務檔 [#](#libpq-pgservice) <a href="#libpq-pgservice" id="libpq-pgservice"></a>

<a id="id-1.7.3.24.2"></a><a id="id-1.7.3.24.3"></a><a id="id-1.7.3.24.4"></a>

連線服務檔讓 libpq 連線參數可以與單一服務名稱建立關聯。之後即可在
libpq 連線字串中使用 `service` 關鍵字
指定該服務名稱，並套用與其關聯的設定。如此一來，修改連線參數時
不需要重新編譯使用 libpq 的應用程式。服務名稱也可以
透過 `PGSERVICE` 環境變數指定。

服務名稱可以定義在個別使用者的服務檔或全系統的服務檔中。
若同一個服務名稱同時存在於使用者服務檔與系統服務檔中，以使用者服務檔為優先。
預設情況下，個別使用者的服務檔名為
`~/.pg_service.conf`。
在 Microsoft Windows 上，其名稱為
`%APPDATA%\postgresql\.pg_service.conf`（其中
`%APPDATA%` 指的是使用者設定檔中的 Application Data 子目錄）。
可以透過設定環境變數 `PGSERVICEFILE` 指定不同的檔名。
全系統的服務檔名為 `pg_service.conf`。
預設會在 PostgreSQL 安裝目錄的
`etc` 目錄中尋找此檔
（可使用 `pg_config --sysconfdir` 精確找出此
目錄）。可以透過設定環境變數
`PGSYSCONFDIR` 指定另一個目錄，但無法指定不同的檔名。

兩種服務檔都使用「INI 檔」格式，其中區段名稱為服務名稱，
參數則為連線參數；參數清單請參閱[第 32.1.2 節](libpq-connect.md#libpq-paramkeywords)。
例如：

```

# comment
[mydb]
host=somehost
port=5433
user=admin
```

PostgreSQL 安裝目錄中提供了一個範例檔：
`share/pg_service.conf.sample`。

從服務檔取得的連線參數會與從其他來源取得的參數合併。
服務檔中的設定會覆寫對應的環境變數，而服務檔的設定又可以
被連線字串中直接給定的值覆寫。
例如，使用上述服務檔時，連線字串
`service=mydb port=5434` 會使用
主機 `somehost`、連接埠 `5434`、
使用者 `admin`，其他參數則依
環境變數或內建預設值設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-pgservice.html)（原文版本：18.6；核對日期：2026-10-17）
