# 3.2. Views[^1]

讓我們回到 2.6 節的查詢範例。假設關連天氣資訊和城市位置的結果，是你的應用中特別常用的，但你並不想要每次都要輸入一長串的查詢語句。那麼，你可以為這個查詢語句建立一個「View」，你可以取一個名字，當你需要使用的時候，你可以把它當作一個表格來使用：

```
CREATE VIEW myview AS
    SELECT city, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;

SELECT * FROM myview;
```

把 View 作妥善的使用，對於良好的 SQL 資料庫設定而言，是很關鍵的部份。View 允許你可封裝你的表格結構與細節，當你的應用系統在逐步發展成熟的過程中，扮演一致性的資料介面。

View 可以用在大多數表格可以使用的地方。用 view 來封裝其他 view 的情況，也不少見。

---

[^1]: [PostgreSQL: Documentation: 10: 3.2. Views](https://www.postgresql.org/docs/10/static/tutorial-views.html)

