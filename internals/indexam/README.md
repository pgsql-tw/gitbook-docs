<a id="INDEXAM"></a>

## 第 63 章：索引存取方法介面定義

**目錄**

[63.1. 索引的基本 API 結構](index-api.md)

[63.2. 索引存取方法函式](index-functions.md)

[63.3. 索引掃描](index-scanning.md)

[63.4. 索引鎖定的考量](index-locking.md)

[63.5. 索引唯一性檢查](index-unique-checks.md)

[63.6. 索引成本估算函式](index-cost-estimation.md)

<a id="id-1.10.15.2"></a><a id="id-1.10.15.3"></a>

本章定義 PostgreSQL 核心系統與*索引存取方法*（index access methods）之間的介面；
索引存取方法負責管理個別的索引類型。除了這裡所規定的內容之外，核心系統對索引一無所知，
因此可以藉由撰寫附加程式碼來開發全新的索引類型。

PostgreSQL 中的所有索引在技術上都屬於所謂的
*次要索引*（secondary indexes）；也就是說，索引在實體上與它所描述的資料表檔案
是分開的。每個索引都儲存為獨立的實體*關聯*（relation），因此由
`pg_class` 目錄中的一筆項目來描述。索引的內容
完全由其索引存取方法控制。實務上，所有索引存取方法都會把索引切分成標準大小的
頁面，以便使用一般的儲存管理器與緩衝區管理器
來存取索引內容。（此外，所有現有的索引存取方法都使用[第 66.6 節](../storage/storage-page-layout.md)所述的標準頁面配置，且大多數對索引
元組標頭使用相同的格式；但這些決定並不強制存取方法遵循。）

索引實質上是從某些資料鍵值到索引所屬父資料表中資料列版本
（元組，tuple）之*元組識別碼*（tuple identifiers，即 TID）的對應。TID 由
區塊編號與該區塊內的項目編號組成（請參閱[第 66.6 節](../storage/storage-page-layout.md)）。這些資訊
足以從資料表中擷取特定的資料列版本。
索引並不直接知道在 MVCC 之下，同一個邏輯資料列可能同時存在多個
現存版本；對索引而言，每個元組都是
需要有自己的索引項目的獨立物件。因此，
更新資料列一律會為該資料列建立全新的索引項目，即使
鍵值沒有改變也是如此。（[HOT
元組](../storage/storage-hot.md)是此說法的例外；
但索引也不處理它們。）死亡元組的索引項目會在
死亡元組本身被回收時（透過 vacuum）一併回收。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexam.html)（原文版本：18.6；核對日期：2026-10-17）
