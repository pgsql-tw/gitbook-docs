# pgbench 初始化步驟

[返回pgbench](pgbench.md)

<a id="PGBENCH-OPTION-INIT-STEPS-D"></a>

## `d` (Drop) [#](#pgbench-option-init-steps-d) <a href="#pgbench-option-init-steps-d" id="pgbench-option-init-steps-d"></a>

移除任何現有的 pgbench 資料表。

<a id="PGBENCH-OPTION-INIT-STEPS-T"></a>

## `t` (create Tables) [#](#pgbench-option-init-steps-t) <a href="#pgbench-option-init-steps-t" id="pgbench-option-init-steps-t"></a>

建立標準 pgbench 情境所使用的資料表，也就是 `pgbench_accounts`、`pgbench_branches`、`pgbench_history` 與 `pgbench_tellers`。

<a id="PGBENCH-OPTION-INIT-STEPS-G"></a>

## `g` 或 `G`（Generate data，用戶端或伺服器端） [#](#pgbench-option-init-steps-g) <a href="#pgbench-option-init-steps-g" id="pgbench-option-init-steps-g"></a>

產生資料並載入標準資料表，取代任何已存在的資料。

使用 `g`（用戶端資料產生）時，資料會在 `pgbench` 用戶端中產生，然後傳送到伺服器。這會透過 `COPY` 大量使用用戶端／伺服器之間的頻寬。對於 PostgreSQL 14 或更新版本，`pgbench` 會使用 `FREEZE` 選項將資料載入一般（非分割區）資料表，以加快後續的 `VACUUM`。使用 `g` 時，在為所有資料表產生資料的期間，日誌每 100,000 個資料列會印出一則訊息。

使用 `G`（伺服器端資料產生）時，`pgbench` 用戶端只會送出小型查詢，而資料實際上是在伺服器中產生。這種方式不需要可觀的頻寬，但伺服器會做更多工作。使用 `G` 時，日誌在產生資料期間不會印出任何進度訊息。

預設的初始化行為使用用戶端資料產生（等同於 `g`）。

<a id="PGBENCH-OPTION-INIT-STEPS-V"></a>

## `v` (Vacuum) [#](#pgbench-option-init-steps-v) <a href="#pgbench-option-init-steps-v" id="pgbench-option-init-steps-v"></a>

對標準資料表執行 `VACUUM`。

<a id="PGBENCH-OPTION-INIT-STEPS-P"></a>

## `p` (create Primary keys) [#](#pgbench-option-init-steps-p) <a href="#pgbench-option-init-steps-p" id="pgbench-option-init-steps-p"></a>

在標準資料表上建立主鍵索引。

<a id="PGBENCH-OPTION-INIT-STEPS-F"></a>

## `f` (create Foreign keys) [#](#pgbench-option-init-steps-f) <a href="#pgbench-option-init-steps-f" id="pgbench-option-init-steps-f"></a>

在標準資料表之間建立外部鍵限制條件。（請注意，預設不會執行此步驟。）

[返回pgbench](pgbench.md)

---

本頁內容由父頁分出，沿用其原文版本與核對日期。

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbench.html)（原文版本：18.6；核對日期：2026-10-10）
