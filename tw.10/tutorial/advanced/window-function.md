# 3.5. 窗函數

窗函數（window function）提供了在一個資料表中，進行資料列與資料列之間的關連運算。這部份可以和彙總函數的功能相呼應。然而，窗函數並無法像彙總函數一樣，把多個資料列運算合併為單一資料列的結果。取而代之的是，這些資料列仍然是分開並列的狀態。在這樣的情境下，窗函數能讓查詢結果的每一個資料列，都得到更多資訊。

這裡有一個列子，試著比較每一個員工他的薪資及他的部門平均薪資的情況：

```text
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
```

```text
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

前面三個欄位是由資料表 empsalary 直接取得，每一個資料列就是該資料表的每一個資料列列。而第四個欄位則呈現整個資料表中，與其 depname 相同的平均薪資。（這實際上就是由非窗函數的 avg 彙總而得，只是 OVER 修飾字讓它成為窗函數，透過「窗」的可見範圍做計算。）

窗函數都會使用 OVER 修飾字，然後緊接著窗函數及其參數。這是在語法上使其有別於一般函數或非窗函數的彙總。OVER 區段需要確切指出如何分組要被窗函數計算的資料列。PARTITION BY 在 OVER 中，意思是要以 PARTITION BY 之後的表示式來分組或拆分資料列的資料。對於每一個資料列而言，窗函數的結果是，透過所有和該資料列相同分組的資料，共同運算而得。

你也可以控制列被窗函數處理的次序，透過在 OVER 中加入 ORDER BY。（窗內的 ORDER BY 不見得需要對應到資料列輸出的次序）例子如下：

```text
SELECT depname, empno, salary,
       rank() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
```

```text
  depname  | empno | salary | rank 
-----------+-------+--------+------
 develop   |     8 |   6000 |    1
 develop   |    10 |   5200 |    2
 develop   |    11 |   5200 |    2
 develop   |     9 |   4500 |    4
 develop   |     7 |   4200 |    5
 personnel |     2 |   3900 |    1
 personnel |     5 |   3500 |    2
 sales     |     1 |   5000 |    1
 sales     |     4 |   4800 |    2
 sales     |     3 |   4800 |    2
(10 rows)
```

如上所示，rank 函數為每個有使用 ORDER BY 的分組，標記一系列數字的次序。rank 不需要特定的參數，因為它標記的範圍一定是整個 OVER 所涵蓋定的範圍。

窗函數所計算的範圍，是一個虛擬資料表的概念，是由 WHERE、GROUP BY、HAVING、或其他方式虛擬出來的。舉例來說，當某個資料列被 WHERE 過濾掉時，它也不會被任何窗函數看見。一個查詢中可以包含多個窗函數，透過不同 OVER 修飾字的指定，將資料做不同觀點的處理。但他們都會在一個相同的虛擬資料表中進行處理。

我們已經瞭解 ORDER BY 可以被省略，如果次序並不重要的話；但其實 PARITION BY 也可以省略，如果所有的資料列都只區分成一個組的話。

還有另一個窗函數相關的重要概念：對於每一個資料列來說，它會在分組中還有個分組，另稱作窗框（window frame），有一些窗函數只對窗框裡的資料列進行處理，而不是整個分組。預設的情況是，如果 ORDER BY 被指定了，以 ORDER BY 排序後，那麼窗框的範圍就是從分組的第一列到該列為止，而在那之後資料列的值都會相同。當 ORDER BY 被省略的時候，預設窗框的範圍就是整個分組。下面是使用 sum 的例子：

```text
SELECT salary, sum(salary) OVER () FROM empsalary;
```

```text
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

上面可以看到，因為在 OVER 裡面沒有 ORDER BY，窗框就等於整個分組，甚至因為沒有 PARTITION BY，所以等於整個資料表。換句話說，每一個資料列總和都是整個資料表的總計，所以我們在每一個資料列中都得到相同的結果。但如果我們加入了 ORDER BY 之後，結果將會不同：

```text
SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
```

```text
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

這裡的總和就是從第一筆（最小），加計到每一列，包含薪資相同的每一列（注意薪資相同的）。

窗函數只允許出現在 SELECT 的輸出列表及 ORDER BY 子句裡，在其他地方都是被禁止的，像是 GROUP BY，HAVING，WHERE等區段。這是因為窗函數在邏輯上，都是在他們處理完之後才進一步處理資料的。也就是說，窗函數是在非窗函數之後才執行的。這意指在窗函數中使用非窗函數是可以的，但反過來就不行了。

如果有一個需要在窗函數處理完再進行過濾或分組的查詢的話，你可以使用子查詢。舉列來說：

```text
SELECT depname, empno, salary, enroll_date
FROM
  (SELECT depname, empno, salary, enroll_date,
          rank() OVER (PARTITION BY depname ORDER BY salary DESC, empno) AS pos
     FROM empsalary
  ) AS ss
WHERE pos < 3;
```

上面的查詢只會顯示內層查詢的次序（rank）小於 3 的資料。

當一個查詢使用了多個窗函數的話，它就會分別使用 OVER 子句來描述，但如果相同的分組方式要被多個函數所引用的話，就重覆了，也容易出錯。這種情況可以使用 WINDOW 子句來取一個別名，來取代 OVER。舉個例子：

```text
SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

更多窗函數的細節可以參閱 [4.2.8 節](../../sql/syntax/4.2.-can-shu-biao-shi-shi.md#4-2-8-chuang-han-hu-jiao)、[9.21 節](../../sql/functions/9.21.-window-han-shi.md)、[7.2.5 節](../../sql/7.-zi-liao-cha-xun/7.2.-zi-liao-biao-biao-shi-shi.md)、及 [SELECT 指令](../../reference/sql-commands/select.md)的說明頁。

