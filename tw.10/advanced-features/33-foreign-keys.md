# 3.3. 外部索引鍵[^1]

回想一下在[第 2 章](/the-sql-language.md)中的表格 weather 及 cities，思考下列問題：  
你想要保證沒有另一個人可以新增在 cities 中沒有的城市資料到 weather 中。這就是所謂資料關連性的管理。在簡單的資料庫系統當中，可能會這樣實作：先檢查 cities 中是否已有對應的資料，然後再決定表格 weather 中新增或拒絕新的天氣資料。這個辦法還有很多問題，而且很不方便，所以 PostgreSQL 可以幫助你解決這個需求。

新的表格宣告如下所示：

```
CREATE TABLE cities (
        city     varchar(80) primary key,
        location point
);

CREATE TABLE weather (
        city      varchar(80) references cities(city),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
```

現在嘗試新增一筆不合理的資料：

```
INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');
```

```
ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".
```

外部索引鍵（foreign key）的行為可以讓你的應用程式變得容易調整。我們在這個導覽中不會在深入這個簡單的例子了，但你可以在[第 5 章](/ii-the-sql-language/data-definition.md)取得進一步的資訊。正確地使用外部索引鍵，可以改善資料庫應用程式的品質，所以強烈建議一定要好好學習它。

---

[^1]: [PostgreSQL: Documentation: 10: 3.3. Foreign Keys](/PostgreSQL: Documentation: 10: 3.3. Foreign Keys)

