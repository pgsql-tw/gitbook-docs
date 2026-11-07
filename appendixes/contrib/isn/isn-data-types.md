# F.20.1. 資料型別

<a id="ISN-DATA-TYPES"></a>

## F.20.1. 資料型別 [#](#isn-data-types) <a href="#isn-data-types" id="isn-data-types"></a>

[表 F.10](#isn-datatypes) 顯示 `isn` 模組提供的資料型別。

<a id="ISN-DATATYPES"></a>

### 表 F.10. `isn` 資料型別 [#](#isn-datatypes) <a href="#isn-datatypes" id="isn-datatypes"></a>

<table border="1" class="table" summary="isn Data Types"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>資料型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">EAN13</code></td><td>
       歐洲商品編碼，一律以 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISBN13</code></td><td>
       國際標準書號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISMN13</code></td><td>
       國際標準音樂作品編號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISSN13</code></td><td>
       國際標準期刊號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISBN</code></td><td>
       國際標準書號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">ISMN</code></td><td>
       國際標準音樂作品編號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">ISSN</code></td><td>
       國際標準期刊號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">UPC</code></td><td>
       通用產品代碼
      </td></tr></tbody></table>

<br>

注意事項：

1. ISBN13、ISMN13、ISSN13 號碼都是 EAN13 號碼。
2. EAN13 號碼不一定是 ISBN13、ISMN13 或 ISSN13（有些是）。
3. 部分 ISBN13 號碼可顯示為 ISBN。
4. 部分 ISMN13 號碼可顯示為 ISMN。
5. 部分 ISSN13 號碼可顯示為 ISSN。
6. UPC 號碼是 EAN13 號碼的子集（基本上是移除第一個 `0` 數字的 EAN13）。
7. 所有 UPC、ISBN、ISMN 與 ISSN 號碼都可表示為 EAN13 號碼。

在內部，所有這些型別使用相同表示法（64 位元整數），並可相互轉換。提供多種型別是為了控制顯示格式，以及對應該表示某個特定號碼型別的輸入進行更嚴格的有效性檢查。

`ISBN`、`ISMN` 與 `ISSN` 型別會在可能時顯示號碼短版（ISxN 10），而不適用短版的號碼則顯示為 ISxN 13 格式。`EAN13`、`ISBN13`、`ISMN13` 與 `ISSN13` 型別一律顯示 ISxN 的長版（EAN13）。

[返回 F.20. isn — 國際標準號碼的資料型別（ISBN、EAN、UPC 等）](../isn.md#isn)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/isn.html)
