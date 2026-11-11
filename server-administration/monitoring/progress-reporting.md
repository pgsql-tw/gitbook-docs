<a id="PROGRESS-REPORTING"></a>

## 27.4. 進度回報 [#](#progress-reporting) <a href="#progress-reporting" id="progress-reporting"></a>

[27.4.1. ANALYZE 進度回報](progress-reporting/analyze-progress-reporting.md#analyze-progress-reporting)

[27.4.2. CLUSTER 進度回報](progress-reporting/cluster-progress-reporting.md#cluster-progress-reporting)

[27.4.3. COPY 進度回報](progress-reporting/copy-progress-reporting.md#copy-progress-reporting)

[27.4.4. CREATE INDEX 進度回報](progress-reporting/create-index-progress-reporting.md#create-index-progress-reporting)

[27.4.5. VACUUM 進度回報](progress-reporting/vacuum-progress-reporting.md#vacuum-progress-reporting)

[27.4.6. 基礎備份進度回報](progress-reporting/basebackup-progress-reporting.md#basebackup-progress-reporting)

PostgreSQL 具備在命令執行期間，
回報特定命令執行進度的能力。目前支援進度回報的命令，
僅有 `ANALYZE`、
`CLUSTER`、
`CREATE INDEX`、`VACUUM`、
`COPY`，
以及 [BASE_BACKUP](../../internals/protocol/protocol-replication.md#PROTOCOL-REPLICATION-BASE-BACKUP)
（也就是 [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md)
用來取得基礎備份時所發出的複寫命令）。
未來可能會擴充支援的命令範圍。

### 27.4.1. ANALYZE 進度回報 [#](#analyze-progress-reporting) <a href="#analyze-progress-reporting" id="analyze-progress-reporting"></a>

完整內容請見 [27.4.1. ANALYZE 進度回報](progress-reporting/analyze-progress-reporting.md#analyze-progress-reporting)。

### 27.4.2. CLUSTER 進度回報 [#](#cluster-progress-reporting) <a href="#cluster-progress-reporting" id="cluster-progress-reporting"></a>

完整內容請見 [27.4.2. CLUSTER 進度回報](progress-reporting/cluster-progress-reporting.md#cluster-progress-reporting)。

### 27.4.3. COPY 進度回報 [#](#copy-progress-reporting) <a href="#copy-progress-reporting" id="copy-progress-reporting"></a>

完整內容請見 [27.4.3. COPY 進度回報](progress-reporting/copy-progress-reporting.md#copy-progress-reporting)。

### 27.4.4. CREATE INDEX 進度回報 [#](#create-index-progress-reporting) <a href="#create-index-progress-reporting" id="create-index-progress-reporting"></a>

完整內容請見 [27.4.4. CREATE INDEX 進度回報](progress-reporting/create-index-progress-reporting.md#create-index-progress-reporting)。

### 27.4.5. VACUUM 進度回報 [#](#vacuum-progress-reporting) <a href="#vacuum-progress-reporting" id="vacuum-progress-reporting"></a>

完整內容請見 [27.4.5. VACUUM 進度回報](progress-reporting/vacuum-progress-reporting.md#vacuum-progress-reporting)。

### 27.4.6. 基礎備份進度回報 [#](#basebackup-progress-reporting) <a href="#basebackup-progress-reporting" id="basebackup-progress-reporting"></a>

完整內容請見 [27.4.6. 基礎備份進度回報](progress-reporting/basebackup-progress-reporting.md#basebackup-progress-reporting)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
