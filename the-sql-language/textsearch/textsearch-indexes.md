<a id="TEXTSEARCH-INDEXES"></a>

## 12.9. 文字搜尋的建議索引型別 [#](#TEXTSEARCH-INDEXES)

<a id="id-1.5.11.12.2"></a>

有兩種索引可以用來加速全文檢索：[GIN](../../internals/indextypes/gin.md) 與 [GiST](../../internals/indextypes/gist.md)。請注意，全文檢索並非一定要使用索引，但如果某個欄位經常被搜尋，通常會希望為它建立索引。

要建立這類索引，請使用下列其中一種方式：

<a id="id-1.5.11.12.4.1.1.1.1"></a> `CREATE INDEX name ON table USING GIN (column);`
:   建立以 GIN（Generalized Inverted Index，通用反向索引）為基礎的索引。*`column`* 必須是 `tsvector` 型別。

<a id="id-1.5.11.12.4.1.2.1.1"></a> `CREATE INDEX name ON table USING GIST (column [ { DEFAULT | tsvector_ops } (siglen = number) ] );`
:   建立以 GiST（Generalized Search Tree，通用搜尋樹）為基礎的索引。*`column`* 可以是 `tsvector` 或 `tsquery` 型別。選用的整數參數 `siglen` 決定以位元組為單位的簽章長度（詳見下文）。

GIN 索引是文字搜尋的首選索引型別。作為反向索引，它們會為每個單字（詞素）建立一個索引項目，並附上相符位置的壓縮清單。多字搜尋可以先找出第一個相符項目，再使用索引移除缺少其他單字的資料列。GIN 索引只儲存 `tsvector` 值中的單字（詞素），並不儲存它們的權重標籤。因此，使用涉及權重的查詢時，需要重新檢查資料表的資料列。

GiST 索引是*有損的*（lossy），也就是說，索引可能會產生錯誤的相符結果，因此必須檢查實際的資料表資料列來排除這些錯誤的相符結果。（PostgreSQL 會在需要時自動進行這項檢查。）GiST 索引之所以有損，是因為每份文件在索引中都以固定長度的簽章來表示。以位元組為單位的簽章長度，由選用的整數參數 `siglen` 的值決定。預設的簽章長度（未指定 `siglen` 時）是 124 位元組，最大簽章長度是 2024 位元組。簽章的產生方式，是將每個單字雜湊到一個 n 位元字串中的單一位元，再將所有這些位元進行 OR 運算，產生 n 位元的文件簽章。當兩個單字雜湊到同一個位元位置時，就會產生錯誤的相符結果。如果查詢中的所有單字都有相符項目（無論是真的還是錯誤的），就必須取出資料表的資料列，檢查相符結果是否正確。較長的簽章能帶來更精確的搜尋（掃描較小比例的索引與較少的 heap 頁面），代價是索引會比較大。

GiST 索引可以是涵蓋索引（covering index），也就是可以使用 `INCLUDE` 子句。被包含的欄位可以是沒有任何 GiST 運算子類別的資料型別。被包含的屬性會以未壓縮的形式儲存。

有損性會造成效能下降，因為必須取出最後證明是錯誤相符結果的資料表紀錄，而這是不必要的。由於隨機存取資料表紀錄很慢，這限制了 GiST 索引的實用性。錯誤相符結果的可能性取決於數個因素，特別是不重複單字的數量，因此建議使用字典來減少這個數量。

請注意，增加 [maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) 通常可以縮短 GIN 索引的建立時間，而 GiST 索引的建立時間則不受這個參數影響。

對大型集合進行分割，並適當使用 GIN 與 GiST 索引，可以實作出支援線上更新的高速搜尋。分割可以在資料庫層級使用資料表繼承來完成，也可以將文件分散到多台伺服器上，再收集外部的搜尋結果，例如透過[外部資料](../ddl/ddl-foreign-data.md)存取。後者之所以可行，是因為排名函式只使用本地資訊。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-indexes.html)（原文版本：18.6；核對日期：2026-09-11）
