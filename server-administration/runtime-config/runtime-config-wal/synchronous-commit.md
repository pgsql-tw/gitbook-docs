# synchronous_commit (enum)

<a id="GUC-SYNCHRONOUS-COMMIT"></a>

## `synchronous_commit` (`enum`) <a id="id-1.6.6.8.3.2.3.1.3"></a> [#](#guc-synchronous-commit) <a href="#guc-synchronous-commit" id="guc-synchronous-commit"></a>

指定在資料庫伺服器向用戶端回覆「成功」訊息之前，
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
（最大延遲為 [wal_writer_delay](../runtime-config-wal.md#GUC-WAL-WRITER-DELAY) 的三倍。）
與 [fsync](../runtime-config-wal.md#GUC-FSYNC) 不同，將此參數設為 `off`
並不會產生任何資料庫不一致的風險：作業系統或資料庫當機，
可能會導致某些近期、原本回報已提交的交易遺失，但資料庫狀態
會與這些交易被乾淨地中止時完全相同。因此，當效能比對交易
持久性的絕對確定性更重要時，關閉 `synchronous_commit`
可以是很實用的替代方案。更多討論請參閱
[28.4 節](../../wal/wal-async-commit.md)。

若 [synchronous_standby_names](../runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) 不為空，
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

[表 19.1](#synchronous-commit-matrix) 摘要說明了
`synchronous_commit` 各設定的能力。

<a id="SYNCHRONOUS-COMMIT-MATRIX"></a>

### 表 19.1. synchronous_commit 模式 [#](#synchronous-commit-matrix) <a href="#synchronous-commit-matrix" id="synchronous-commit-matrix"></a>

<table border="1" class="table" summary="synchronous_commit 模式"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/></colgroup><thead><tr><th>synchronous_commit 設定</th><th>本機持久提交</th><th>PG 當機後待命伺服器持久提交</th><th>作業系統當機後待命伺服器持久提交</th><th>待命伺服器查詢一致性</th></tr></thead><tbody><tr><td>remote_apply</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>on</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center"> </td></tr><tr><td>remote_write</td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center"> </td></tr><tr><td>local</td><td align="center">•</td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr><tr><td>off</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr></tbody></table>

<br>

[返回 19.5. 預寫式日誌 (WAL)](../runtime-config-wal.md#runtime-config-wal)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html)（原文版本：18.6；核對日期：2026-09-25）
