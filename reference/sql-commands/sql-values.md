<a id="id-1.9.3.185.1"></a>

## VALUES

VALUES — 計算一組資料列

## 語法

```

VALUES ( expression [, ...] ) [, ...]
    [ ORDER BY sort_expression [ ASC | DESC | USING operator ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
```

<a id="id-1.9.3.185.5"></a>

## 說明

`VALUES` 會依照指定的值運算式，計算出一個資料列值或
一組資料列值。它最常用來在較大的指令中產生一張「常數表」，
但也可以單獨使用。

當指定超過一個資料列時，所有資料列都必須擁有相同數量的元素。
結果資料表各欄的資料型別，是依該欄中出現的運算式的明確或
推導型別，套用與 `UNION` 相同的規則組合而成
（參閱 [Section 10.5](../../the-sql-language/typeconv/typeconv-union-case.md)）。

在較大的指令中，`VALUES` 在語法上允許出現在任何可以使用
`SELECT` 的地方。因為文法將它視為與
`SELECT` 相同，所以可以對 `VALUES`
指令使用 `ORDER BY`、`LIMIT`
（或等效的 `FETCH FIRST`），以及
`OFFSET` 子句。

<a id="id-1.9.3.185.6"></a>

## 參數

*`expression`*
:   要計算並插入結果資料表（資料列集合）中指定位置的常數或運算式。
    在出現於 `INSERT` 最上層的 `VALUES`
    清單中，*`expression`* 可以用
    `DEFAULT` 取代，以表示應插入目的欄位的預設值。
    `VALUES` 出現在其他情境中時不能使用 `DEFAULT`。

*`sort_expression`*
:   指示如何排序結果資料列的運算式或整數常數。
    此運算式可以用 `column1`、`column2`
    等方式參照 `VALUES` 結果的欄位。詳情請參閱
    [SELECT](sql-select.md) 文件中的
    [ORDER BY 子句](sql-select.md#SQL-ORDERBY)。

*`operator`*
:   排序運算子。詳情請參閱
    [SELECT](sql-select.md) 文件中的
    [ORDER BY 子句](sql-select.md#SQL-ORDERBY)。

*`count`*
:   要傳回的資料列的最大數量。詳情請參閱
    [SELECT](sql-select.md) 文件中的
    [LIMIT 子句](sql-select.md#SQL-LIMIT)。

*`start`*
:   在開始傳回資料列之前要略過的資料列數。
    詳情請參閱 [SELECT](sql-select.md) 文件中的
    [LIMIT 子句](sql-select.md#SQL-LIMIT)。

<a id="id-1.9.3.185.7"></a>

## 注意事項

應避免使用含有非常多資料列的 `VALUES` 清單，
因為你可能會遇到記憶體不足的錯誤或效能不佳的問題。
出現在 `INSERT` 中的 `VALUES` 是一種特殊情況
（因為所需的欄位型別可由 `INSERT` 的目標資料表得知，
不需要透過掃描 `VALUES` 清單來推導），因此它能處理的清單，可以比
其他情境中實務上可行的清單更大。

<a id="id-1.9.3.185.8"></a>

## 範例

一個單獨的 `VALUES` 指令：

```

VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

這會傳回一個兩欄三列的資料表，實際上等同於：

```

SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

更常見的情況是，`VALUES` 用在較大的 SQL 指令中。
最常見的用法是在 `INSERT` 中：

```

INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');
```

在 `INSERT` 的情境中，`VALUES` 清單中的項目可以是
`DEFAULT`，以表示此處應使用欄位預設值，而非指定值：

```

INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, DEFAULT, 'Comedy', '82 minutes'),
    ('T_601', 'Yojimbo', 106, DEFAULT, 'Drama', DEFAULT);
```

`VALUES` 也可以用在能夠撰寫子 `SELECT` 的地方，
例如在 `FROM` 子句中：

```

SELECT f.*
  FROM films f, (VALUES('MGM', 'Horror'), ('UA', 'Sci-Fi')) AS t (studio, kind)
  WHERE f.studio = t.studio AND f.kind = t.kind;

UPDATE employees SET salary = salary * v.increase
  FROM (VALUES(1, 200000, 1.2), (2, 400000, 1.4)) AS v (depno, target, increase)
  WHERE employees.depno = v.depno AND employees.sales >= v.target;
```

請注意，當 `VALUES` 用在 `FROM` 子句中時，
必須有一個 `AS` 子句，這點與 `SELECT` 的
情況相同。並不要求 `AS` 子句為所有欄位都指定名稱，
但這麼做是良好的做法。（在 PostgreSQL 中，
`VALUES` 的預設欄位名稱為 `column1`、
`column2` 等，但在其他資料庫系統中，這些名稱
可能有所不同。）

當 `VALUES` 用在 `INSERT` 中時，值會自動強制轉型為
對應目的欄位的資料型別。當它用在其他情境中時，
可能需要指定正確的資料型別。若所有項目都是加上引號的
常值常數，只要對第一個項目進行強制轉型即可確定
所有項目所假定的型別：

```

SELECT * FROM machines
WHERE ip_address IN (VALUES('192.168.0.1'::inet), ('192.168.0.10'), ('192.168.1.43'));
```

### 提示

對於簡單的 `IN` 測試，比起像上面那樣撰寫
`VALUES` 查詢，最好改用
[純量清單](../../the-sql-language/functions/functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR)
形式的 `IN`。純量清單的方式需要輸入的內容較少，
通常也更有效率。

<a id="id-1.9.3.185.9"></a>

## 相容性

`VALUES` 符合 SQL 標準。
`LIMIT` 與 `OFFSET` 是
PostgreSQL 的擴充功能；另請參閱
[SELECT](sql-select.md)。

<a id="id-1.9.3.185.10"></a>

## 參見

[INSERT](sql-insert.md), [SELECT](sql-select.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-values.html)（原文版本：18.6；核對日期：2026-09-28）
