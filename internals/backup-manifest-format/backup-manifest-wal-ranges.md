## 70.3. 備份清單的 WAL 範圍物件 [#](#BACKUP-MANIFEST-WAL-RANGES)

描述 WAL 範圍的物件固定有三個鍵：

`Timeline`
:   此範圍 WAL 記錄所屬的時間軸，以整數表示。

`Start-LSN`
:   使用此備份時，在指定時間軸上必須開始重播的 LSN。LSN 採用 PostgreSQL 一般使用的格式儲存：由兩段長度各為 1 到 8 的十六進位字元字串組成，中間以斜線分隔。

`End-LSN`
:   使用此備份時，在指定時間軸上最早可以結束重播的 LSN。儲存格式與 `Start-LSN` 相同。

通常只會有一個 WAL 範圍。不過，若從備用伺服器取得備份，而該伺服器在備份期間因上游伺服器升級為主要伺服器而切換時間軸，就可能存在多個範圍，每個範圍屬於不同時間軸。同一時間軸絕不會出現多個 WAL 範圍。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-manifest-wal-ranges.html)（原文版本：18.6；核對日期：2026-09-07）
