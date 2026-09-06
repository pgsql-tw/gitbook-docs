## 8.20. `pg_lsn` 型別 [#](#DATATYPE-PG-LSN)

<a id="id-1.5.7.28.2"></a>

`pg_lsn` 資料型別可用於儲存 LSN（Log Sequence Number，日誌序號）資料；它是指向 WAL 中位置的指標。此型別是 `XLogRecPtr` 的表示法，也是 PostgreSQL 的內部系統型別。

在內部，LSN 是 64 位元整數，代表預先寫入日誌串流中的位元組位置。它以兩個最多各 8 位數的十六進位數字表示，並以斜線分隔，例如 `16/B374D848`。`pg_lsn` 型別支援標準比較運算子，如 `=` 和 `>`。可用 `-` 運算子相減兩個 LSN，結果為兩個預先寫入日誌位置相隔的位元組數。也可分別使用 `+(pg_lsn,numeric)` 與 `-(pg_lsn,numeric)` 運算子，將位元組數加至或減自 LSN。請注意，計算出的 LSN 必須在 `pg_lsn` 型別範圍內，也就是介於 `0/0` 與 `FFFFFFFF/FFFFFFFF` 之間。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-pg-lsn.html)（原文版本：18.6；核對日期：2026-09-06）
