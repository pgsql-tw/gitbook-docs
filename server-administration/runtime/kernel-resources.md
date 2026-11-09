<a id="KERNEL-RESOURCES"></a>

## 18.4. 管理核心資源 [#](#kernel-resources) <a href="#kernel-resources" id="kernel-resources"></a>

[18.4.1. 共享記憶體與號誌（Semaphore）](kernel-resources/sysvipc.md#sysvipc)

[18.4.2. systemd RemoveIPC](kernel-resources.md#systemd-removeipc)

[18.4.3. 資源限制](kernel-resources.md#kernel-resources-limits)

[18.4.4. Linux 記憶體超額分配（Overcommit）](kernel-resources.md#linux-memory-overcommit)

[18.4.5. Linux 大頁（Huge Pages）](kernel-resources.md#linux-huge-pages)

PostgreSQL 有時可能會耗盡各種作業系統資源限制，
特別是當同一系統上同時執行多份伺服器複本時，
或是在非常大型的安裝環境中。本節說明
PostgreSQL 所使用的核心資源，
以及您可以採取哪些步驟，來解決與核心資源消耗
相關的問題。

### 18.4.1. 共享記憶體與號誌（Semaphore） [#](#sysvipc) <a href="#sysvipc" id="sysvipc"></a>

完整內容請見 [18.4.1. 共享記憶體與號誌（Semaphore）](kernel-resources/sysvipc.md#sysvipc)。

<a id="SYSTEMD-REMOVEIPC"></a>

### 18.4.2. systemd RemoveIPC [#](#systemd-removeipc) <a href="#systemd-removeipc" id="systemd-removeipc"></a>

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

### 18.4.3. 資源限制 [#](#kernel-resources-limits) <a href="#kernel-resources-limits" id="kernel-resources-limits"></a>

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

### 18.4.4. Linux 記憶體超額分配（Overcommit） [#](#linux-memory-overcommit) <a href="#linux-memory-overcommit" id="linux-memory-overcommit"></a>

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

### 18.4.5. Linux 大頁（Huge Pages） [#](#linux-huge-pages) <a href="#linux-huge-pages" id="linux-huge-pages"></a>

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
