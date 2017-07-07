# 2.2. 概念[^1]

PostgreSQL 是一個關連式資料庫管理系統（RDBMS）。這表示它是一個管理關連性質資料的系統。關連性，基本上在數學裡是以 table 的形式來表現的。今天，以 table 為形式儲存資料是很常見的事，它是很自然的表現，但也有很多其他組識資料庫的方式。在　Unix-like的作業系統中，檔案和目錄是一個階層式資料庫的案例。更先進的發展是採用物件導向式的資料庫。

每一個 table 是很多 row 的集合。而每一個 row 則以許多相同集合的 column 所組成。每一個 column 被指定了特定的資料型別。每一個 row 中的 column 次序是固定的。很重要且必須記得的是，SQL 並不保證 row 在 table 中的次序（雖然他們可以在顯示的時候被明確表現）。

資料庫中 table 被集合起來，而很多的資料庫則被一個 PostgreSQL 服務所管理，而形成一個資料庫叢集。

---

[^1]: [PostgreSQL: Documentation: 10: 2.2. Concepts](https://www.postgresql.org/docs/10/static/tutorial-concepts.html)

