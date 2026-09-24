<a id="SERVER-START"></a>

## 18.3. 啟動資料庫伺服器 [#](#SERVER-START)

[18.3.1. 伺服器啟動失敗](server-start.md#SERVER-START-FAILURES)

[18.3.2. 用戶端連線問題](server-start.md#CLIENT-CONNECTION-PROBLEMS)

在任何人能夠存取資料庫之前，您必須先啟動資料庫伺服器。
資料庫伺服器程式稱為
`postgres`。<a id="id-1.6.5.6.2.2"></a>

若您使用的是預先封裝的 PostgreSQL 版本，
它幾乎必定包含了依照您作業系統慣例、
以背景工作方式執行伺服器的相關設定。使用套件所提供的
基礎架構來啟動伺服器，會比自行摸索容易得多。
詳情請參閱套件層級的相關文件。

手動啟動伺服器最基本的方式，就是直接呼叫
`postgres`，並以 `-D` 選項，
指定資料目錄的位置，例如：

```

$ postgres -D /usr/local/pgsql/data
```

這會讓伺服器在前景執行。此操作必須在登入
PostgreSQL 使用者帳號的狀態下進行。若未指定
`-D`，伺服器會嘗試使用環境變數
`PGDATA` 所指名的資料目錄。若也未提供該變數，
則會執行失敗。

一般而言，將 `postgres` 放到背景執行會比較好。
若要這麼做，可使用一般的 Unix shell 語法：

```

$ postgres -D /usr/local/pgsql/data >logfile 2>&1 &
```

如上所示，將伺服器的 stdout 與 stderr 輸出
儲存到某處相當重要。這有助於稽核，
也有助於診斷問題。（關於日誌檔處理方式的更完整討論，
請參閱[24.3 節](../maintenance/logfile-maintenance.md)。）

`postgres` 程式還接受許多其他命令列選項。
更多資訊請參閱
[postgres](../../reference/reference-server/app-postgres.md) 參考頁面，
以及下方的[第 19 章](../runtime-config/README.md)。

這種 shell 語法很快就會變得繁瑣。因此，
系統提供了包裝程式
[pg_ctl](../../reference/reference-server/app-pg-ctl.md)<a id="id-1.6.5.6.7.2"></a>，
以簡化部分工作。舉例來說：

```

pg_ctl start -l logfile
```

會在背景啟動伺服器，並將輸出放入指定的日誌檔中。
此處的 `-D` 選項，與 `postgres`
的意義相同。`pg_ctl` 也能夠停止伺服器。

一般而言，您會希望在電腦開機時，
啟動資料庫伺服器。<a id="id-1.6.5.6.8.1"></a>
自動啟動指令碼，會因作業系統而異。
PostgreSQL 隨附了一些範例指令碼，
位於 `contrib/start-scripts` 目錄中。
安裝其中任何一個，都需要 root 權限。

不同的系統，在開機時啟動守護程序（daemon）的慣例也不同。
許多系統有一個 `/etc/rc.local`
或 `/etc/rc.d/rc.local` 檔案。其他系統
則使用 `init.d` 或 `rc.d` 目錄。
無論您採用哪種做法，伺服器都必須以
PostgreSQL 使用者帳號執行，
*而非以 root 或任何其他使用者身分*執行。
因此，您可能應該以
`su postgres -c '...'` 的形式，
組成您的指令。例如：

```

su postgres -c 'pg_ctl start -D /usr/local/pgsql/data -l serverlog'
```

以下再提供一些依作業系統而異的建議。
（在每個範例中，請務必將我們所展示的通用值，
換成正確的安裝目錄與使用者名稱。）

* 若為 FreeBSD，請參閱 PostgreSQL 原始碼發行版中的
  `contrib/start-scripts/freebsd` 檔案。
  <a id="id-1.6.5.6.10.1.1.1.4"></a>
* 在 OpenBSD 上，將以下幾行加入
  `/etc/rc.local` 檔案：
  <a id="id-1.6.5.6.10.1.2.1.3"></a>

  ```

  if [ -x /usr/local/pgsql/bin/pg_ctl -a -x /usr/local/pgsql/bin/postgres ]; then
      su -l postgres -c '/usr/local/pgsql/bin/pg_ctl start -s -l /var/postgresql/log -D /usr/local/pgsql/data'
      echo -n ' postgresql'
  fi
  ```
* 在 Linux 系統上，可以將
  <a id="id-1.6.5.6.10.1.3.1.2"></a>

  ```

  /usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data
  ```

  加入 `/etc/rc.d/rc.local`
  或 `/etc/rc.local`，也可以參閱 PostgreSQL
  原始碼發行版中的 `contrib/start-scripts/linux` 檔案。

  若使用 systemd，您可以使用以下服務單元檔（service unit file）
  （例如放置於
  `/etc/systemd/system/postgresql.service`）：<a id="id-1.6.5.6.10.1.3.2.3"></a>

  ```

  [Unit]
  Description=PostgreSQL database server
  Documentation=man:postgres(1)
  After=network-online.target
  Wants=network-online.target

  [Service]
  Type=notify
  User=postgres
  ExecStart=/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data
  ExecReload=/bin/kill -HUP $MAINPID
  KillMode=mixed
  KillSignal=SIGINT
  TimeoutSec=infinity

  [Install]
  WantedBy=multi-user.target
  ```

  使用 `Type=notify` 時，要求伺服器執行檔，
  必須以 `configure --with-systemd` 選項建置而成。

  請仔細考量逾時設定。截至撰寫本文為止，
  systemd 的預設逾時時間為 90 秒，
  若程序在此時間內未回報就緒狀態，就會將其終止。
  但可能需要在啟動時執行當機復原的 PostgreSQL
  伺服器，可能需要更長的時間才能就緒。
  建議的值 `infinity`，會停用此逾時邏輯。
* 在 NetBSD 上，可依個人偏好，
  使用 FreeBSD 或 Linux 的啟動指令碼。
  <a id="id-1.6.5.6.10.1.4.1.4"></a>
* 在 Solaris 上，請建立一個名為
  `/etc/init.d/postgresql` 的檔案，
  內容包含以下這一行：
  <a id="id-1.6.5.6.10.1.5.1.3"></a>

  ```

  su - postgres -c "/usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data"
  ```

  接著，在 `/etc/rc3.d` 中，
  建立一個指向該檔案、名為 `S99postgresql`
  的符號連結。

伺服器執行期間，其 PID 會儲存在資料目錄中的
`postmaster.pid` 檔案裡。這是用來
防止同一個資料目錄中，同時執行多個伺服器實體，
也可用於關閉伺服器。

<a id="SERVER-START-FAILURES"></a>

### 18.3.1. 伺服器啟動失敗 [#](#SERVER-START-FAILURES)

伺服器可能無法啟動，有幾個常見的原因。請檢查伺服器的
日誌檔，或手動啟動伺服器（不重新導向標準輸出或標準錯誤），
查看出現了哪些錯誤訊息。以下我們會更詳細地說明，
一些最常見的錯誤訊息。

```

LOG:  could not bind IPv4 address "127.0.0.1": Address already in use
HINT:  Is another postmaster already running on port 5432? If not, wait a few seconds and retry.
FATAL:  could not create any TCP/IP sockets
```

這通常正如訊息所暗示的：您嘗試在某個已有伺服器
執行中的相同連接埠上，啟動另一個伺服器。不過，
若核心的錯誤訊息並非 `Address already in use`
或其類似變體，可能就是另有其他問題。舉例來說，
嘗試在保留連接埠編號上啟動伺服器，
可能會出現類似以下的訊息：

```

$ postgres -p 666
LOG:  could not bind IPv4 address "127.0.0.1": Permission denied
HINT:  Is another postmaster already running on port 666? If not, wait a few seconds and retry.
FATAL:  could not create any TCP/IP sockets
```

類似以下的訊息：

```

FATAL:  could not create shared memory segment: Invalid argument
DETAIL:  Failed system call was shmget(key=5440001, size=4011376640, 03600).
```

很可能表示，您核心對共享記憶體大小的限制，
小於 PostgreSQL 嘗試建立的工作區域
（在此範例中為 4011376640 位元組）。這種情況，
只有在您已將 `shared_memory_type`
設定為 `sysv` 時，才比較可能發生。
在這種情況下，您可以嘗試以少於平常數量的緩衝區
（[shared_buffers](../runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS)）
啟動伺服器，或者重新設定您的核心，
以增加允許的共享記憶體大小。若您嘗試在同一部機器上，
啟動多個伺服器，且它們所要求的總空間，
超過了核心限制，您也可能看到這則訊息。

類似以下的錯誤：

```

FATAL:  could not create semaphores: No space left on device
DETAIL:  Failed system call was semget(5440126, 17, 03600).
```

*並不*代表您的磁碟空間已耗盡。它的意思是，
您核心對 System V 號誌（semaphore）數量的限制，
小於 PostgreSQL 想要建立的數量。如同前述情況，
您或許可以透過以較少的允許連線數
（[max_connections](../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)）
啟動伺服器，暫時解決此問題，但最終您還是需要
提高核心限制。

關於設定 System V IPC 機制的詳細資訊，
請參閱[18.4.1 節](kernel-resources.md#SYSVIPC)。

<a id="CLIENT-CONNECTION-PROBLEMS"></a>

### 18.3.2. 用戶端連線問題 [#](#CLIENT-CONNECTION-PROBLEMS)

雖然用戶端可能出現的錯誤狀況相當多樣，且因應用程式而異，
但其中有幾種，可能與伺服器啟動的方式直接相關。
除了以下所展示的狀況之外，其他狀況應該會記載於
各自用戶端應用程式的文件中。

```

psql: error: connection to server at "server.joe.com" (123.123.123.123), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

這是一則通用的「找不到可交談的伺服器」失敗訊息。
在嘗試 TCP/IP 通訊時，就會出現如上所示的訊息。
常見的錯誤，是忘記設定
[listen_addresses](../runtime-config/runtime-config-connection.md#GUC-LISTEN-ADDRESSES)，
導致伺服器無法接受遠端 TCP 連線。

此外，在嘗試對本機伺服器進行 Unix 網域 socket 通訊時，
您也可能看到以下訊息：

```

psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?
```

若伺服器確實正在執行，請檢查用戶端所認定的
socket 路徑（此處為 `/tmp`），
是否與伺服器的
[unix_socket_directories](../runtime-config/runtime-config-connection.md#GUC-UNIX-SOCKET-DIRECTORIES)
設定一致。

連線失敗訊息，一律會顯示伺服器位址或 socket 路徑名稱，
這有助於確認用戶端是否嘗試連向正確的位置。若該處
實際上並沒有伺服器正在聆聽，核心的錯誤訊息，
通常會是 `Connection refused`，
或 `No such file or directory`，如上所示。（必須了解的是，在此情境下，
`Connection refused` 並*不*代表
伺服器收到了您的連線請求並加以拒絕。那種情況，
會產生另一則不同的訊息，如
[20.16 節](../client-authentication/client-authentication-problems.md)所示。）
其他錯誤訊息，例如 `Connection timed out`，
則可能表示更根本的問題，例如網路連線不通，
或防火牆阻擋了連線。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/server-start.html)（原文版本：18.6；核對日期：2026-09-24）
