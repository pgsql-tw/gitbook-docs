<a id="SYSTEM-CATALOG-DECLARATIONS"></a>

## 68.1. 系統目錄宣告規則 [#](#SYSTEM-CATALOG-DECLARATIONS)

目錄標頭檔的關鍵部分是一個 C 結構定義，描述目錄中每一筆資料列的配置。它以 `CATALOG` 巨集開頭，就 C 編譯器而言，這只是 `typedef struct
FormData_catalogname` 的簡寫。結構中的每個成員欄位都會產生一個目錄欄位。成員欄位可以使用 `genbki.h` 中所述的 BKI 屬性巨集加以標註，例如為欄位定義預設值，或將它標記為可為 null 或不可為 null。`CATALOG` 這一行也可以使用 `genbki.h` 中所述的其他一些 BKI 屬性巨集加以標註，以定義整個目錄的其他屬性，例如它是否為共享關聯。

系統目錄快取程式碼（以及一般而言大多數處理目錄的程式碼）假設所有系統目錄元組（tuple）的固定長度部分確實存在，因為它會將這個 C 結構宣告直接對應到這些元組上。因此，所有變動長度欄位與可為 null 的欄位都必須放在最後，而且不能以結構成員的方式存取。舉例來說，如果你嘗試將 `pg_type`.`typrelid` 設為 NULL，那麼當某段程式碼嘗試參照 `typetup->typrelid` 時就會失敗（或者更糟，參照 `typetup->typelem` 時也會失敗，因為它位於 `typrelid` 之後）。這會造成隨機的錯誤，甚至是區段錯誤（segmentation violation）。

作為對這類錯誤的部分防護，變動長度或可為 null 的欄位不應直接讓 C 編譯器看見。做法是將它們包在 `#ifdef
CATALOG_VARLEN` ... `#endif` 之中（其中 `CATALOG_VARLEN` 是一個從未定義的符號）。這可以防止 C 程式碼草率地嘗試存取可能不存在、或可能位於其他偏移位置的欄位。作為防止建立不正確資料列的另一道獨立防護，我們要求所有應該不可為 null 的欄位都必須在 `pg_attribute` 中如此標記。若目錄欄位為固定寬度，且其前方沒有任何可為 null 或變動寬度的欄位，初始建置（bootstrap）程式碼會自動將它標記為 `NOT NULL`。在此規則不足之處，你可以視需要使用 `BKI_FORCE_NOT_NULL` 與 `BKI_FORCE_NULL` 標註來強制進行正確的標記。

前端程式碼不應引入任何 `pg_xxx.h` 目錄標頭檔，因為這些檔案可能含有在後端之外無法編譯的 C 程式碼。（通常這是因為這些檔案也含有 `src/backend/catalog/` 底下各檔案中函式的宣告。）前端程式碼可以改為引入對應的、自動產生的 `pg_xxx_d.h` 標頭檔，其中會含有 OID 的 `#define` 以及其他任何可能對用戶端有用的資料。如果你希望目錄標頭檔中的巨集或其他程式碼能讓前端程式碼看見，請在該區段前後寫上 `#ifdef
EXPOSE_TO_CLIENT_CODE` ... `#endif`，以指示 `genbki.pl` 將該區段複製到 `pg_xxx_d.h` 標頭檔中。

有少數幾個目錄是如此基礎，以至於它們甚至無法用大多數目錄所使用的 BKI `create` 命令來建立，因為該命令需要將資訊寫入這些目錄，以描述新的目錄。這些目錄稱為*初始建置*（bootstrap）目錄，而定義一個這樣的目錄需要大量額外的工作：你必須在 `pg_class` 與 `pg_type` 的預先載入內容中，為它們手動準備適當的項目，而且每當目錄結構後續有所變更時，這些項目也需要隨之更新。（初始建置目錄也需要在 `pg_attribute` 中有預先載入的項目，但幸好如今 `genbki.pl` 會處理這項雜務。）請盡可能避免讓新的目錄成為初始建置目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/system-catalog-declarations.html)（原文版本：18.6；核對日期：2026-10-17）
