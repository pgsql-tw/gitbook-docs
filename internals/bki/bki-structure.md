## 68.5. 啟動初始化 BKI 檔案的結構 [#](#BKI-STRUCTURE)

只有在 `open` 命令所需的資料表已存在，且其中包含要開啟之資料表的項目時，才能使用 `open`。（最少需要的資料表是 `pg_class`、`pg_attribute`、`pg_proc` 與 `pg_type`。）為了填入這些資料表本身，帶有 `bootstrap` 選項的 `create` 會隱含地開啟剛建立的資料表，以供插入資料。

同樣地，只有在所需的系統目錄已建立並填入資料後，才能使用 `declare index` 與 `declare toast` 命令。

因此，`postgres.bki` 檔案必須採用下列結構：

1. 使用 `create bootstrap` 建立其中一個關鍵資料表。
2. 使用 `insert` 插入至少描述這些關鍵資料表的資料。
3. 執行 `close`。
4. 對其他關鍵資料表重複上述步驟。
5. 使用 `create`（不加 `bootstrap`）建立非關鍵資料表。
6. 執行 `open`。
7. 使用 `insert` 插入所需資料。
8. 執行 `close`。
9. 對其他非關鍵資料表重複上述步驟。
10. 定義索引與 TOAST 資料表。
11. 執行 `build indices`。

無疑還存在其他尚未記載的順序相依關係。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bki-structure.html)（原文版本：18.6；核對日期：2026-09-07）
