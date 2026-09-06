# 37. The Information Schema

The information schema consists of a set of views that contain information about the objects defined in the current database. The information schema is defined in the SQL standard and can therefore be expected to be portable and remain stable — unlike the system catalogs, which are specific to PostgreSQL and are modeled after implementation concerns. The information schema views do not, however, contain information about PostgreSQL-specific features; to inquire about those you need to query the system catalogs or other PostgreSQL-specific views.

{% hint style="info" %}
在資料庫中查詢限制條件資訊時，符合標準的查詢可能預期會回傳一筆資料，到數筆資料。這是因為 SQL 標準要求限制條件名稱在綱要中必須是唯一的，但是 PostgreSQL 不強制執行此限制條件。PostgreSQL 自動產生的限制條件名稱會避免在同一綱要中的重複，但是使用者可以指定重複的名稱。

查詢 information schema 檢視表（如check\_constraint\_routine\_usage，check\_constraints，domain\_constraints 和 referential\_constraints）時，可能會出現此問題。其他一些檢視表也有類似的問題，但是包含資料表名稱用以協助區分重複的資料。例如，constraint\_column\_usage，constraint\_table\_usage，table\_constraints。
{% endhint %}
