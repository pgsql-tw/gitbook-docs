<a id="DIFFERENT-REPLICATION-SOLUTIONS"></a>

## 26.1. 各種解決方案比較 [#](#DIFFERENT-REPLICATION-SOLUTIONS)

共享磁碟容錯移轉（Shared Disk Failover）
:   共享磁碟容錯移轉透過只保留一份資料庫複本，避免了同步的額外
    負擔。它使用一個由多台伺服器共享的單一磁碟陣列。若主要資料庫
    伺服器故障，待命伺服器就能掛載並啟動該資料庫，就像是從
    資料庫當機中復原一樣。這讓容錯移轉能夠快速完成且不會遺失資料。

    共享硬體功能在網路儲存裝置中相當常見。使用
    網路檔案系統也是可行的，不過必須留意該檔案系統要具備完整的
    POSIX 行為（見 [第 18.2.2.1 節](../runtime/creating-cluster.md#CREATING-CLUSTER-NFS)）。此方法有一項重大限制，
    就是若共享磁碟陣列故障或損毀，主要伺服器與待命伺服器將
    雙雙無法運作。另一個問題是，在主要伺服器運作期間，待命
    伺服器不應該存取該共享儲存裝置。

檔案系統（區塊裝置）複寫
:   共享硬體功能的一種變化版本是檔案系統
    複寫，也就是將檔案系統的所有變更鏡射到位於另一台電腦上的
    檔案系統。唯一的限制是，鏡射動作的執行方式必須確保待命
    伺服器擁有一份一致的檔案系統複本——具體來說，寫入
    待命端的順序必須與主要端相同。DRBD 是 Linux 上常見的
    檔案系統複寫解決方案。

WAL 傳送（Write-Ahead Log Shipping）
:   透過讀取一連串 write-ahead log（WAL）
    記錄的資料流，可以讓暖備援（warm standby）與熱備援（hot standby）伺服器保持最新。
    若主要伺服器故障，待命伺服器會擁有主要伺服器
    幾乎全部的資料，並能夠迅速
    成為新的主要資料庫伺服器。此方式可以是同步或
    非同步的，且只能套用於整個資料庫伺服器。

    待命伺服器可以透過檔案式日誌傳送
    （[第 26.2 節](warm-standby.md)）或串流複寫（見
    [第 26.2.5 節](warm-standby.md#STREAMING-REPLICATION)）來實作，也可以兩者
    合併使用。關於熱備援的相關資訊，請見 [第 26.4 節](hot-standby.md)。

邏輯複寫（Logical Replication）
:   邏輯複寫可讓一台資料庫伺服器將資料
    異動的資料流傳送到另一台伺服器。PostgreSQL
    的邏輯複寫會從 WAL 建構出一連串邏輯資料
    異動。邏輯複寫可以依資料表逐一複寫資料變更。
    此外，正在發布自身變更的伺服器，也可以同時訂閱
    另一台伺服器的變更，讓資料能以多個方向流動。關於邏輯
    複寫的更多資訊，請見 [第 29 章](../logical-replication/README.md)。透過
    邏輯解碼介面（[第 47 章](../../server-programming/logicaldecoding/README.md)），
    第三方擴充功能也能提供類似的功能。

以觸發程序為基礎的主要—待命複寫
:   以觸發程序為基礎的複寫架構，通常會將資料異動
    查詢統一導向指定的主要伺服器。主要伺服器會以逐資料表的方式運作，
    （通常是）非同步地將資料變更傳送到
    待命伺服器。在主要伺服器運作期間，待命伺服器可以回應查詢，
    也可能允許部分本地資料變更或寫入活動。這種
    複寫方式常用於分擔大型分析或資料
    倉儲查詢的負載。

    Slony-I 就是這種類型複寫的一個例子，具備
    逐資料表的細緻度，並支援多台待命伺服器。由於它是
    非同步地（分批）更新待命伺服器，容錯移轉時可能會遺失
    部分資料。

以 SQL 為基礎的複寫中介軟體
:   以 SQL 為基礎的複寫中介軟體，會由一個程式攔截
    每一筆 SQL 查詢，並將其傳送到一台或所有伺服器。每台伺服器
    各自獨立運作。讀寫查詢必須傳送到所有伺服器，
    確保每台伺服器都能收到所有變更。但唯讀查詢
    可以只傳送到單一伺服器，讓讀取負載得以分散
    到各伺服器之間。

    若查詢只是原封不動地廣播出去，像
    `random()`、`CURRENT_TIMESTAMP` 以及
    序列這類函式，在不同伺服器上可能會得到不同的值。
    這是因為每台伺服器都是獨立運作，而且廣播的是
    SQL 查詢本身，而不是實際的資料變更。若
    這種情況無法接受，中介軟體或應用程式就
    必須從單一來源決定這類值，然後在寫入查詢中使用
    那些值。同時也必須留意，確保所有
    交易在所有伺服器上要嘛全部提交、要嘛全部中止，或許可以
    使用兩階段提交（[PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md)
    與 [COMMIT PREPARED](../../reference/sql-commands/sql-commit-prepared.md)）來達成。
    Pgpool-II 與 Continuent Tungsten
    就是這種類型複寫的例子。

非同步多主複寫（Asynchronous Multimaster Replication）
:   對於未經常連線或通訊連結較慢的伺服器，像
    筆記型電腦或
    遠端伺服器，要在各伺服器間保持資料一致是一項
    挑戰。使用非同步多主複寫時，每台
    伺服器獨立運作，並定期與
    其他伺服器通訊，以找出彼此衝突的交易。這些
    衝突可以由使用者或衝突解決規則來排解。
    Bucardo 就是這種類型複寫的一個例子。

同步多主複寫（Synchronous Multimaster Replication）
:   在同步多主複寫中，每台伺服器都能接受
    寫入請求，而且在每筆交易
    提交之前，異動後的資料都會從
    來源伺服器傳送到其他每一台伺服器。大量的寫入活動可能造成
    過度鎖定與提交延遲，導致效能不佳。讀取請求可以
    傳送到任一台伺服器。有些實作方式會使用共享磁碟
    以降低通訊額外負擔。同步多主複寫
    最適合用於以讀取為主的工作負載，不過它最大的
    優點在於任何伺服器都能接受寫入請求——
    不需要在主要伺服器與待命伺服器之間分割工作負載，
    而且因為資料變更是從一台伺服器
    傳送到另一台，因此不會有像
    `random()` 這類非決定性函式所造成的問題。

    PostgreSQL 並未提供這種類型的複寫，
    不過可以使用 PostgreSQL 的兩階段提交（[PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md) 與 [COMMIT PREPARED](../../reference/sql-commands/sql-commit-prepared.md)）
    在應用程式程式碼或中介軟體中實作這種功能。

[表 26.1](different-replication-solutions.md#HIGH-AVAILABILITY-MATRIX) 彙整了
上述各種解決方案的功能。

<a id="HIGH-AVAILABILITY-MATRIX"></a>

**表 26.1. 高可用性、負載平衡與複寫功能對照表**

<table border="1" class="table" summary="高可用性、負載平衡與複寫功能對照表"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/><col class="col7"/><col class="col8"/><col class="col9"/></colgroup><thead><tr><th>功能</th><th>共享磁碟</th><th>檔案系統複寫</th><th>WAL 傳送</th><th>邏輯複寫</th><th>觸發程序式複寫</th><th>SQL 複寫中介軟體</th><th>非同步多主複寫</th><th>同步多主複寫</th></tr></thead><tbody><tr><td>常見範例</td><td align="center">NAS</td><td align="center">DRBD</td><td align="center">內建串流複寫</td><td align="center">內建邏輯複寫、pglogical</td><td align="center">Londiste、Slony</td><td align="center">pgpool-II</td><td align="center">Bucardo</td><td align="center"> </td></tr><tr><td>通訊方式</td><td align="center">共享磁碟</td><td align="center">磁碟區塊</td><td align="center">WAL</td><td align="center">邏輯解碼</td><td align="center">資料表資料列</td><td align="center">SQL</td><td align="center">資料表資料列</td><td align="center">資料表資料列與資料列鎖定</td></tr><tr><td>不需要特殊硬體</td><td align="center"> </td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>允許多台主要伺服器</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>主要伺服器無額外負擔</td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center"> </td><td align="center"> </td></tr><tr><td>不需要等待多台伺服器</td><td align="center">•</td><td align="center"> </td><td align="center">停用同步時</td><td align="center">停用同步時</td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center"> </td></tr><tr><td>主要伺服器故障絕不遺失資料</td><td align="center">•</td><td align="center">•</td><td align="center">啟用同步時</td><td align="center">啟用同步時</td><td align="center"> </td><td align="center">•</td><td align="center"> </td><td align="center">•</td></tr><tr><td>複本可接受唯讀查詢</td><td align="center"> </td><td align="center"> </td><td align="center">搭配 hot standby 時</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>逐資料表細緻度</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center">•</td></tr><tr><td>不需要衝突解決機制</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center">•</td></tr></tbody></table>

<br>

還有一些解決方案不屬於上述任何類別：

資料分區（Data Partitioning）
:   資料分區將資料表切分成多個資料集。每個
    資料集只能由一台伺服器修改。舉例來說，資料可以
    依辦公室分區，例如倫敦與巴黎，每間辦公室各有
    一台伺服器。若需要結合倫敦與巴黎資料的
    查詢，應用程式可以同時查詢兩台伺服器，或者
    可以使用主要／待命複寫，在各伺服器上保留另一間
    辦公室資料的唯讀複本。

多伺服器平行查詢執行
:   上述許多解決方案都允許多台伺服器分別處理多筆
    查詢，但沒有一種允許單一查詢使用多台伺服器來
    更快完成。這種解決方案允許多台伺服器同時
    協同處理單一查詢。通常的做法是將
    資料切分到各伺服器上，讓每台伺服器執行查詢中屬於
    自己的部分，再將結果回傳給中央伺服器進行
    合併，最後回傳給使用者。這可以使用
    PL/Proxy 工具集來實作。

還必須指出，由於 PostgreSQL
是開放原始碼且易於擴充，已有不少公司
以 PostgreSQL 為基礎，打造出具備獨特容錯移轉、複寫與負載
平衡能力的商業封閉原始碼解決方案。這些方案在此不予
討論。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/different-replication-solutions.html)（原文版本：18.6；核對日期：2026-09-25）
