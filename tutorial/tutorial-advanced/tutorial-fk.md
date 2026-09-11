<a id="TUTORIAL-FK"></a>

## 3.3. 外部索引鍵 [#](#TUTORIAL-FK)

<a id="id-1.4.5.4.2"></a><a id="id-1.4.5.4.3"></a>

回想[第 2 章](../tutorial-sql/README.md)中的 `weather` 與 `cities` 資料表。考慮下列問題：你想確保沒有人能在 `weather` 資料表中插入於 `cities` 資料表裡找不到相符項目的資料列。這稱為維護資料的*參照完整性*（referential integrity）。在簡單的資料庫系統中，這項功能（如果有實作的話）會先查看 `cities` 資料表，檢查是否存在相符的記錄，再決定插入或拒絕新的 `weather` 記錄。這種做法有不少問題，而且非常不方便，因此 PostgreSQL 可以替你處理這件事。

新的資料表宣告會像這樣：

```

CREATE TABLE cities (
        name     varchar(80) primary key,
        location point
);

CREATE TABLE weather (
        city      varchar(80) references cities(name),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
```

現在試著插入一筆無效的記錄：

```

INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');
```

```

ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".
```

外部索引鍵的行為可以依你的應用程式精細調整。本教學不會超出這個簡單範例的範圍，更多資訊請參閱[第 5 章](../../the-sql-language/ddl/README.md)。正確使用外部索引鍵一定能提升資料庫應用程式的品質，因此強烈建議你深入瞭解。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-fk.html)（原文版本：18.6；核對日期：2026-09-11）
