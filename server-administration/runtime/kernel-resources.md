<a id="KERNEL-RESOURCES"></a>

## 18.4. 管理核心資源 [#](#KERNEL-RESOURCES)

[18.4.1. 共享記憶體與號誌（Semaphore）](kernel-resources.md#SYSVIPC)

[18.4.2. systemd RemoveIPC](kernel-resources.md#SYSTEMD-REMOVEIPC)

[18.4.3. 資源限制](kernel-resources.md#KERNEL-RESOURCES-LIMITS)

[18.4.4. Linux 記憶體超額分配（Overcommit）](kernel-resources.md#LINUX-MEMORY-OVERCOMMIT)

[18.4.5. Linux 大頁（Huge Pages）](kernel-resources.md#LINUX-HUGE-PAGES)

PostgreSQL 有時可能會耗盡各種作業系統資源限制，
特別是當同一系統上同時執行多份伺服器複本時，
或是在非常大型的安裝環境中。本節說明
PostgreSQL 所使用的核心資源，
以及您可以採取哪些步驟，來解決與核心資源消耗
相關的問題。

<a id="SYSVIPC"></a>

### 18.4.1. 共享記憶體與號誌（Semaphore） [#](#SYSVIPC)

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
（請參閱 [shared_memory_type](../runtime-config/runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE)）。
此外，伺服器啟動時，還會建立相當數量的號誌，
可以是 System V 或 POSIX 樣式。目前，
Linux 與 FreeBSD 系統使用 POSIX 號誌，
其他平台則使用 System V 號誌。

System V IPC 功能，通常受到系統層級配置上限的限制。
當 PostgreSQL 超過這些限制之一時，
伺服器將拒絕啟動，並應留下一則說明問題內容
及處理方式的指示性錯誤訊息。（另請參閱
[18.3.1 節](server-start.md#SERVER-START-FAILURES)。）
相關的核心參數，在不同系統上，命名方式相當一致；
[表 18.1](kernel-resources.md#SYSVIPC-PARAMETERS) 提供了概觀。
不過，設定這些參數的方法則各異。以下針對部分平台，
提供一些建議。

<a id="SYSVIPC-PARAMETERS"></a>

**表 18.1. System V IPC 參數**

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
[shared_memory_type](../runtime-config/runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE)
與
[dynamic_shared_memory_type](../runtime-config/runtime-config-resource.md#GUC-DYNAMIC-SHARED-MEMORY-TYPE)），
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
（[max_connections](../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)）、
每個允許的 autovacuum 工作程序
（[autovacuum_worker_slots](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)）、
每個允許的 WAL 傳送端程序
（[max_wal_senders](../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）、
每個允許的背景程序
（[max_worker_processes](../runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)）等，各使用一個號誌，這些號誌以 16 個為一組來配置。執行期計算所得的參數
[num_os_semaphores](../runtime-config/runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES)，
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
[表 18.1](kernel-resources.md#SYSVIPC-PARAMETERS) 中的公式）。
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
（[max_connections](../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)）、
每個允許的 autovacuum 工作程序
（[autovacuum_worker_slots](../runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)）、
每個允許的 WAL 傳送端程序
（[max_wal_senders](../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）、
每個允許的背景程序
（[max_worker_processes](../runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)）等，
各使用一個號誌。在偏好使用此選項的平台上，
對 POSIX 號誌的數量，並沒有特定的核心限制。

FreeBSD <a id="id-1.6.5.7.3.15.1.1.2"></a>
:   除非您已將 `shared_memory_type`
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
:   除非您已將 `shared_memory_type`
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
:   除非您已將 `shared_memory_type`
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
:   除非您已將 `shared_memory_type`
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
:   除非您已將 `shared_memory_type`
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
:   對大多數 PostgreSQL 應用程式而言，
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

<a id="SYSTEMD-REMOVEIPC"></a>

### 18.4.2. systemd RemoveIPC [#](#SYSTEMD-REMOVEIPC)

<a id="id-1.6.5.7.4.2"></a>

若使用 systemd，就必須採取一些措施，
確保 IPC 資源（包括共享記憶體）不會被作業系統提前移除。
從原始碼安裝 PostgreSQL 時，這一點尤其需要注意。
使用 PostgreSQL 發行套件的使用者，較不容易受此影響，
因為在這種情況下，`postgres` 使用者，
通常會被建立為系統使用者。

`logind.conf` 中的 `RemoveIPC` 設定，
控制著當使用者完全登出時，IPC 物件是否會被移除。
系統使用者則不受此一「登出時移除 IPC 物件」規則的限制。此設定，在原生 systemd 中，
預設為開啟，但某些作業系統發行版，
則預設將其關閉。

當此設定為開啟時，一個典型可觀察到的效果，
是用於平行查詢執行的共享記憶體物件，
會在看似隨機的時間點被移除，
導致在嘗試開啟並移除它們時，出現如下的錯誤與警告：

```

WARNING:  could not remove shared memory segment "/PostgreSQL.1450751626": No such file or directory
```

不同類型的 IPC 物件（共享記憶體與號誌、
System V 與 POSIX），在 systemd 中的處理方式，
略有不同，因此您可能會觀察到，某些 IPC 資源，
移除的方式與其他資源並不相同。但不建議依賴
這些細微的差異。

「使用者登出」可能發生於維護作業期間，
也可能是管理者以 `postgres` 使用者身分
（或類似身分）登入後，該次登入所開啟的工作階段最終仍會登出所致，
因此一般而言，很難完全避免這種情況。

「系統使用者」的定義，是在 systemd 編譯時，
根據 `/etc/login.defs` 中的
`SYS_UID_MAX` 設定決定的。

封裝與部署指令碼，應謹慎地使用
`useradd -r`、`adduser --system`
或等效方式，將 `postgres` 使用者，
建立為系統使用者。

或者，若該使用者帳號建立方式有誤，
或無法變更，建議在 `/etc/systemd/logind.conf`
或其他適當的組態檔中，設定

```

RemoveIPC=no
```

### 注意

上述兩件事，至少必須確保其中一件，
否則 PostgreSQL 伺服器將會非常不可靠。

<a id="KERNEL-RESOURCES-LIMITS"></a>

### 18.4.3. 資源限制 [#](#KERNEL-RESOURCES-LIMITS)

類 Unix 作業系統，會強制實施各種可能干擾
PostgreSQL 伺服器運作的資源限制。特別重要的，
是每個使用者的程序數量限制、每個程序的
開啟檔案數量限制，以及每個程序可用的記憶體量限制。
這些限制，每一項都有「硬性」與「軟性」限制。
實際生效的是軟性限制，但使用者可以在硬性限制的範圍內，
變更軟性限制。硬性限制，則只能由 root 使用者變更。
系統呼叫 `setrlimit`，負責設定這些參數。
shell 內建的 `ulimit` 指令
（Bourne shell）或 `limit`（csh），
則用於從命令列控制資源限制。在衍生自 BSD 的系統上，
`/etc/login.conf` 檔案，控制著登入期間所設定的
各項資源限制。詳情請參閱作業系統的相關文件。
相關參數為 `maxproc`、`openfiles`
與 `datasize`。舉例來說：

```

default:\
...
        :datasize-cur=256M:\
        :maxproc-cur=256:\
        :openfiles-cur=256:\
...
```

（`-cur` 是軟性限制。附加 `-max`，
則可設定硬性限制。）

核心也可能對部分資源，具有系統層級的限制。

* 在 Linux 上，核心參數 `fs.file-max`，
  決定了核心所支援的最大開啟檔案數量。
  可以使用 `sysctl -w fs.file-max=N`
  來變更此值。若要讓此設定在重新開機後仍然有效，
  請在 `/etc/sysctl.conf` 中，加入對應的指派。
  每個程序的檔案數量上限，
  是在核心編譯時就固定的；更多資訊，
  請參閱 `/usr/src/linux/Documentation/proc.txt`。

PostgreSQL 伺服器每個連線使用一個伺服器程序（server process），
因此，除了系統其餘部分所需要的程序之外，
您應該至少提供與允許連線數相同數量的程序。
這通常不會構成問題，但若您在同一部機器上，
執行多個伺服器，情況可能就會變得吃緊。

出廠預設的開啟檔案數量限制，通常設定為「對社群友善」的值，
讓許多使用者能共用一部機器，而不會佔用系統資源中
不成比例的份額。若您在一部機器上執行多個伺服器，
這或許正是您想要的，但在專用伺服器上，
您可能會想要提高此限制。

另一方面，有些系統，則允許個別程序，
開啟大量的檔案；若超過少數幾個程序都這麼做，
系統層級的限制，就可能輕易被超過。若您發現這種情況發生，
且不想變更系統層級的限制，可以設定 PostgreSQL 的
[max_files_per_process](../runtime-config/runtime-config-resource.md#GUC-MAX-FILES-PER-PROCESS)
組態參數，來限制開啟檔案的消耗量。

在支援大量用戶端連線時，另一項可能需要留意的核心限制，
是最大 socket 連線佇列長度。若在極短時間內，
湧入超過該數量的連線請求，其中某些請求，
可能會在 PostgreSQL 伺服器有機會處理之前就被拒絕，
導致這些用戶端收到無助於診斷的連線失敗錯誤，
例如「Resource temporarily unavailable」
或「Connection refused」。在許多平台上，
預設的佇列長度限制為 128。若要提高此限制，
請透過 sysctl，調整對應的核心參數，
然後重新啟動 PostgreSQL 伺服器。此參數，
在 Linux 上命名為 `net.core.somaxconn`，
在較新版本的 FreeBSD 上，
命名為 `kern.ipc.soacceptqueue`，
在 macOS 與其他 BSD 變體上，
則命名為 `kern.ipc.somaxconn`。

<a id="LINUX-MEMORY-OVERCOMMIT"></a>

### 18.4.4. Linux 記憶體超額分配（Overcommit） [#](#LINUX-MEMORY-OVERCOMMIT)

<a id="id-1.6.5.7.6.2"></a><a id="id-1.6.5.7.6.3"></a><a id="id-1.6.5.7.6.4"></a>

Linux 預設的虛擬記憶體行為，對 PostgreSQL
而言，並非最理想的設定。由於核心實作記憶體超額分配的方式，
若 PostgreSQL 或其他程序的記憶體需求，
導致系統的虛擬記憶體耗盡，核心可能會終止
PostgreSQL 的 postmaster，也就是監督者伺服器程序（server process）。

若發生這種情況，您會看到類似以下的核心訊息
（請查閱您系統的文件與設定，了解應在何處查看此類訊息）：

```

Out of Memory: Killed process 12345 (postgres).
```

這表示 `postgres` 程序，
已因記憶體壓力而被終止。雖然既有的資料庫連線，
仍會繼續正常運作，但不會再接受任何新的連線。
若要復原，就必須重新啟動 PostgreSQL。

避免這個問題的其中一種方法，是在一部您能夠確定，
其他程序不會耗盡機器記憶體的機器上，
執行 PostgreSQL。若記憶體吃緊，
增加作業系統的交換空間，有助於避免這個問題，
因為只有在實體記憶體與交換空間都耗盡時，
才會觸發 OOM killer。

若造成系統記憶體耗盡的是 PostgreSQL 本身，
您可以透過變更組態設定，來避免此問題。在某些情況下，
降低與記憶體相關的組態參數，可能會有幫助，
特別是
[`shared_buffers`](../runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS)、
[`work_mem`](../runtime-config/runtime-config-resource.md#GUC-WORK-MEM)
與
[`hash_mem_multiplier`](../runtime-config/runtime-config-resource.md#GUC-HASH-MEM-MULTIPLIER)。
在其他情況下，問題可能是由允許過多連線到
資料庫伺服器本身所造成的。在許多情況下，
降低
[`max_connections`](../runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)，
改用外部的連線池軟體，可能會是更好的做法。

可以修改核心的行為，讓它不會「超額分配」記憶體。
雖然這項設定，並無法完全防止
[OOM killer](https://lwn.net/Articles/104179/) 被觸發，
但能大幅降低其發生機率，因此有助於系統行為更加穩健。
做法是透過 `sysctl`，選擇嚴格的超額分配模式：

```

sysctl -w vm.overcommit_memory=2
```

或者在 `/etc/sysctl.conf` 中，
加入等效的項目。您可能也會想要修改相關設定
`vm.overcommit_ratio`。詳情請參閱核心文件檔案
<https://www.kernel.org/doc/Documentation/vm/overcommit-accounting>。

另一種做法，可以搭配或不搭配變更
`vm.overcommit_memory` 使用，
是將 postmaster 程序特定的
*OOM 分數調整*（OOM score adjustment）值，
設定為 `-1000`，藉此保證它不會成為
OOM killer 的目標。最簡單的做法，
是在啟動指令碼中，於呼叫 `postgres`
之前，執行

```

echo -1000 > /proc/self/oom_score_adj
```

請注意，此動作必須以 root 身分執行，
否則不會有任何效果；因此，由 root 擁有的啟動指令碼，
是執行此動作最簡單的地方。若您這麼做，
也應該在呼叫 `postgres` 之前，
在啟動指令碼中設定以下環境變數：

```

export PG_OOM_ADJUST_FILE=/proc/self/oom_score_adj
export PG_OOM_ADJUST_VALUE=0
```

這些設定，會讓 postmaster 的子程序，
以正常的 OOM 分數調整值零執行，
如此一來，OOM killer 在需要時，
仍能以它們為目標。若您希望子程序，
以其他的 OOM 分數調整值執行，
可以為 `PG_OOM_ADJUST_VALUE` 使用其他值。
（也可以省略 `PG_OOM_ADJUST_VALUE`，
此時預設值為零。）若您未設定
`PG_OOM_ADJUST_FILE`，子程序，
就會以與 postmaster 相同的 OOM 分數調整值執行，
這並不明智，因為整個做法的重點，
就是要確保 postmaster 具有優先的設定。

<a id="LINUX-HUGE-PAGES"></a>

### 18.4.5. Linux 大頁（Huge Pages） [#](#LINUX-HUGE-PAGES)

在使用大塊連續記憶體時（如 PostgreSQL 所做的那樣），
使用大頁（huge pages），能夠降低額外負擔，
特別是在使用較大的
[shared_buffers](../runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS)
值時。若要在 PostgreSQL 中使用此功能，
您需要一個具有 `CONFIG_HUGETLBFS=y`
與 `CONFIG_HUGETLB_PAGE=y` 的核心。
您也必須設定作業系統，提供足夠數量、
所需大小的大頁。執行期計算所得的參數
[shared_memory_size_in_huge_pages](../runtime-config/runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES)，
會回報所需要的大頁數量。可以在啟動伺服器之前，
透過類似以下的 `postgres` 指令查看此參數：

```

$ postgres -D $PGDATA -C shared_memory_size_in_huge_pages
3170
$ grep ^Hugepagesize /proc/meminfo
Hugepagesize:       2048 kB
$ ls /sys/kernel/mm/hugepages
hugepages-1048576kB  hugepages-2048kB
```

在此範例中，預設值為 2MB，但您也可以透過
[huge_page_size](../runtime-config/runtime-config-resource.md#GUC-HUGE-PAGE-SIZE)，
明確要求使用 2MB 或 1GB，
以調整
`shared_memory_size_in_huge_pages`
所計算出的頁面數量。雖然在此範例中，
我們至少需要 `3170` 個大頁，
但若機器上其他程式，也需要用到大頁，
設定較高的值會比較合適。
我們可以透過以下方式設定此值：

```

# sysctl -w vm.nr_hugepages=3170
```

別忘了將此設定加入 `/etc/sysctl.conf`，
讓它在重新開機後仍會重新套用。對於非預設大小的大頁，
我們則可以改用：

```

# echo 3170 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

也可以在開機時，透過類似
`hugepagesz=2M hugepages=3170` 的核心參數，
提供這些設定。

有時，由於記憶體碎片化，核心無法立即配置
所需數量的大頁，因此可能需要重複執行該指令，
或重新開機。（重新開機之後不久，
機器的大部分記憶體，應該都能用來轉換為大頁。）
若要確認某個特定大小的大頁配置情況，
請使用：

```

$ cat /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

也可能需要透過 sysctl 設定
`vm.hugetlb_shm_group`，
授予資料庫伺服器的作業系統使用者使用大頁的權限，
及／或透過 `ulimit -l`，
授予鎖定記憶體的權限。

PostgreSQL 對大頁的預設行為，
是在可能的情況下，使用系統預設大小的大頁，
並在失敗時回退為一般頁面。若要強制使用大頁，
您可以在 `postgresql.conf` 中，
將 [huge_pages](../runtime-config/runtime-config-resource.md#GUC-HUGE-PAGES)
設定為 `on`。請注意，在此設定下，
若可用的大頁數量不足，PostgreSQL 將無法啟動。

關於 Linux 大頁功能的詳細說明，
請參閱
<https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt>。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/kernel-resources.html)（原文版本：18.6；核對日期：2026-09-26）
