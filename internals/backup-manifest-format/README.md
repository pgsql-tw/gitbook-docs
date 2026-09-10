## 第 70 章 備份清單格式

**目錄**

[70.1. 備份清單頂層物件](backup-manifest-toplevel.md)

[70.2. 備份清單檔案物件](backup-manifest-files.md)

[70.3. 備份清單 WAL 範圍物件](backup-manifest-wal-ranges.md)

<a id="id-1.10.22.2"></a>

[pg_basebackup](../../reference/reference-client/app-pgbasebackup.md) 產生的備份清單主要用於讓
[pg_verifybackup](../../reference/reference-client/app-pgverifybackup.md) 驗證備份。不過，其他工具也能讀取
備份清單檔案並使用其中資訊來達成自身目的。為此，本章說明備份清單檔案的格式。

備份清單是以 UTF-8 編碼的 JSON 文件。（一般而言，JSON 文件必須採用 Unicode；但 PostgreSQL 允許
`json` 與 `jsonb` 資料型別使用任何受支援的伺服器編碼。備份清單沒有相同的例外。）JSON 文件
一律是物件；下一節會說明該物件包含的鍵。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-manifest-format.html)（原文版本：18.6；核對日期：2026-09-10）
