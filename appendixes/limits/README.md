<a id="LIMITS"></a>

## 附錄 K. PostgreSQL 限制

[表 K.1](README.md#LIMITS-TABLE) 說明 PostgreSQL 的各種硬性限制。不過，在達到絕對的硬性限制之前，可能就會先遇到實務上的限制，例如效能限制或可用磁碟空間。

<a id="LIMITS-TABLE"></a>

**表 K.1. PostgreSQL 限制**

<table border="1" class="table" summary="PostgreSQL 限制"><colgroup><col/><col/><col/></colgroup><thead><tr><th>項目</th><th>上限</th><th>備註</th></tr></thead><tbody><tr><td>資料庫大小</td><td>無限制</td><td> </td></tr><tr><td>資料庫數量</td><td>4,294,950,911</td><td> </td></tr><tr><td>每個資料庫的關聯數</td><td>1,431,650,303</td><td> </td></tr><tr><td>關聯大小</td><td>32 TB</td><td><code class="symbol">BLCKSZ</code> 為預設值 8192 位元組時</td></tr><tr><td>每個資料表的資料列數</td><td>受限於 4,294,967,295 個頁面所能容納的元組數</td><td> </td></tr><tr><td>每個資料表的欄位數</td><td>1,600</td><td>還會進一步受限於元組大小必須能放入單一頁面；請參閱下方說明</td></tr><tr><td>結果集的欄位數</td><td>1,664</td><td> </td></tr><tr><td>欄位大小</td><td>1 GB</td><td> </td></tr><tr><td>每個資料表的索引數</td><td>無限制</td><td>受每個資料庫的最大關聯數限制</td></tr><tr><td>每個索引的欄位數</td><td>32</td><td>可藉由重新編譯 <span class="productname">PostgreSQL</span> 提高</td></tr><tr><td>分割鍵數</td><td>32</td><td>可藉由重新編譯 <span class="productname">PostgreSQL</span> 提高</td></tr><tr><td>識別字長度</td><td>63 位元組</td><td>可藉由重新編譯 <span class="productname">PostgreSQL</span> 提高</td></tr><tr><td>函式參數數</td><td>100</td><td>可藉由重新編譯 <span class="productname">PostgreSQL</span> 提高</td></tr><tr><td>查詢參數數</td><td>65,535</td><td> </td></tr></tbody></table>

<br>

由於要儲存的元組必須能放入單一 8192 位元組的堆積頁面，資料表的最大欄位數還會進一步減少。例如，不計元組標頭，由 1,600 個 `int` 欄位組成的元組會佔用 6400 位元組，可以存放在一個堆積頁面中；但由 1,600 個 `bigint` 欄位組成的元組會佔用 12800 位元組，因此無法放入一個堆積頁面。`text`、`varchar`、`char` 等型別的變動長度欄位，在值大到有需要時，可以將值以行外（out of line）方式存放在該資料表的 TOAST 資料表中，只有一個 18 位元組的指標必須留在資料表堆積中的元組內。較短的變動長度欄位則使用 4 位元組或 1 位元組的欄位標頭，值直接存放在堆積元組內。

已從資料表中移除的欄位，也會計入最大欄位數限制。此外，雖然新建立的元組中已移除欄位的值，在內部會於元組的 null 位元圖中標記為 null，但 null 位元圖本身也會佔用空間。

每個資料表理論上最多可以存放 2^32 個行外值；關於行外儲存的詳細討論，請參閱[第 66.2 節](../../internals/storage/storage-toast.md)。這個限制源自於使用 32 位元的 OID 來識別每個這類值。實際限制遠低於理論限制，因為隨著 OID 空間逐漸填滿，尋找仍可用的 OID 可能變得很耗費資源，進而拖慢 INSERT/UPDATE 陳述式。這通常只對包含數 TB 資料的資料表才會成為問題；分割是一種可行的因應方式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/limits.html)（原文版本：18.6；核對日期：2026-10-22）
