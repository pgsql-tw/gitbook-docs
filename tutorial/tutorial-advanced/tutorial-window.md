<a id="TUTORIAL-WINDOW"></a>

## 3.5. Window 函式 [#](#TUTORIAL-WINDOW)

<a id="id-1.4.5.6.2"></a>

*Window 函式*（window function）會對一組與目前資料列有某種關聯的資料表資料列進行計算。這類似於彙總函式所能進行的計算。不過，window 函式不會像非 window 的彙總函式呼叫那樣，把資料列分組成單一輸出資料列；各資料列仍保有各自的獨立身分。在幕後，window 函式能夠存取的不只是查詢結果中的目前資料列。

以下範例說明如何將每位員工的薪資與其所屬部門的平均薪資相比較：

```

SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
```

```

  depname  | empno | salary |          avg
-----------+-------+--------+-----------------------
 develop   |    11 |   5200 | 5020.0000000000000000
 develop   |     7 |   4200 | 5020.0000000000000000
 develop   |     9 |   4500 | 5020.0000000000000000
 develop   |     8 |   6000 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     3 |   4800 | 4866.6666666666666667
 sales     |     1 |   5000 | 4866.6666666666666667
 sales     |     4 |   4800 | 4866.6666666666666667
(10 rows)
```

前三個輸出欄位直接來自資料表 `empsalary`，資料表中的每一筆資料列都對應一筆輸出資料列。第四個欄位代表所有與目前資料列具有相同 `depname` 值的資料表資料列的平均值。（這其實與非 window 的 `avg` 彙總函式是同一個函式，但 `OVER` 子句讓它被當作 window 函式處理，並在視窗框架上進行計算。）

Window 函式呼叫一定會在函式名稱與參數之後緊接著 `OVER` 子句。這就是它在語法上與一般函式或非 window 彙總函式的區別。`OVER` 子句精確決定了查詢的資料列要如何切分，以供 window 函式處理。`OVER` 中的 `PARTITION BY` 子句會將資料列分成若干組，也就是分割區（partition），同一分割區中的資料列具有相同的 `PARTITION BY` 運算式值。對每一筆資料列而言，window 函式會在與目前資料列屬於同一分割區的資料列上進行計算。

你也可以在 `OVER` 中使用 `ORDER BY`，控制 window 函式處理資料列的順序。（window 的 `ORDER BY` 甚至不必與資料列的輸出順序相同。）範例如下：

```

SELECT depname, empno, salary,
       row_number() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
```

```

  depname  | empno | salary | row_number
-----------+-------+--------+------------
 develop   |     8 |   6000 |          1
 develop   |    10 |   5200 |          2
 develop   |    11 |   5200 |          3
 develop   |     9 |   4500 |          4
 develop   |     7 |   4200 |          5
 personnel |     2 |   3900 |          1
 personnel |     5 |   3500 |          2
 sales     |     1 |   5000 |          1
 sales     |     4 |   4800 |          2
 sales     |     3 |   4800 |          3
(10 rows)
```

如這裡所示，`row_number` window 函式會依 `ORDER BY` 子句定義的順序，為每個分割區中的資料列依序編號（同值的資料列以未指定的順序編號）。`row_number` 不需要明確的參數，因為它的行為完全由 `OVER` 子句決定。

Window 函式所處理的資料列，是查詢的 `FROM` 子句所產生的「虛擬資料表」中的資料列，並經過查詢中 `WHERE`、`GROUP BY` 與 `HAVING` 子句（如果有的話）的篩選。例如，因不符合 `WHERE` 條件而被移除的資料列，任何 window 函式都看不到。一個查詢可以包含多個 window 函式，各自使用不同的 `OVER` 子句以不同方式切分資料，但它們都作用於這個虛擬資料表所定義的同一組資料列。

我們已經看過，如果資料列的順序不重要，可以省略 `ORDER BY`。也可以省略 `PARTITION
BY`，此時會只有一個包含所有資料列的分割區。

與 window 函式相關的另一個重要概念是：對每一筆資料列而言，其所屬分割區中有一組資料列稱為它的*視窗框架*（window frame）。有些 window 函式只作用於視窗框架中的資料列，而不是整個分割區。預設情況下，如果有提供 `ORDER BY`，框架會包含從分割區開頭直到目前資料列的所有資料列，再加上依 `ORDER BY` 子句與目前資料列相等的任何後續資料列。省略 `ORDER BY` 時，預設框架會包含分割區中的所有資料列。
[<a id="id-1.4.5.6.9.5"></a>[5]](#ftn.id-1.4.5.6.9.5)
以下是使用 `sum` 的範例：

```

SELECT salary, sum(salary) OVER () FROM empsalary;
```

```

 salary |  sum
--------+-------
   5200 | 47100
   5000 | 47100
   3500 | 47100
   4800 | 47100
   3900 | 47100
   4200 | 47100
   4500 | 47100
   4800 | 47100
   6000 | 47100
   5200 | 47100
(10 rows)
```

上例中，由於 `OVER` 子句中沒有 `ORDER BY`，視窗框架與分割區相同；又因為沒有 `PARTITION BY`，分割區就是整個資料表。換句話說，每個總和都是對整個資料表計算，所以每一筆輸出資料列都得到相同的結果。但如果我們加上 `ORDER BY` 子句，就會得到截然不同的結果：

```

SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
```

```

 salary |  sum
--------+-------
   3500 |  3500
   3900 |  7400
   4200 | 11600
   4500 | 16100
   4800 | 25700
   4800 | 25700
   5000 | 30700
   5200 | 41100
   5200 | 41100
   6000 | 47100
(10 rows)
```

這裡的總和是從第一筆（最低的）薪資一路累加到目前這筆，並包含與目前這筆重複的薪資（請留意重複薪資的結果）。

Window 函式只能用在查詢的 `SELECT` 清單與 `ORDER BY` 子句中，在其他地方則禁止使用，例如 `GROUP BY`、`HAVING` 與 `WHERE` 子句。這是因為在邏輯上，window 函式是在這些子句處理完之後才執行。此外，window 函式會在非 window 的彙總函式之後執行。這表示在 window 函式的參數中呼叫彙總函式是有效的，反之則不行。

如果需要在 window 計算完成之後再篩選或分組資料列，可以使用子查詢（sub-select）。例如：

```

SELECT depname, empno, salary, enroll_date
FROM
  (SELECT depname, empno, salary, enroll_date,
     row_number() OVER (PARTITION BY depname ORDER BY salary DESC, empno) AS pos
     FROM empsalary
  ) AS ss
WHERE pos < 3;
```

上面的查詢只會顯示內層查詢中 `row_number` 小於 3 的資料列（也就是每個部門的前兩筆資料列）。

當查詢涉及多個 window 函式時，可以為每個函式分別寫出 `OVER` 子句；但如果多個函式需要相同的視窗行為，這樣寫既重複又容易出錯。取而代之的做法是，在 `WINDOW` 子句中為每種視窗行為命名，再於 `OVER` 中參照。例如：

```

SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

關於 window 函式的更多細節，請參閱[第 4.2.8 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)、[第 9.22 節](../../the-sql-language/functions/functions-window.md)、[第 7.2.5 節](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-WINDOW)以及 [SELECT](../../reference/sql-commands/sql-select.md) 參考頁面。

<br>

---

<a id="ftn.id-1.4.5.6.9.5"></a>

[[5]](#id-1.4.5.6.9.5) 
還有其他定義視窗框架的選項，但本教學不會介紹。詳情請參閱[第 4.2.8 節](../../the-sql-language/sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-window.html)（原文版本：18.6；核對日期：2026-09-11）
