<a id="TEST-DECODING"></a>

## F.45. test_decoding — 以 SQL 為基礎的 WAL 邏輯解碼測試／範例模組 [#](#test-decoding) <a href="#test-decoding" id="test-decoding"></a>

<a id="id-1.11.7.55.2"></a>

`test_decoding` 是邏輯解碼輸出外掛程式的一個範例。它本身並不做什麼特別有用的事，但可以作為開發你自己的輸出外掛程式的起點。

`test_decoding` 透過邏輯解碼機制接收 WAL，並將其解碼為所執行操作的文字表示。

透過 SQL 邏輯解碼介面使用此外掛程式時，典型的輸出可能如下：

```

postgres=# SELECT * FROM pg_logical_slot_get_changes('test_slot', NULL, NULL, 'include-xids', '0');
   lsn     | xid |                       data
-----------+-----+--------------------------------------------------
 0/16D30F8 | 691 | BEGIN
 0/16D32A0 | 691 | table public.data: INSERT: id[int4]:2 data[text]:'arg'
 0/16D32A0 | 691 | table public.data: INSERT: id[int4]:3 data[text]:'demo'
 0/16D32A0 | 691 | COMMIT
 0/16D32D8 | 692 | BEGIN
 0/16D3398 | 692 | table public.data: DELETE: id[int4]:2
 0/16D3398 | 692 | table public.data: DELETE: id[int4]:3
 0/16D3398 | 692 | COMMIT
(8 rows)
```

我們也可以取得進行中交易的變更，典型的輸出可能如下：

```

postgres[33712]=#* SELECT * FROM pg_logical_slot_get_changes('test_slot', NULL, NULL, 'stream-changes', '1');
    lsn    | xid |                       data
-----------+-----+--------------------------------------------------
 0/16B21F8 | 503 | opening a streamed block for transaction TXN 503
 0/16B21F8 | 503 | streaming change for TXN 503
 0/16B2300 | 503 | streaming change for TXN 503
 0/16B2408 | 503 | streaming change for TXN 503
 0/16BEBA0 | 503 | closing a streamed block for transaction TXN 503
 0/16B21F8 | 503 | opening a streamed block for transaction TXN 503
 0/16BECA8 | 503 | streaming change for TXN 503
 0/16BEDB0 | 503 | streaming change for TXN 503
 0/16BEEB8 | 503 | streaming change for TXN 503
 0/16BEBA0 | 503 | closing a streamed block for transaction TXN 503
(10 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/test-decoding.html)（原文版本：18.6；核對日期：2026-10-22）
