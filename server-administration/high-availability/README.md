<a id="HIGH-AVAILABILITY"></a>

## 第 26 章 高可用性、負載平衡與複寫

**目錄**

[26.1. 不同解決方案的比較](different-replication-solutions.md)

[26.2. 日誌傳送待命伺服器](warm-standby.md)
:   [26.2.1. 規劃](warm-standby.md#STANDBY-PLANNING)

    [26.2.2. 待命伺服器運作](warm-standby.md#STANDBY-SERVER-OPERATION)

    [26.2.3. 為待命伺服器準備主要伺服器](warm-standby.md#PREPARING-PRIMARY-FOR-STANDBY)

    [26.2.4. 設定待命伺服器](warm-standby.md#STANDBY-SERVER-SETUP)

    [26.2.5. 串流複寫](warm-standby.md#STREAMING-REPLICATION)

    [26.2.6. 複寫槽](warm-standby.md#STREAMING-REPLICATION-SLOTS)

    [26.2.7. 串接複寫](warm-standby.md#CASCADING-REPLICATION)

    [26.2.8. 同步複寫](warm-standby.md#SYNCHRONOUS-REPLICATION)

    [26.2.9. 待命伺服器中的連續封存](warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY)

[26.3. 容錯移轉](warm-standby-failover.md)

[26.4. 熱待命](hot-standby.md)
:   [26.4.1. 使用者總覽](hot-standby.md#HOT-STANDBY-USERS)

    [26.4.2. 處理查詢衝突](hot-standby.md#HOT-STANDBY-CONFLICT)

    [26.4.3. 管理者總覽](hot-standby.md#HOT-STANDBY-ADMIN)

    [26.4.4. 熱待命參數參考](hot-standby.md#HOT-STANDBY-PARAMETERS)

    [26.4.5. 注意事項](hot-standby.md#HOT-STANDBY-CAVEATS)

<a id="id-1.6.13.2"></a><a id="id-1.6.13.3"></a><a id="id-1.6.13.4"></a><a id="id-1.6.13.5"></a><a id="id-1.6.13.6"></a><a id="id-1.6.13.7"></a>

多台資料庫伺服器可以協同運作，讓第二台伺服器在主要伺服器失效時
能夠快速接手（高可用性），或是讓多台電腦提供相同的資料服務
（負載平衡）。理想情況下，資料庫伺服器之間應該能夠無縫協同運作。
提供靜態網頁的網頁伺服器，只需單純地將網頁請求負載平衡到多台機器，
就能相當輕鬆地結合在一起。事實上，唯讀的資料庫伺服器也相對容易結合。
不幸的是，大多數資料庫伺服器同時處理讀取與寫入請求，而可讀寫的
伺服器要結合起來就困難得多。這是因為，雖然唯讀資料只需要在每台
伺服器上放置一次，但寫入任何一台伺服器的資料，都必須傳播到所有
伺服器，未來對這些伺服器發出的讀取請求，才能得到一致的結果。

這個同步問題，是伺服器協同運作時的根本困難所在。由於沒有單一
解決方案能消除同步問題在所有使用情境下的影響，因此存在多種
解決方案。每種解決方案都以不同的方式處理這個問題，並針對特定的
工作負載將其影響降到最低。

有些解決方案透過只允許一台伺服器修改資料，來處理同步問題。
能夠修改資料的伺服器，稱為可讀寫、*master* 或 *primary*
伺服器。追蹤主要伺服器異動的伺服器，稱為 *standby* 或
*secondary* 伺服器。在被提升為主要伺服器之前都無法連線的待命
伺服器，稱為 *warm standby* 伺服器；而可以接受連線並提供唯讀
查詢服務的待命伺服器，則稱為 *hot standby* 伺服器。

有些解決方案是同步的，意即在所有伺服器都已提交某個異動資料的
交易之前，這個交易不會被視為已提交。這保證了容錯移轉不會遺失
任何資料，而且無論查詢哪一台伺服器，所有經過負載平衡的伺服器
都會回傳一致的結果。相對地，非同步的解決方案，容許提交時間與
其傳播到其他伺服器之間存在一定延遲，這使得在切換到備援伺服器
時，有可能遺失部分交易，而且經過負載平衡的伺服器也可能回傳
稍微過時的結果。當同步方式的速度太慢時，就會使用非同步通訊。

解決方案也可以依其精細程度來分類。有些解決方案只能處理整台
資料庫伺服器，而其他方案則能提供資料表層級或資料庫層級的控制。

在做任何選擇時，都必須考慮效能。功能性與效能之間，通常存在
取捨關係。舉例來說，在速度緩慢的網路上使用完全同步的解決方案，
可能會讓效能降低超過一半，而非同步的方案則可能對效能只有
極小的影響。

本節其餘部分，將概述各種容錯移轉、複寫與負載平衡的解決方案。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/high-availability.html)（原文版本：18.6；核對日期：2026-09-25）
