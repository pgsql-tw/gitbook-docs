<a id="BACKUP-MANIFEST-FILES"></a>

## 70.2. 備份清單檔案物件 [#](#BACKUP-MANIFEST-FILES)

描述單一檔案的物件會包含 `Path` 鍵或 `Encoded-Path` 鍵其中之一。通常會出現的是 `Path` 鍵，其對應的字串值是該檔案相對於備份目錄根目錄的路徑。位於使用者定義資料表空間中的檔案，其路徑的前兩個組成部分是 `pg_tblspc` 與該資料表空間的 OID。若路徑不是合法的 UTF-8 字串，或使用者要求所有檔案都使用編碼路徑，則改為出現 `Encoded-Path` 鍵。它儲存相同的資料，但編碼為十六進位數字組成的字串。字串中每一對十六進位數字代表一個八位元組（octet）。

下列兩個鍵一律存在：

`Size`
:   此檔案的預期大小，以整數表示。

`Last-Modified`
:   備份當時伺服器所回報的檔案最後修改時間。與備份中儲存的其他欄位不同，此欄位不會被 [pg_verifybackup](../../reference/reference-client/app-pgverifybackup.md) 使用，納入它僅供參考。

若備份是在啟用檔案檢查碼的情況下取得，則會存在下列鍵：

`Checksum-Algorithm`
:   用來計算此檔案檢查碼的檢查碼演算法。目前，備份清單中每個檔案所用的演算法都相同，但這在未來的版本中可能會改變。目前支援的檢查碼演算法有 `CRC32C`、`SHA224`、`SHA256`、`SHA384` 與 `SHA512`。

`Checksum`
:   為此檔案計算出的檢查碼，以一連串十六進位字元儲存，檢查碼的每個位元組對應兩個字元。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-manifest-files.html)（原文版本：18.6；核對日期：2026-10-17）
