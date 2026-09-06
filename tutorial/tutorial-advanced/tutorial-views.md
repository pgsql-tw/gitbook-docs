## 3.2. 檢視表 [#](#TUTORIAL-VIEWS)

<a id="id-1.4.5.3.2"></a>

回顧[第 2.6 節](../tutorial-sql/tutorial-join.md)的查詢。假設天氣記錄與城市位置的合併清單對你的應用程式特別有用，但你不想每次需要時都重新輸入查詢，就可以根據該查詢建立*檢視表*。這等於為查詢命名，之後便能像一般資料表一樣參照它：

```

CREATE VIEW myview AS
    SELECT name, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;

SELECT * FROM myview;
```

善用檢視表是良好 SQL 資料庫設計的重要一環。檢視表讓你透過一致的介面，封裝資料表結構的細節；即使應用程式持續演進、資料表結構隨之改變，也能維持介面的一致性。

幾乎所有可以使用實際資料表的地方，都能使用檢視表。在其他檢視表之上建立檢視表也很常見。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-views.html)（原文版本：18.6；核對日期：2026-09-07）
