# 18.4.1. 共享記憶體與號誌（Semaphore）

<a id="SYSVIPC"></a>

## 18.4.1. 共享記憶體與號誌（Semaphore） [#](#sysvipc) <a href="#sysvipc" id="sysvipc"></a>

<a id="id-1.6.5.7.3.2"></a><a id="id-1.6.5.7.3.3"></a>

PostgreSQL 要求作業系統提供程序間通訊
（inter-process communication，IPC）功能，具體而言，
就是共享記憶體與號誌。衍生自 Unix 的系統，
通常會提供「System V」IPC、「POSIX」IPC，
或兩者皆有。Windows 則有自己的實作方式，
本節不予討論。

依預設，PostgreSQL 會配置一小部分的 System V
共享記憶體，以及一大部分的匿名 `mmap` 共享記憶體。
或者，也可以改用單一一大塊的 System V 共享記憶體區域
（請參閱 [shared_memory_type](../../runtime-config/runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE)）。
此外，伺服器啟動時，還會建立相當數量的號誌，
可以是 System V 或 POSIX 樣式。目前，
Linux 與 FreeBSD 系統使用 POSIX 號誌，
其他平台則使用 System V 號誌。

System V IPC 功能，通常受到系統層級配置上限的限制。
當 PostgreSQL 超過這些限制之一時，
伺服器將拒絕啟動，並應留下一則說明問題內容
及處理方式的指示性錯誤訊息。（另請參閱
[18.3.1 節](../server-start.md#server-start-failures)。）
相關的核心參數，在不同系統上，命名方式相當一致；
[表 18.1](#sysvipc-parameters) 提供了概觀。
不過，設定這些參數的方法則各異。以下針對部分平台，
提供一些建議。

<a id="SYSVIPC-PARAMETERS"></a>

### 表 18.1. System V IPC 參數 [#](#sysvipc-parameters) <a href="#sysvipc-parameters" id="sysvipc-parameters"></a>

<table border="1" class="table" summary="System V IPC Parameters"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>說明</th><th>執行一份 <span class="productname">PostgreSQL</span> 實體所需的值</th></tr></thead><tbody><tr><td><code class="varname">SHMMAX</code></td><td>共享記憶體區段的最大大小（位元組）</td><td>至少 1kB，但預設值通常高出許多</td></tr><tr><td><code class="varname">SHMMIN</code></td><td>共享記憶體區段的最小大小（位元組）</td><td>1</td></tr><tr><td><code class="varname">SHMALL</code></td><td>可用共享記憶體的總量（位元組或頁面）</td><td>若以位元組為單位，與 <code class="varname">SHMMAX</code> 相同，
        若以頁面為單位，則為 <code class="literal">ceil(SHMMAX/PAGE_SIZE)</code>，
        再加上其他應用程式所需的空間</td></tr><tr><td><code class="varname">SHMSEG</code></td><td>每個程序所能使用的共享記憶體區段數上限</td><td>只需要 1 個區段，但預設值通常高出許多</td></tr><tr><td><code class="varname">SHMMNI</code></td><td>整個系統中共享記憶體區段數的上限</td><td>如同 <code class="varname">SHMSEG</code>，再加上其他應用程式所需的空間</td></tr><tr><td><code class="varname">SEMMNI</code></td><td>號誌識別碼（也就是集合）的數量上限</td><td>至少 <code class="literal">ceil(num_os_semaphores / 16)</code>，再加上其他應用程式所需的空間</td></tr><tr><td><code class="varname">SEMMNS</code></td><td>整個系統中號誌數的上限</td><td><code class="literal">ceil(num_os_semaphores / 16) * 17</code>，再加上其他應用程式所需的空間</td></tr><tr><td><code class="varname">SEMMSL</code></td><td>每個集合中號誌數的上限</td><td>至少 17</td></tr><tr><td><code class="varname">SEMMAP</code></td><td>號誌對應表中的項目數</td><td>請參閱內文</td></tr><tr><td><code class="varname">SEMVMX</code></td><td>號誌的最大值</td><td>至少 1000（預設值通常為 32767；除非必要，否則請勿變更）</td></tr></tbody></table>

<br>

伺服器的每一份複本，都需要用到少量的 System V
共享記憶體（在 64 位元平台上，通常為 48 位元組）。
在大多數現代作業系統上，這個數量都能輕易配置。
不過，若您同時執行伺服器的多份複本，
或明確地將伺服器設定為使用大量的 System V 共享記憶體
（請參閱
[shared_memory_type](../../runtime-config/runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE)
與
[dynamic_shared_memory_type](../../runtime-config/runtime-config-resource.md#GUC-DYNAMIC-SHARED-MEMORY-TYPE)），
就可能有必要增加 `SHMALL`，
也就是整個系統的 System V 共享記憶體總量。
請注意，在許多系統上，`SHMALL`
是以頁面而非位元組為單位計算的。

較不容易造成問題的，是共享記憶體區段的最小大小
（`SHMMIN`），對 PostgreSQL 而言，
其值最多應約為 32 位元組（通常僅為 1）。
除非您的系統將這些參數設為零，否則整個系統中的
最大區段數（`SHMMNI`）或每個程序的最大區段數
（`SHMSEG`），不太可能造成問題。

當使用 System V 號誌時，PostgreSQL
會為每個允許的連線
（[max_connections](../../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)）、
每個允許的 autovacuum 工作程序
（[autovacuum_worker_slots](../../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)）、
每個允許的 WAL 傳送端程序
（[max_wal_senders](../../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）、
每個允許的背景程序
（[max_worker_processes](../../runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)）等，各使用一個號誌，這些號誌以 16 個為一組來配置。執行期計算所得的參數
[num_os_semaphores](../../runtime-config/runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES)，
會回報所需要的號誌數量。可以在啟動伺服器之前，
透過類似以下的 `postgres` 指令查看此參數：

```

$ postgres -D $PGDATA -C num_os_semaphores
```

每一組 16 個號誌，還會包含第 17 個號誌，
用於存放一個「魔術數字」，以偵測與其他應用程式所使用的
號誌集合之間的衝突。系統中號誌的數量上限，
由 `SEMMNS` 設定，因此，此值必須至少等於
`num_os_semaphores`，再加上每一組 16 個所需號誌
額外多出的一個（請參閱
[表 18.1](#sysvipc-parameters) 中的公式）。
參數 `SEMMNI` 決定了系統中，
同一時間所能存在的號誌集合數量上限。因此，
此參數必須至少為
`ceil(num_os_semaphores / 16)`。降低允許連線數，
是暫時解決失敗問題的權宜之計，這類失敗，
通常會以令人困惑的訊息呈現，例如函式 `semget`
所產生的「No space left on device」。

在某些情況下，也可能有必要將 `SEMMAP`，
至少提高到與 `SEMMNS` 相同的量級。
若您的系統具有此參數（許多系統並沒有），
它定義了號誌資源對應表的大小，其中每一個連續的可用號誌區塊，
都需要一個項目。當某個號誌集合被釋放時，
它會被加入與該釋放區塊相鄰的既有項目，
或者被登錄為一個新的對應表項目。若對應表已滿，
被釋放的號誌就會遺失（直到重新開機為止）。
隨著時間推移，號誌空間的碎片化，
可能導致可用號誌數量少於原本應有的數量。

與「號誌復原」（semaphore undo）相關的其他各項設定，
例如 `SEMMNU` 與 `SEMUME`，
都不會影響 PostgreSQL。

當使用 POSIX 號誌時，所需的號誌數量，
與 System V 相同，也就是每個允許的連線
（[max_connections](../../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)）、
每個允許的 autovacuum 工作程序
（[autovacuum_worker_slots](../../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)）、
每個允許的 WAL 傳送端程序
（[max_wal_senders](../../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）、
每個允許的背景程序
（[max_worker_processes](../../runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)）等，
各使用一個號誌。在偏好使用此選項的平台上，
對 POSIX 號誌的數量，並沒有特定的核心限制。

FreeBSD <a id="id-1.6.5.7.3.15.1.1.2"></a>

除非您已將 `shared_memory_type`
設定為 `sysv`，否則預設的共享記憶體設定，
通常已經足夠。此平台不使用 System V 號誌。

可以使用 `sysctl` 或 `loader`
介面，變更預設的 IPC 設定。以下參數，
可以使用 `sysctl` 設定：

```

    # sysctl kern.ipc.shmall=32768
    # sysctl kern.ipc.shmmax=134217728
```

若要讓這些設定在重新開機後仍然有效，
請修改 `/etc/sysctl.conf`。

若您已將 `shared_memory_type`
設定為 `sysv`，您可能也會想要設定核心，
將 System V 共享記憶體鎖定於 RAM 中，
防止其被分頁至交換空間。可以透過
`sysctl` 設定 `kern.ipc.shm_use_phys`
來達成此目的。

若在 FreeBSD jail 中執行，您應該將其
`sysvshm` 參數，設定為 `new`，
如此一來，它就會擁有自己獨立的 System V
共享記憶體命名空間。
（在 FreeBSD 11.0 之前的版本，需要啟用
jail 對主機 IPC 命名空間的共享存取，
並採取措施避免衝突。）

NetBSD <a id="id-1.6.5.7.3.15.2.1.2"></a>

除非您已將 `shared_memory_type`
設定為 `sysv`，否則預設的共享記憶體設定，
通常已經足夠。不過，您將需要提高
`kern.ipc.semmni` 與
`kern.ipc.semmns`，因為 NetBSD
對這些參數的預設值，小到難以使用。

可以使用 `sysctl`，調整 IPC 參數，例如：

```

    # sysctl -w kern.ipc.semmni=100
```

若要讓這些設定在重新開機後仍然有效，
請修改 `/etc/sysctl.conf`。

若您已將 `shared_memory_type`
設定為 `sysv`，您可能也會想要設定核心，
將 System V 共享記憶體鎖定於 RAM 中，
防止其被分頁至交換空間。可以透過
`sysctl` 設定 `kern.ipc.shm_use_phys`
來達成此目的。

OpenBSD <a id="id-1.6.5.7.3.15.3.1.2"></a>

除非您已將 `shared_memory_type`
設定為 `sysv`，否則預設的共享記憶體設定，
通常已經足夠。不過，您將需要提高
`kern.seminfo.semmni` 與
`kern.seminfo.semmns`，因為 OpenBSD
對這些參數的預設值，小到難以使用。

可以使用 `sysctl`，調整 IPC 參數，例如：

```

    # sysctl kern.seminfo.semmni=100
```

若要讓這些設定在重新開機後仍然有效，
請修改 `/etc/sysctl.conf`。

Linux <a id="id-1.6.5.7.3.15.4.1.2"></a>

除非您已將 `shared_memory_type`
設定為 `sysv`，否則預設的共享記憶體設定，
通常已經足夠，即使如此，也只有在搭載較舊版本核心、
預設值偏低的系統上，才需要調整。此平台不使用
System V 號誌。

可以透過 `sysctl` 介面，
變更共享記憶體大小的設定。舉例來說，
若要允許 16 GB：

```

    $ sysctl -w kernel.shmmax=17179869184
    $ sysctl -w kernel.shmall=4194304
```

若要讓這些設定在重新開機後仍然有效，
請參閱 `/etc/sysctl.conf`。

macOS <a id="id-1.6.5.7.3.15.5.1.2"></a>

除非您已將 `shared_memory_type`
設定為 `sysv`，否則預設的共享記憶體與號誌設定，
通常已經足夠。

在 macOS 上設定共享記憶體，建議的方法，
是建立一個名為 `/etc/sysctl.conf` 的檔案，
其中包含類似以下的變數指派：

```

    kern.sysv.shmmax=4194304
    kern.sysv.shmmin=1
    kern.sysv.shmmni=32
    kern.sysv.shmseg=8
    kern.sysv.shmall=1024
```

請注意，在某些 macOS 版本中，
*全部五個*共享記憶體參數，都必須在
`/etc/sysctl.conf` 中設定，
否則這些值將被忽略。

`SHMMAX` 只能設定為 4096 的倍數。

在此平台上，`SHMALL` 是以 4 kB 頁面為單位計算的。

除了 `SHMMNI` 之外，其他參數都可以使用
sysctl 即時變更。但最好還是透過
`/etc/sysctl.conf`，設定您偏好的值，
這樣這些值就能在重新開機後保留下來。

Solaris<br>illumos

對大多數 PostgreSQL 應用程式而言，
預設的共享記憶體與號誌設定，通常已經足夠。Solaris
的 `SHMMAX` 預設為系統 RAM 的四分之一。
若要進一步調整此設定，請使用與
`postgres` 使用者關聯的 project 設定。
舉例來說，以 `root` 身分執行以下指令：

```

    projadd -c "PostgreSQL DB User" -K "project.max-shm-memory=(privileged,8GB,deny)" -U postgres -G postgres user.postgres
```

此指令會新增 `user.postgres` project，
並將 `postgres` 使用者的共享記憶體上限，
設為 8GB，此設定會在該使用者下次登入時，
或您重新啟動（而非重新載入）PostgreSQL 時生效。
以上假設 PostgreSQL 是由 `postgres` 群組中的
`postgres` 使用者執行的。不需要重新啟動伺服器。

對於將有大量連線的資料庫伺服器而言，
其他建議變更的核心設定包括：

```

    project.max-shm-ids=(priv,32768,deny)
    project.max-sem-ids=(priv,4096,deny)
    project.max-msg-ids=(priv,4096,deny)
```

此外，若您在某個 zone 中執行 PostgreSQL，
可能也需要提高該 zone 的資源使用限制。
關於 `projects` 與 `prctl` 的更多資訊，
請參閱*System Administrator's Guide* 中的
「Chapter2: Projects and Tasks」。

[返回 18.4. 管理核心資源](../kernel-resources.md#kernel-resources)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/kernel-resources.html)（原文版本：18.6；核對日期：2026-09-26）
