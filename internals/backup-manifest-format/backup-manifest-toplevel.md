<a id="BACKUP-MANIFEST-TOPLEVEL"></a>

## 70.1. 備份清單頂層物件 [#](#backup-manifest-toplevel) <a href="#backup-manifest-toplevel" id="backup-manifest-toplevel"></a>

備份清單的 JSON 文件包含下列鍵。

`PostgreSQL-Backup-Manifest-Version`
:   對應的值是整數。從 PostgreSQL `17` 開始，其值為 `2`；在較舊的版本中則為 `1`。

`System-Identifier`
:   取得備份的 PostgreSQL 執行個體的資料庫系統識別碼。只有當 `PostgreSQL-Backup-Manifest-Version` 為 `2` 時，才會有此欄位。

`Files`
:   對應的值一律是物件清單，每個物件描述備份中存在的一個檔案。使用此備份所需的 WAL 檔案，以及備份清單本身，都不會在此清單中有項目。清單中每個物件的結構說明於[第 70.2 節](backup-manifest-files.md)。

`WAL-Ranges`
:   對應的值一律是物件清單，每個物件描述一段 WAL 記錄範圍；為了使用此備份，這段範圍必須能從特定時間軸讀取。這些物件的結構進一步說明於[第 70.3 節](backup-manifest-wal-ranges.md)。

`Manifest-Checksum`
:   此鍵一律出現在備份清單檔案的最後一行。對應的值是前面所有行的 SHA-256 檢查碼。我們在這裡使用固定的檢查碼方法，讓用戶端可以逐步剖析備份清單。雖然 SHA-256 檢查碼的計算成本明顯高於 CRC-32C 檢查碼，但備份清單通常應該夠小，額外的計算不會造成太大影響。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-manifest-toplevel.html)（原文版本：18.6；核對日期：2026-10-17）
