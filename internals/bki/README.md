<a id="BKI"></a>

## 第 68 章 系統目錄宣告與初始內容

**目錄**

- [68.1. 系統目錄宣告規則](system-catalog-declarations.md)

- [68.2. 系統目錄初始資料](system-catalog-initial-data.md)
  - [68.2.1. 資料檔格式](system-catalog-initial-data.md#system-catalog-initial-data-format)

  - [68.2.2. OID 指派](system-catalog-initial-data.md#system-catalog-oid-assignment)

  - [68.2.3. OID 參照查找](system-catalog-initial-data.md#system-catalog-oid-references)

  - [68.2.4. 自動建立陣列型別](system-catalog-initial-data.md#system-catalog-auto-array-types)

  - [68.2.5. 編輯資料檔的作法](system-catalog-initial-data.md#system-catalog-recipes)

- [68.3. BKI 檔案格式](bki-format.md)

- [68.4. BKI 命令](bki-commands.md)

- [68.5. 初始建置 BKI 檔案的結構](bki-structure.md)

- [68.6. BKI 範例](bki-example.md)

PostgreSQL 使用許多不同的系統目錄來追蹤資料庫物件（例如資料表與函式）的存在與屬性。實體上，系統目錄與一般使用者資料表並無差異，但後端的 C 程式碼知道每個系統目錄的結構與屬性，並且可以在低階層直接操作它。因此，舉例來說，不建議嘗試在執行中即時變更系統目錄的結構；這樣做會破壞 C 程式碼中對系統目錄資料列配置方式所內建的假設。不過，系統目錄的結構可能會在主要版本之間改變。

系統目錄的結構宣告在原始碼樹 `src/include/catalog/` 目錄中特殊格式的 C 標頭檔裡。每個系統目錄都有一個以該系統目錄命名的標頭檔（例如 `pg_class` 對應 `pg_class.h`），其中定義該系統目錄擁有的欄位集合，以及其 OID 等其他一些基本屬性。

許多系統目錄都有初始資料，必須在 initdb 的「初始建置」（bootstrap）階段載入，讓系統達到能夠執行 SQL 命令的狀態。（例如，`pg_class.h` 必須包含一筆描述它自身的項目，以及每個其他系統目錄與索引各一筆項目。）這些初始資料以可編輯的形式保存在資料檔中，這些資料檔同樣存放在 `src/include/catalog/` 目錄。例如，`pg_proc.dat` 描述了所有必須插入 `pg_proc` 系統目錄的初始資料列。

為了建立系統目錄檔並將這些初始資料載入其中，以初始建置模式執行的後端會讀取一個包含命令與初始資料的 BKI（Backend Interface，後端介面）檔案。此模式所使用的 `postgres.bki` 檔案，是在建置 PostgreSQL 發行版時，由一支名為 `genbki.pl` 的 Perl 腳本根據前述的標頭檔與資料檔產生的。雖然 `postgres.bki` 專屬於特定的 PostgreSQL 版本，但它與平台無關，並安裝在安裝樹的 `share` 子目錄中。

`genbki.pl` 也會為每個系統目錄產生一個衍生的標頭檔，例如為 `pg_class` 系統目錄產生 `pg_class_d.h`。此檔案包含自動產生的巨集定義，並且可能包含其他巨集、列舉宣告等，這些內容對於讀取特定系統目錄的用戶端 C 程式碼可能很有用。

大多數 PostgreSQL 開發者不需要直接處理 BKI 檔案，但幾乎任何在後端新增的非瑣碎功能，都需要修改系統目錄標頭檔和／或初始資料檔。本章其餘部分提供這方面的一些資訊，並且為了完整起見，說明 BKI 檔案格式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bki.html)（原文版本：18.6；核對日期：2026-10-17）
