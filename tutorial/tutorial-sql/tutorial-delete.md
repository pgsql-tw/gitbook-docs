## 2.9. 刪除 [#](#TUTORIAL-DELETE)

<a id="id-1.4.4.10.2"></a>

你可以使用 `DELETE` 命令從資料表移除資料列。假設你不再關心 Hayward 的天氣，可以如下從資料表刪除這些資料列：

```

DELETE FROM weather WHERE city = 'Hayward';
```

所有屬於 Hayward 的天氣記錄都會被移除。

```

SELECT * FROM weather;
```

```

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
(2 rows)
```

使用下列形式的陳述式時必須小心：

```

DELETE FROM tablename;
```

若未指定條件，`DELETE` 會移除指定資料表中的*所有*資料列，使其成為空資料表。系統執行前不會要求確認！

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-delete.html)（原文版本：18.6；核對日期：2026-09-07）
