## 35.1. 資訊結構描述 [#](#INFOSCHEMA-SCHEMA)

資訊結構描述本身是一個名為 `information_schema` 的 schema。此 schema 會自動
存在於所有資料庫中。它的擁有者是叢集的初始資料庫使用者，該使用者自然擁有此
schema 的所有權限，包括刪除它的能力（不過這樣能節省的空間微乎其微）。

預設情況下，資訊結構描述不在 schema 搜尋路徑中，因此必須以限定名稱存取其中
的所有物件。資訊結構描述中的某些物件名稱很通用，可能也會出現在使用者應用程式
中；若要將資訊結構描述加入搜尋路徑，應特別小心。

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-schema.html)】
