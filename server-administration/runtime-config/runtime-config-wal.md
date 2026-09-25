<a id="RUNTIME-CONFIG-WAL"></a>

## 19.5. 預寫式日誌 (WAL) [#](#RUNTIME-CONFIG-WAL)

[19.5.1. 設定](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)

[19.5.2. 檢查點](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)

[19.5.3. 歸檔](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)

[19.5.4. 復原](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)

[19.5.5. 歸檔復原](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

[19.5.6. 復原目標](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

[19.5.7. WAL 摘要化](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

關於調校這些設定的更多資訊，
請參閱[28.5 節](../wal/wal-configuration.md)。

<a id="RUNTIME-CONFIG-WAL-SETTINGS"></a>

### 19.5.1. 設定 [#](#RUNTIME-CONFIG-WAL-SETTINGS)

<a id="GUC-WAL-LEVEL"></a>

`wal_level` (`enum`) <a id="id-1.6.6.8.3.2.1.1.3"></a> [#](#GUC-WAL-LEVEL)
:   `wal_level` 決定要寫入 WAL 的資訊量多寡。
    預設值為 `replica`，會寫入足夠的資料以支援 WAL 歸檔與複寫，
    包括在待命伺服器上執行唯讀查詢。`minimal` 會移除除了
    從當機或立即關機復原所需資訊之外的所有記錄。最後，
    `logical` 會加入支援邏輯解碼所需的資訊。
    每個層級都涵蓋所有較低層級所記錄的資訊。此參數只能在
    伺服器啟動時設定。

    `minimal` 層級會產生最少量的 WAL。對於在交易中建立或
    重寫的永久性關聯，它不會為其記錄任何資料列資訊。
    這能讓作業快上許多（請參閱
    [14.4.7 節](../../the-sql-language/performance-tips/populate.md#POPULATE-PITR)）。
    會啟用此最佳化的作業包括：

    <table border="0" class="simplelist" summary="簡易清單"><tr><td><code class="command">ALTER ... SET TABLESPACE</code></td></tr><tr><td><code class="command">CLUSTER</code></td></tr><tr><td><code class="command">CREATE TABLE</code></td></tr><tr><td><code class="command">REFRESH MATERIALIZED VIEW</code>
             (不含 <code class="option">CONCURRENTLY</code>)</td></tr><tr><td><code class="command">REINDEX</code></td></tr><tr><td><code class="command">TRUNCATE</code></td></tr></table>

    然而，最小化的 WAL 並不包含足以進行時間點復原的資訊，
    因此必須使用 `replica` 或更高層級，才能啟用
    持續歸檔（[archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE)）與串流二進位複寫。
    事實上，若 `max_wal_senders` 不為零，
    伺服器甚至無法以此模式啟動。
    請注意，將 `wal_level` 變更為
    `minimal` 會使先前的基礎備份無法用於時間點復原與待命伺服器。

    在 `logical` 層級下，會記錄與 `replica`
    相同的資訊，再加上從 WAL 擷取邏輯變更集合所需的資訊。使用
    `logical` 層級會增加 WAL 用量，尤其是當許多資料表都設定為
    `REPLICA IDENTITY FULL`，且執行了大量的
    `UPDATE` 與 `DELETE` 陳述式時。

    在 9.6 之前的版本中，此參數也接受
    `archive` 與 `hot_standby` 這兩個值。
    這些值目前仍會被接受，但會對應為 `replica`。
<a id="GUC-FSYNC"></a>

`fsync` (`boolean`) <a id="id-1.6.6.8.3.2.2.1.3"></a> [#](#GUC-FSYNC)
:   若此參數為 on，PostgreSQL 伺服器會嘗試確保更新確實實際寫入磁碟，
    方式是發出 `fsync()` 系統呼叫，或其他等效的方法
    （請參閱 [wal_sync_method](runtime-config-wal.md#GUC-WAL-SYNC-METHOD)）。
    這能確保資料庫叢集在作業系統或硬體當機後，
    仍可復原至一致的狀態。

    雖然關閉 `fsync` 通常能帶來效能上的好處，
    但這可能在電源故障或系統當機時，導致無法復原的資料損毀。
    因此，只有在你能輕易從外部資料重新建立整個資料庫時，
    才建議關閉 `fsync`。

    適合關閉 `fsync` 的安全情境範例包括：從備份檔案
    初次載入新的資料庫叢集、使用資料庫叢集處理一批資料，
    處理完後該資料庫將被捨棄並重新建立，或是用於
    經常重新建立、且不會用於容錯移轉的唯讀資料庫複本。
    僅憑高品質硬體並不足以作為關閉 `fsync` 的正當理由。

    若要在將 `fsync` 從關閉改為開啟後仍能可靠地復原，
    就必須強制將核心中所有已修改的緩衝區寫入永久性儲存體。
    這可以在叢集關機時完成，也可以在 `fsync`
    為開啟狀態時，透過執行 `initdb --sync-only`、
    執行 `sync`、卸載檔案系統，或重新開機伺服器來完成。

    在許多情況下，針對非關鍵性交易關閉
    [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT)，
    就能取得關閉 `fsync` 所能帶來的大部分潛在效能優勢，
    卻不必承擔資料損毀的相應風險。

    `fsync` 只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    若你關閉此參數，也應考慮一併關閉
    [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES)。
<a id="GUC-SYNCHRONOUS-COMMIT"></a>

`synchronous_commit` (`enum`) <a id="id-1.6.6.8.3.2.3.1.3"></a> [#](#GUC-SYNCHRONOUS-COMMIT)
:   指定在資料庫伺服器向用戶端回覆「成功」訊息之前，
    必須完成多少 WAL 處理作業。有效值為
    `remote_apply`、`on`
    （預設值）、`remote_write`、
    `local`，以及 `off`。

    若 `synchronous_standby_names` 為空，
    則唯一有意義的設定是 `on` 與
    `off`；`remote_apply`、
    `remote_write` 與 `local`
    都會提供與 `on` 相同的本機同步層級。
    所有非 `off` 模式的本機行為，都是等待 WAL 在本機刷寫（flush）至磁碟。
    在 `off` 模式下，不會有任何等待，
    因此回報成功給用戶端的時間點，與該交易之後保證能安全
    抵抗伺服器當機的時間點之間，可能會有延遲。
    （最大延遲為 [wal_writer_delay](runtime-config-wal.md#GUC-WAL-WRITER-DELAY) 的三倍。）
    與 [fsync](runtime-config-wal.md#GUC-FSYNC) 不同，將此參數設為 `off`
    並不會產生任何資料庫不一致的風險：作業系統或資料庫當機，
    可能會導致某些近期、原本回報已提交的交易遺失，但資料庫狀態
    會與這些交易被乾淨地中止時完全相同。因此，當效能比對交易
    持久性的絕對確定性更重要時，關閉 `synchronous_commit`
    可以是很實用的替代方案。更多討論請參閱
    [28.4 節](../wal/wal-async-commit.md)。

    若 [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) 不為空，
    `synchronous_commit` 也會控制交易提交是否要等待其
    WAL 紀錄在待命伺服器上處理完成。

    當設為 `remote_apply` 時，提交動作會等待，
    直到目前同步待命伺服器的回覆指出它們已收到該交易的提交紀錄
    並已套用，使其對待命伺服器上的查詢可見，且已寫入待命伺服器的
    永久性儲存體為止。由於需要等待 WAL 重播，這會造成比先前設定
    大得多的提交延遲。當設為 `on` 時，
    提交動作會等待，直到目前同步待命伺服器的回覆指出它們已收到
    該交易的提交紀錄，並已刷寫至永久性儲存體為止。這能確保
    除非主要伺服器與所有同步待命伺服器的資料庫儲存體同時損毀，
    否則該交易不會遺失。當設為 `remote_write` 時，
    提交動作會等待，直到目前同步待命伺服器的回覆指出它們已收到
    該交易的提交紀錄，並已寫入其檔案系統為止。此設定能確保
    在待命伺服器的 PostgreSQL 執行個體當機時資料不會遺失，
    但若待命伺服器發生作業系統層級的當機，則無法保證，
    因為資料未必已抵達待命伺服器的永久性儲存體。
    `local` 設定會讓提交動作等待本機刷寫至磁碟，
    但不等待複寫完成。這在使用同步複寫時通常並非所欲，
    但為求完整性而提供此選項。

    此參數可隨時變更；任一筆交易的行為，取決於其提交時
    生效中的設定。因此可以（也很實用地）讓部分交易以同步方式提交，
    另一些則以非同步方式提交。舉例來說，若要讓單一
    多陳述式交易在預設為相反設定的情況下以非同步方式提交，
    可在交易內發出 `SET LOCAL synchronous_commit TO OFF`。

    [表 19.1](runtime-config-wal.md#SYNCHRONOUS-COMMIT-MATRIX) 摘要說明了
    `synchronous_commit` 各設定的能力。

    <a id="SYNCHRONOUS-COMMIT-MATRIX"></a>

    **表 19.1. synchronous_commit 模式**

    <table border="1" class="table" summary="synchronous_commit 模式"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/></colgroup><thead><tr><th>synchronous_commit 設定</th><th>本機持久提交</th><th>PG 當機後待命伺服器持久提交</th><th>作業系統當機後待命伺服器持久提交</th><th>待命伺服器查詢一致性</th></tr></thead><tbody><tr><td>remote_apply</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>on</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center"> </td></tr><tr><td>remote_write</td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center"> </td></tr><tr><td>local</td><td align="center">•</td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr><tr><td>off</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr></tbody></table>

    <br>
<a id="GUC-WAL-SYNC-METHOD"></a>

`wal_sync_method` (`enum`) <a id="id-1.6.6.8.3.2.4.1.3"></a> [#](#GUC-WAL-SYNC-METHOD)
:   強制將 WAL 更新寫出至磁碟時所使用的方法。
    若 `fsync` 為關閉，則此設定無關緊要，
    因為 WAL 檔案更新完全不會被強制寫出。
    可用的值有：

    * `open_datasync`（以 `open()` 選項 `O_DSYNC` 寫入 WAL 檔案）
    * `fdatasync`（每次提交時呼叫 `fdatasync()`）
    * `fsync`（每次提交時呼叫 `fsync()`）
    * `fsync_writethrough`（每次提交時呼叫 `fsync()`，並強制透寫任何磁碟寫入快取）
    * `open_sync`（以 `open()` 選項 `O_SYNC` 寫入 WAL 檔案）

    並非所有平台都支援上述所有選項。
    預設值為上述清單中該平台所支援的第一個方法，
    但 `fdatasync` 在 Linux 與 FreeBSD 上為預設值。
    預設值未必是理想的；為了建立當機安全的組態，
    或達到最佳效能，可能有必要變更此設定，
    或系統其他組態面向。這些面向在
    [28.1 節](../wal/wal-reliability.md)中討論。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-FULL-PAGE-WRITES"></a>

`full_page_writes` (`boolean`) <a id="id-1.6.6.8.3.2.5.1.3"></a> [#](#GUC-FULL-PAGE-WRITES)
:   當此參數為 on 時，PostgreSQL 伺服器會在檢查點後，
    每個磁碟頁面第一次被修改時，將其完整內容寫入 WAL。
    這是必要的，因為若作業系統在頁面寫入過程中當機，
    該寫入可能只完成一部分，導致磁碟上的頁面混雜著
    新舊資料。通常儲存在 WAL 中的資料列層級變更資訊，
    不足以在當機後復原時完整還原這類頁面。儲存完整頁面映像
    能保證頁面可被正確還原，但代價是必須寫入 WAL 的資料量增加。
    （由於 WAL 重播一律從某個檢查點開始，因此只需在
    檢查點後每個頁面第一次變更時執行此動作即可。
    因此，降低完整頁面寫入成本的方法之一，就是拉長
    檢查點間隔參數。）

    關閉此參數能加快一般作業速度，但在系統故障後，
    可能導致無法復原的資料損毀，或不動聲色的資料損毀。
    其風險與關閉 `fsync` 類似，只是程度較小，
    也應僅在符合該參數建議的相同情境下才關閉。

    關閉此參數不會影響 WAL 歸檔用於時間點復原（PITR）的使用
    （請參閱 [25.3 節](../backup/continuous-archiving.md)）。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `on`。
<a id="GUC-WAL-LOG-HINTS"></a>

`wal_log_hints` (`boolean`) <a id="id-1.6.6.8.3.2.6.1.3"></a> [#](#GUC-WAL-LOG-HINTS)
:   當此參數為 `on` 時，PostgreSQL 伺服器會在檢查點後，
    每個磁碟頁面第一次被修改時，將其完整內容寫入 WAL，
    即使是對所謂提示位元（hint bits）的非關鍵性修改也一樣。

    若已啟用資料總和檢查碼，提示位元更新一律會記錄到 WAL，
    此時本設定會被忽略。你可以利用此設定來測試，
    若你的資料庫啟用資料總和檢查碼，會額外產生多少 WAL 記錄量。

    此參數只能在伺服器啟動時設定。預設值為 `off`。
<a id="GUC-WAL-COMPRESSION"></a>

`wal_compression` (`enum`) <a id="id-1.6.6.8.3.2.7.1.3"></a> [#](#GUC-WAL-COMPRESSION)
:   此參數會啟用以指定壓縮方法對 WAL 進行壓縮。
    啟用後，PostgreSQL 伺服器會壓縮寫入 WAL 的完整頁面映像
    （例如當 [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES) 為 on、
    進行基礎備份時等）。
    壓縮過的頁面映像會在 WAL 重播時解壓縮。
    支援的方法有 `pglz`、
    `lz4`（若 PostgreSQL 是以
    `--with-lz4` 編譯的），
    以及 `zstd`（若 PostgreSQL 是以
    `--with-zstd` 編譯的）。
    值 `on` 是 `pglz` 的舊式拼法。
    預設值為 `off`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    啟用壓縮可在不增加無法復原資料損毀風險的情況下減少 WAL 用量，
    但代價是在 WAL 記錄時會多耗費一些 CPU 進行壓縮，
    在 WAL 重播時則多耗費一些 CPU 進行解壓縮。
<a id="GUC-WAL-INIT-ZERO"></a>

`wal_init_zero` (`boolean`) <a id="id-1.6.6.8.3.2.8.1.3"></a> [#](#GUC-WAL-INIT-ZERO)
:   若設為 `on`（預設值），此選項會讓新的
    WAL 檔案以零值填滿。在某些檔案系統上，這能確保
    在我們需要寫入 WAL 紀錄之前，空間已先配置完成。
    然而，*寫入時複製*（Copy-On-Write，COW）檔案系統
    可能無法從此技巧中受益，因此提供此選項以略過不必要的工作。
    若設為 `off`，則只會在建立檔案時寫入最後一個位元組，
    使其具有預期的大小。
<a id="GUC-WAL-RECYCLE"></a>

`wal_recycle` (`boolean`) <a id="id-1.6.6.8.3.2.9.1.3"></a> [#](#GUC-WAL-RECYCLE)
:   若設為 `on`（預設值），此選項會透過重新命名的方式
    回收 WAL 檔案，避免需要建立新檔案。在 COW 檔案系統上，
    建立新檔案可能反而更快，因此提供此選項以停用此行為。
<a id="GUC-WAL-BUFFERS"></a>

`wal_buffers` (`integer`) <a id="id-1.6.6.8.3.2.10.1.3"></a> [#](#GUC-WAL-BUFFERS)
:   用於存放尚未寫入磁碟之 WAL 資料的共享記憶體量。
    預設值 -1 會選擇等同於
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS) 1/32（約 3%）的大小，
    但不會小於 `64kB`，也不會大於單一 WAL
    區段的大小（通常為 `16MB`）。若自動選擇的值
    太大或太小，可以手動設定此值，但任何小於
    `32kB` 的正數值，都會被視為 `32kB`。
    若此值未指定單位，則以 WAL 區塊為單位計算，
    也就是 `XLOG_BLCKSZ` 位元組，通常為 8kB。
    此參數只能在伺服器啟動時設定。

    WAL 緩衝區的內容會在每次交易提交時寫出至磁碟，
    因此極大的值不太可能帶來顯著的好處。然而，
    將此值設為至少數個 MB，能在有許多用戶端同時提交的
    繁忙伺服器上改善寫入效能。預設值 -1 所選用的
    自動調校，在多數情況下應能提供合理的結果。
<a id="GUC-WAL-WRITER-DELAY"></a>

`wal_writer_delay` (`integer`) <a id="id-1.6.6.8.3.2.11.1.3"></a> [#](#GUC-WAL-WRITER-DELAY)
:   以時間為單位，指定 WAL 寫入程序刷寫 WAL 的頻率。
    刷寫 WAL 之後，寫入程序會休眠
    `wal_writer_delay` 這段長度的時間，
    除非因某個非同步提交的交易而提早喚醒。
    若上一次刷寫距今的時間少於 `wal_writer_delay`，
    且自那之後產生的 WAL 量少於
    `wal_writer_flush_after`，則 WAL 只會寫入
    作業系統，而不會刷寫至磁碟。
    若此值未指定單位，則以毫秒為單位。
    預設值為 200 毫秒（`200ms`）。請注意，
    在某些系統上，休眠延遲的有效解析度為 10 毫秒；
    若將 `wal_writer_delay` 設為非 10 的倍數，
    其結果可能與設為下一個較高的 10 倍數相同。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-WAL-WRITER-FLUSH-AFTER"></a>

`wal_writer_flush_after` (`integer`) <a id="id-1.6.6.8.3.2.12.1.3"></a> [#](#GUC-WAL-WRITER-FLUSH-AFTER)
:   以資料量為單位，指定 WAL 寫入程序刷寫 WAL 的頻率。
    若上一次刷寫距今的時間少於 `wal_writer_delay`，
    且自那之後產生的 WAL 量少於
    `wal_writer_flush_after`，則 WAL 只會寫入
    作業系統，而不會刷寫至磁碟。若
    `wal_writer_flush_after` 設為 `0`，
    則 WAL 資料一律會立即刷寫。
    若此值未指定單位，則以 WAL 區塊為單位計算，
    也就是 `XLOG_BLCKSZ` 位元組，通常為 8kB。
    預設值為 `1MB`。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-WAL-SKIP-THRESHOLD"></a>

`wal_skip_threshold` (`integer`) <a id="id-1.6.6.8.3.2.13.1.3"></a> [#](#GUC-WAL-SKIP-THRESHOLD)
:   當 `wal_level` 為 `minimal`，
    且某筆交易在建立或重寫某個永久性關聯後提交時，
    此設定決定要如何保存新資料。若資料小於此設定值，
    就將其寫入 WAL 日誌；否則，就對受影響的檔案執行 fsync。
    依你儲存體的特性而定，提高或降低此值，
    可能有助於改善此類提交動作拖慢並行交易的情形。
    若此值未指定單位，則以 KB 為單位計算。
    預設值為兩 MB（`2MB`）。
<a id="GUC-COMMIT-DELAY"></a>

`commit_delay` (`integer`) <a id="id-1.6.6.8.3.2.14.1.3"></a> [#](#GUC-COMMIT-DELAY)
:   設定 `commit_delay` 會在啟動 WAL 刷寫之前
    加入一段時間延遲。若系統負載夠高，使得額外的交易
    能在指定的時間間隔內準備好進行提交，這能讓更多筆交易
    透過單次 WAL 刷寫進行群組提交，藉此提升群組提交的
    輸送量。然而，這也會使每次 WAL 刷寫的延遲，
    最多增加 `commit_delay` 這麼多。
    由於若沒有其他交易準備好提交，這段延遲就只是白白浪費，
    因此只有在即將啟動刷寫時，至少有
    `commit_siblings` 筆其他交易正在進行中，
    才會執行延遲。此外，若已停用 `fsync`，
    則不會執行任何延遲。
    若此值未指定單位，則以微秒為單位。
    `commit_delay` 的預設值為零（不延遲）。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    在 9.3 之前的 PostgreSQL 版本中，
    `commit_delay` 的行為並不相同，效果也差得多：
    它只影響提交動作，而非所有的 WAL 刷寫，
    且即使 WAL 刷寫提早完成，仍會等待完整設定的延遲時間。
    從 PostgreSQL 9.3 開始，
    第一個準備好進行刷寫的程序，會等待設定的間隔時間，
    而後續的程序，則只需等到領頭者完成刷寫作業為止。
<a id="GUC-COMMIT-SIBLINGS"></a>

`commit_siblings` (`integer`) <a id="id-1.6.6.8.3.2.15.1.3"></a> [#](#GUC-COMMIT-SIBLINGS)
:   在執行 `commit_delay` 延遲之前，
    所需的最少並行未結束交易數量。此值越大，
    就越有可能在延遲期間有至少一筆其他交易準備好進行提交。
    預設值為五筆交易。

<a id="RUNTIME-CONFIG-WAL-CHECKPOINTS"></a>

### 19.5.2. 檢查點 [#](#RUNTIME-CONFIG-WAL-CHECKPOINTS)

<a id="GUC-CHECKPOINT-TIMEOUT"></a>

`checkpoint_timeout` (`integer`) <a id="id-1.6.6.8.4.2.1.1.3"></a> [#](#GUC-CHECKPOINT-TIMEOUT)
:   自動 WAL 檢查點之間的最長時間。
    若此值未指定單位，則以秒為單位。
    有效範圍為 30 秒至一天之間。
    預設值為五分鐘（`5min`）。
    提高此參數，可能會增加當機復原所需的時間。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-CHECKPOINT-COMPLETION-TARGET"></a>

`checkpoint_completion_target` (`floating point`) <a id="id-1.6.6.8.4.2.2.1.3"></a> [#](#GUC-CHECKPOINT-COMPLETION-TARGET)
:   以檢查點之間總時間的比例，指定檢查點完成的目標。
    預設值為 0.9，會將檢查點分散到幾乎整個可用區間，
    提供相當一致的 I/O 負載，同時也為檢查點完成的額外負擔
    保留一些時間。不建議降低此參數，因為這會使檢查點更快完成，
    導致檢查點期間的 I/O 速率較高，接著在檢查點完成後
    到下一次排定檢查點之間，出現一段 I/O 較少的期間。
    此參數只能在 `postgresql.conf` 檔案中
    或伺服器命令列上設定。
<a id="GUC-CHECKPOINT-FLUSH-AFTER"></a>

`checkpoint_flush_after` (`integer`) <a id="id-1.6.6.8.4.2.3.1.3"></a> [#](#GUC-CHECKPOINT-FLUSH-AFTER)
:   每當執行檢查點期間已寫入的資料量超過此值，
    就嘗試強制作業系統將這些寫入動作送交底層儲存體。
    這麼做能限制核心分頁快取（page cache）中的髒資料量，
    降低在檢查點結束時發出 `fsync`，
    或作業系統在背景以較大批次寫回資料時發生停滯的可能性。
    這通常能大幅降低交易延遲，但也有一些情況——尤其是
    工作負載大於 [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)，
    但小於作業系統分頁快取的情況——效能反而可能下降。
    此設定在某些平台上可能沒有效果。
    若此值未指定單位，則以區塊為單位計算，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    有效範圍介於 `0`（停用強制寫回）
    與 `2MB` 之間。在 Linux 上預設值為 `256kB`，
    在其他平台上則為 `0`。（若 `BLCKSZ`
    不是 8kB，則預設值與最大值會依比例縮放。）
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-CHECKPOINT-WARNING"></a>

`checkpoint_warning` (`integer`) <a id="id-1.6.6.8.4.2.4.1.3"></a> [#](#GUC-CHECKPOINT-WARNING)
:   若因 WAL 區段檔案填滿而觸發的檢查點，彼此間隔時間
    短於此值，就在伺服器日誌中寫入一則訊息
    （這代表 `max_wal_size` 應該調高）。
    若此值未指定單位，則以秒為單位。
    預設值為 30 秒（`30s`）。
    設為零可停用此警告。
    若 `checkpoint_timeout`
    小於 `checkpoint_warning`，則不會產生任何警告。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-MAX-WAL-SIZE"></a>

`max_wal_size` (`integer`) <a id="id-1.6.6.8.4.2.5.1.3"></a> [#](#GUC-MAX-WAL-SIZE)
:   自動檢查點期間，允許 WAL 成長的最大大小。
    這是一項軟性限制；在特殊情況下，WAL 大小可能會超出
    `max_wal_size`，例如負載過高、
    `archive_command` 或 `archive_library`
    失敗，或 `wal_keep_size` 設定過高等。
    若此值未指定單位，則以 MB 為單位。
    預設值為 1 GB。
    提高此參數，可能會增加當機復原所需的時間。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-MIN-WAL-SIZE"></a>

`min_wal_size` (`integer`) <a id="id-1.6.6.8.4.2.6.1.3"></a> [#](#GUC-MIN-WAL-SIZE)
:   只要 WAL 磁碟用量維持在此設定之下，舊的 WAL 檔案
    就一律會在檢查點時被回收供未來使用，而非直接移除。
    這可用於確保保留足夠的 WAL 空間，
    以因應 WAL 用量的突增，例如執行大型批次工作時。
    若此值未指定單位，則以 MB 為單位。
    預設值為 80 MB。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

<a id="RUNTIME-CONFIG-WAL-ARCHIVING"></a>

### 19.5.3. 歸檔 [#](#RUNTIME-CONFIG-WAL-ARCHIVING)

<a id="GUC-ARCHIVE-MODE"></a>

`archive_mode` (`enum`) <a id="id-1.6.6.8.5.2.1.1.3"></a> [#](#GUC-ARCHIVE-MODE)
:   當 `archive_mode` 啟用時，
    已完成的 WAL 區段會透過設定
    [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) 或
    [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 傳送至歸檔儲存體。
    除了用來停用的 `off` 之外，還有兩種模式：
    `on` 與 `always`。
    在正常運作期間，這兩種模式並無差異，但設為 `always`
    時，WAL 歸檔器在歸檔復原或待命模式期間也會啟用。
    在 `always` 模式下，所有從歸檔還原，
    或透過串流複寫傳輸的檔案，都會（再次）被歸檔。詳情請參閱
    [26.2.9 節](../high-availability/warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY)。

    `archive_mode` 是與
    `archive_command` 及
    `archive_library` 分開的設定，
    如此一來便可在不離開歸檔模式的情況下，
    變更 `archive_command` 與
    `archive_library`。
    此參數只能在伺服器啟動時設定。
    當 `wal_level` 設為 `minimal` 時，
    無法啟用 `archive_mode`。
<a id="GUC-ARCHIVE-COMMAND"></a>

`archive_command` (`string`) <a id="id-1.6.6.8.5.2.2.1.3"></a> [#](#GUC-ARCHIVE-COMMAND)
:   用於歸檔已完成 WAL 檔案區段的本機 shell 命令。
    字串中的任何 `%p` 都會被替換為
    要歸檔之檔案的路徑名稱，任何
    `%f` 則會被替換為僅有檔案名稱。
    （此路徑名稱是相對於伺服器的工作目錄，
    也就是叢集的資料目錄。）
    使用 `%%` 可在命令中嵌入實際的 `%` 字元。
    此命令唯有在成功時才回傳退出狀態碼零，這一點非常重要。
    更多資訊請參閱
    [25.3.1 節](../backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL)。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。它只有在
    `archive_mode` 在伺服器啟動時被啟用，
    且 `archive_library` 設為空字串時才會使用。
    若 `archive_command` 與 `archive_library`
    同時被設定，就會引發錯誤。
    若 `archive_command` 為空字串（預設值），
    而 `archive_mode` 已啟用（且 `archive_library`
    設為空字串），WAL 歸檔會暫時停用，但伺服器仍會繼續
    累積 WAL 區段檔案，以待稍後提供命令。將
    `archive_command` 設為一個除了回傳 true
    之外不做任何事的命令，例如 `/bin/true`
    （Windows 上為 `REM`），實際上等同於停用歸檔，
    但也會破壞歸檔復原所需的 WAL 檔案鏈結，因此只應在
    不常見的情況下使用。
<a id="GUC-ARCHIVE-LIBRARY"></a>

`archive_library` (`string`) <a id="id-1.6.6.8.5.2.3.1.3"></a> [#](#GUC-ARCHIVE-LIBRARY)
:   用於歸檔已完成 WAL 檔案區段的程式庫。若設為
    空字串（預設值），則會啟用透過 shell 進行的歸檔，
    並使用 [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND)。
    若 `archive_command` 與 `archive_library`
    同時被設定，就會引發錯誤。否則，
    就會使用指定的共享程式庫來進行歸檔。當此參數變更時，
    postmaster 會重新啟動 WAL 歸檔程序。更多資訊請參閱
    [25.3.1 節](../backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL) 與
    [第 49 章](../../server-programming/archive-modules/README.md)。

    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-ARCHIVE-TIMEOUT"></a>

`archive_timeout` (`integer`) <a id="id-1.6.6.8.5.2.4.1.3"></a> [#](#GUC-ARCHIVE-TIMEOUT)
:   [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) 或
    [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY)
    只會針對已完成的 WAL 區段被呼叫。因此，若你的伺服器
    產生的 WAL 流量很少（或有低流量的時段），
    交易完成與其安全記錄至歸檔儲存體之間，
    可能會有很長的延遲。為了限制未歸檔資料能有多舊，
    你可以設定 `archive_timeout`，
    強制伺服器定期切換至新的 WAL 區段檔案。當此參數大於零時，
    只要自上次區段檔案切換以來已經過這段時間，
    且期間有任何資料庫活動（包括單一檢查點，若無資料庫活動則
    會跳過檢查點），伺服器就會切換至新的區段檔案。請注意，
    因強制切換而提早關閉的歸檔檔案，
    長度仍與完全填滿的檔案相同。因此，
    使用非常短的 `archive_timeout` 並不明智——
    這會使你的歸檔儲存體膨脹。`archive_timeout`
    設為約一分鐘左右通常是合理的。若你希望資料能比這更快地
    從主要伺服器複寫出去，應考慮使用串流複寫，
    而非歸檔。
    若此值未指定單位，則以秒為單位。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。

<a id="RUNTIME-CONFIG-WAL-RECOVERY"></a>

### 19.5.4. 復原 [#](#RUNTIME-CONFIG-WAL-RECOVERY)

<a id="id-1.6.6.8.6.2"></a>

本節說明適用於一般復原情境的設定，
會影響當機復原、串流複寫，以及以歸檔為基礎的複寫。

<a id="GUC-RECOVERY-PREFETCH"></a>

`recovery_prefetch` (`enum`) <a id="id-1.6.6.8.6.4.1.1.3"></a> [#](#GUC-RECOVERY-PREFETCH)
:   復原期間，是否嘗試預先擷取 WAL 中已提及、
    但尚未進入緩衝區集區的區塊。有效值為
    `off`、`on` 與
    `try`（預設值）。設定為
    `try` 時，只有在作業系統提供支援發出
    預讀建議（read-ahead advice）的能力時，
    才會啟用預先擷取。

    針對即將用到的區塊進行預先擷取，在某些工作負載下，
    能減少復原期間的 I/O 等待時間。
    另請參閱 [wal_decode_buffer_size](runtime-config-wal.md#GUC-WAL-DECODE-BUFFER-SIZE) 與
    [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY) 設定，
    這兩者會限制預先擷取的活動量。
<a id="GUC-WAL-DECODE-BUFFER-SIZE"></a>

`wal_decode_buffer_size` (`integer`) <a id="id-1.6.6.8.6.4.2.1.3"></a> [#](#GUC-WAL-DECODE-BUFFER-SIZE)
:   限制伺服器在 WAL 中能向前查看多遠，
    以尋找可預先擷取的區塊。若此值未指定單位，
    則以位元組為單位計算。
    預設值為 512kB。
    此參數只能在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY"></a>

### 19.5.5. 歸檔復原 [#](#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

<a id="id-1.6.6.8.7.2"></a>

本節說明僅在復原期間才適用的設定。
若你希望執行後續的復原，就必須重新設定這些設定。

「復原」涵蓋將伺服器用作待命伺服器，
或用於執行目標式復原。一般而言，待命模式是用來提供高可用性
及／或讀取擴展性，而目標式復原則是用來從資料遺失中復原。

若要以待命模式啟動伺服器，請在資料目錄中建立一個名為
`standby.signal`<a id="id-1.6.6.8.7.5.2"></a>
的檔案。伺服器會進入復原狀態，
且在抵達已歸檔 WAL 的結尾時不會停止復原，而是會持續嘗試
透過連線至 `primary_conninfo` 設定所指定的傳送伺服器，
及／或透過 `restore_command` 擷取新的 WAL 區段，
繼續進行復原。在此模式下，本節與
[19.6.3 節](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)
的參數都值得留意。[19.5.6 節](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)
的參數也會被套用，但在此模式下通常並不實用。

若要以目標式復原模式啟動伺服器，請在資料目錄中建立一個名為
`recovery.signal`<a id="id-1.6.6.8.7.6.2"></a>
的檔案。若 `standby.signal` 與
`recovery.signal` 檔案同時被建立，
則以待命模式優先。目標式復原模式會在已歸檔 WAL
完全重播完成，或達到 `recovery_target` 時結束。
在此模式下，本節與
[19.5.6 節](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)
兩者的參數都會被使用。

<a id="GUC-RESTORE-COMMAND"></a>

`restore_command` (`string`) <a id="id-1.6.6.8.7.7.1.1.3"></a> [#](#GUC-RESTORE-COMMAND)
:   用於從 WAL 檔案序列中取回已歸檔區段的本機 shell 命令。
    此參數為歸檔復原所必須，但對串流複寫而言為選用。
    字串中的任何 `%f` 都會被替換為
    要從歸檔取回之檔案的名稱，任何
    `%p` 則會被替換為伺服器上的複本目的地路徑名稱。
    （此路徑名稱是相對於目前的工作目錄，
    也就是叢集的資料目錄。）
    任何 `%r` 都會被替換為包含最後一個有效
    重新啟動點的檔案名稱。這是必須保留、
    以讓還原動作可重新啟動的最早檔案，因此此資訊可用來
    將歸檔截短至支援目前還原所需的最小範圍。
    `%r` 一般僅用於暖待命（warm-standby）組態
    （請參閱 [26.2 節](../high-availability/warm-standby.md)）。
    寫入 `%%` 可嵌入實際的 `%` 字元。

    此命令唯有在成功時才回傳退出狀態碼零，這一點非常重要。
    此命令*將會*被要求提供歸檔中不存在的檔案名稱；
    在這種情況下，它必須回傳非零值。範例：

    ```

    restore_command = 'cp /mnt/server/archivedir/%f "%p"'
    restore_command = 'copy "C:\\server\\archivedir\\%f" "%p"'  # Windows
    ```

    有一個例外情況：若命令是因訊號而終止（SIGTERM 除外，
    該訊號屬於資料庫伺服器關機程序的一部分），
    或因 shell 發生錯誤（例如找不到命令）而終止，
    則復原會中止，且伺服器不會啟動。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-ARCHIVE-CLEANUP-COMMAND"></a>

`archive_cleanup_command` (`string`) <a id="id-1.6.6.8.7.7.2.1.3"></a> [#](#GUC-ARCHIVE-CLEANUP-COMMAND)
:   此選用參數指定一個 shell 命令，會在每個重新啟動點執行。
    `archive_cleanup_command` 的用途，
    是提供一種機制，用來清除待命伺服器不再需要的
    舊已歸檔 WAL 檔案。
    任何 `%r` 都會被替換為包含最後一個有效
    重新啟動點的檔案名稱。
    這是必須*保留*、以讓還原動作可重新啟動的最早檔案，
    因此所有早於 `%r` 的檔案都可以安全移除。
    此資訊可用來將歸檔截短至支援目前還原所需的最小範圍。
    [pg_archivecleanup](../../reference/reference-server/pgarchivecleanup.md) 模組
    常被用於單一待命伺服器組態中的
    `archive_cleanup_command`，例如：

    ```
    archive_cleanup_command = 'pg_archivecleanup /mnt/server/archivedir %r'
    ```

    然而請注意，若有多個待命伺服器正從同一個歸檔目錄還原，
    你必須確保在任一伺服器仍需要某個 WAL 檔案時，不會將其刪除。
    `archive_cleanup_command` 一般會用於
    暖待命組態中（請參閱 [26.2 節](../high-availability/warm-standby.md)）。
    寫入 `%%` 可在命令中嵌入實際的 `%` 字元。

    若命令回傳非零的退出狀態碼，就會寫入一則警告日誌訊息。
    但有一個例外情況：若命令是因訊號終止，
    或因 shell 發生錯誤（例如找不到命令）而終止，
    則會引發致命錯誤。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-RECOVERY-END-COMMAND"></a>

`recovery_end_command` (`string`) <a id="id-1.6.6.8.7.7.3.1.3"></a> [#](#GUC-RECOVERY-END-COMMAND)
:   此參數指定一個只會在復原結束時執行一次的 shell 命令。
    此參數為選用。`recovery_end_command`
    的用途，是提供一種機制，用於在複寫或復原完成後進行清理。
    任何 `%r` 都會被替換為包含最後一個有效重新啟動點的
    檔案名稱，用法與 [archive_cleanup_command](runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND) 相同。

    若命令回傳非零的退出狀態碼，就會寫入一則警告日誌訊息，
    但資料庫仍會繼續啟動。有一個例外情況：若命令是因訊號
    或 shell 發生錯誤（例如找不到命令）而終止，
    則資料庫不會繼續啟動。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

<a id="RUNTIME-CONFIG-WAL-RECOVERY-TARGET"></a>

### 19.5.6. 復原目標 [#](#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

依預設，復原會一直復原到 WAL 日誌的結尾。以下參數
可用來指定更早的停止點。
`recovery_target`、
`recovery_target_lsn`、`recovery_target_name`、
`recovery_target_time`，或 `recovery_target_xid`
之中最多只能使用一個；若組態檔中同時指定了一個以上，
就會引發錯誤。
這些參數只能在伺服器啟動時設定。

<a id="GUC-RECOVERY-TARGET"></a>

`recovery_target` `= 'immediate'` <a id="id-1.6.6.8.8.3.1.1.3"></a> [#](#GUC-RECOVERY-TARGET)
:   此參數指定復原應在達到一致狀態後立即結束，
    也就是儘可能提早結束。若是從線上備份還原，
    這代表的是備份完成時的那個時間點。

    技術上而言，這是一個字串參數，但目前
    `'immediate'` 是唯一允許的值。
<a id="GUC-RECOVERY-TARGET-NAME"></a>

`recovery_target_name` (`string`) <a id="id-1.6.6.8.8.3.2.1.3"></a> [#](#GUC-RECOVERY-TARGET-NAME)
:   此參數指定復原要進行到的具名還原點
    （以 `pg_create_restore_point()` 建立）。
<a id="GUC-RECOVERY-TARGET-TIME"></a>

`recovery_target_time` (`timestamp`) <a id="id-1.6.6.8.8.3.3.1.3"></a> [#](#GUC-RECOVERY-TARGET-TIME)
:   此參數指定復原要進行到的時間戳記。
    確切的停止點也會受
    [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE)
    影響。

    此參數的值，是以 `timestamp with time zone`
    資料型別所接受的格式表示的時間戳記，
    但不能使用時區縮寫（除非在組態檔中較早處已設定
    [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) 變數）。
    建議的寫法是使用相對於 UTC 的數字偏移量，
    或者也可以寫出完整的時區名稱，
    例如 `Europe/Helsinki`，而非 `EEST`。
<a id="GUC-RECOVERY-TARGET-XID"></a>

`recovery_target_xid` (`string`) <a id="id-1.6.6.8.8.3.4.1.3"></a> [#](#GUC-RECOVERY-TARGET-XID)
:   此參數指定復原要進行到的交易 ID。請留意，
    雖然交易 ID 是在交易開始時依序指派的，
    但交易完成的數值順序可能會不同。
    會被復原的交易，是那些在指定的交易之前
    （且可選擇是否包含指定的交易本身）提交的交易。
    確切的停止點也會受
    [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE)
    影響。
<a id="GUC-RECOVERY-TARGET-LSN"></a>

`recovery_target_lsn` (`pg_lsn`) <a id="id-1.6.6.8.8.3.5.1.3"></a> [#](#GUC-RECOVERY-TARGET-LSN)
:   此參數指定復原要進行到的預寫式日誌位置（LSN）。
    確切的停止點也會受
    [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE) 影響。此
    參數會以系統資料型別
    [`pg_lsn`](../../the-sql-language/datatype/datatype-pg-lsn.md) 進行解析。

以下選項進一步指定了復原目標，並會影響
抵達目標時所發生的情況：

<a id="GUC-RECOVERY-TARGET-INCLUSIVE"></a>

`recovery_target_inclusive` (`boolean`) <a id="id-1.6.6.8.8.5.1.1.3"></a> [#](#GUC-RECOVERY-TARGET-INCLUSIVE)
:   指定要在指定的復原目標之後才停止
    （`on`），或是在復原目標之前就停止
    （`off`）。
    此設定適用於指定了 [recovery_target_lsn](runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN)、
    [recovery_target_time](runtime-config-wal.md#GUC-RECOVERY-TARGET-TIME)，或
    [recovery_target_xid](runtime-config-wal.md#GUC-RECOVERY-TARGET-XID) 的情況。
    此設定分別控制了恰好具有目標 WAL 位置（LSN）、
    提交時間，或交易 ID 的交易，是否會被納入復原範圍。
    預設值為 `on`。
<a id="GUC-RECOVERY-TARGET-TIMELINE"></a>

`recovery_target_timeline` (`string`) <a id="id-1.6.6.8.8.5.2.1.3"></a> [#](#GUC-RECOVERY-TARGET-TIMELINE)
:   指定要復原到某個特定的時間線。此值可以是
    數字時間線 ID，或一個特殊值。值
    `current` 會沿著基礎備份建立當時
    正生效的同一條時間線進行復原。值
    `latest` 則會復原到歸檔中所找到的
    最新時間線，這在待命伺服器上很實用。
    `latest` 為預設值。

    若要以十六進位表示時間線 ID（例如，若是從
    WAL 檔案名稱或歷史檔案中擷取而來），
    請在前面加上 `0x`。舉例來說，
    若 WAL 檔案名稱為
    `00000011000000A10000004F`，
    則時間線 ID 為 `0x11`（十進位為 17）。

    你通常只有在複雜的重複復原情境中，
    才需要設定此參數——也就是當你需要回到某個
    自身也是透過時間點復原才抵達的狀態時。
    請參閱 [25.3.6 節](../backup/continuous-archiving.md#BACKUP-TIMELINES)
    進行討論。
<a id="GUC-RECOVERY-TARGET-ACTION"></a>

`recovery_target_action` (`enum`) <a id="id-1.6.6.8.8.5.3.1.3"></a> [#](#GUC-RECOVERY-TARGET-ACTION)
:   指定伺服器在抵達復原目標之後應採取的動作。
    預設值為 `pause`，代表復原會被暫停。
    `promote` 代表復原程序會結束，
    伺服器會開始接受連線。
    最後，`shutdown` 則會在抵達復原目標後
    將伺服器停止。

    `pause` 設定的用意，是讓你能對資料庫
    執行查詢，以檢查此復原目標是否是最理想的復原停止點。
    可以透過使用 `pg_wal_replay_resume()`
    （請參閱
    [表 9.99](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-RECOVERY-CONTROL-TABLE)）
    來繼續已暫停的狀態，如此便會使復原結束。
    若此復原目標並非所需的停止點，
    請關閉伺服器、將復原目標設定變更為更晚的目標，
    再重新啟動以繼續復原。

    `shutdown` 設定的用途，
    是讓執行個體準備好停在所需的確切重播位置。
    此執行個體仍能重播更多 WAL 紀錄
    （事實上，下次啟動時，它必須重播自上次檢查點以來的 WAL 紀錄）。

    請注意，由於當 `recovery_target_action` 設為
    `shutdown` 時，`recovery.signal`
    不會被移除，因此除非變更組態，
    或手動移除 `recovery.signal` 檔案，
    否則任何後續的啟動都會以立即關機收場。

    若未設定復原目標，此設定不會產生任何效果。
    若未啟用 [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY)，
    則 `pause` 設定的行為會與 `shutdown` 相同。
    若在提升正在進行時抵達復原目標，
    則 `pause` 設定的行為會與
    `promote` 相同。

    無論如何，若已設定復原目標，
    但歸檔復原卻在抵達目標之前結束，
    伺服器就會以致命錯誤關機。

<a id="RUNTIME-CONFIG-WAL-SUMMARIZATION"></a>

### 19.5.7. WAL 摘要化 [#](#RUNTIME-CONFIG-WAL-SUMMARIZATION)

以下設定控制 WAL 摘要化，這是執行
[增量備份](../backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)
必須啟用的功能。

<a id="GUC-SUMMARIZE-WAL"></a>

`summarize_wal` (`boolean`) <a id="id-1.6.6.8.9.3.1.1.3"></a> [#](#GUC-SUMMARIZE-WAL)
:   啟用 WAL 摘要器（summarizer）程序。請注意，
    WAL 摘要化可以在主要伺服器或待命伺服器上啟用。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。預設值為 `off`。

    若 `wal_level` 設為 `minimal`，
    伺服器無法以 `summarize_wal=on` 啟動。
    若是在伺服器啟動後，於 `wal_level=minimal`
    的狀態下設定 `summarize_wal=on`，
    摘要器仍會執行，但會拒絕為任何以
    `wal_level=minimal` 產生的 WAL
    產生摘要檔案。
<a id="GUC-WAL-SUMMARY-KEEP-TIME"></a>

`wal_summary_keep_time` (`integer`) <a id="id-1.6.6.8.9.3.2.1.3"></a> [#](#GUC-WAL-SUMMARY-KEEP-TIME)
:   設定 WAL 摘要器自動移除舊 WAL 摘要之前，
    要經過的時間長度。系統會使用檔案的時間戳記，
    判斷哪些檔案已舊到可以移除。一般而言，
    你應將此值設得比一次備份與依賴該次備份的後續增量備份之間
    可能經過的時間，還要寬裕一些。WAL 摘要必須涵蓋
    前一次備份與正在進行之新備份之間的整段 WAL 紀錄範圍；
    若否，該次增量備份就會失敗。若此參數設為零，
    WAL 摘要就不會被自動刪除，但你仍可以安全地手動移除
    你確知未來增量備份不會用到的檔案。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
    若此值未指定單位，則以分鐘為單位。
    預設值為 10 天。若 `summarize_wal = off`，
    無論此參數值為何，既有的 WAL 摘要都不會被移除，
    因為 WAL 摘要器不會執行。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html)（原文版本：18.6；核對日期：2026-09-25）
