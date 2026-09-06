## 12.11. 限制 [#](#TEXTSEARCH-LIMITATIONS)

PostgreSQL 文字搜尋功能目前有下列限制：

* 每個詞素（lexeme）的長度必須小於 2 KB。
* `tsvector` 的長度（詞素加上位置）必須小於 1 MB。
* 詞素數量必須小於 2<sup>64</sup>。
* `tsvector` 中的位置值必須大於 0，且不超過 16,383。
* `tsquery` 的 `<N>`（FOLLOWED BY）運算子所指定的比對距離不得超過 16,384。
* 每個詞素最多可有 256 個位置。
* `tsquery` 中的節點數量（詞素加上運算子）必須小於 32,768。

作為比較，PostgreSQL 8.1 文件包含 10,441 個不重複單字，總計 335,420 個單字；最常出現的單字「postgresql」在 655 份文件中共出現 6,127 次。

另一個例子是 PostgreSQL 郵件論壇封存，其中 461,020 封訊息包含 910,989 個不重複單字，共計 57,491,343 個詞素。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-limitations.html)（原文版本：18.6；核對日期：2026-09-07）
