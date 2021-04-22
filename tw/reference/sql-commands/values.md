# VALUES

VALUES — 産生一組資料列

## 語法

```text
VALUES ( expression [, ...] ) [, ...]
    [ ORDER BY sort_expression [ ASC | DESC | USING operator ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
```

## 說明

VALUES 由指定值表示式産生資料列或就是一組資料列。它通常用於在更大的指令中産生「常數資料表」，但它也可以單獨使用。

當指定多個資料列時，所有資料列必須具有相同數量的元素。結果的資料表的資料型別是透過組合顯示或推斷出現在該欄位中表示式的型別來決定的，其使用與 UNION 相同的規則（見[第 10.5 節](../../the-sql-language/type-conversion/union-case-and-related-constructs.md)）。

在較大的指令中，VALUES 在 SELECT 的任何位置在語法上都是被允許的。由於語法將其視為 SELECT，因此可以使用 ORDER BY、LIMIT（或等價的 FETCH FIRST）和 OFFSET 子句以及 VALUES 指令。

## 參數

_`expression`_

計算並在結果資料表（資料列集合）中的指定位置插入的常數或表示式。在出現在 INSERT 最上層的 VALUES 列表中，可以用 DEFAULT 替換表示式來指示應該插入目標欄位的預設值。當 VALUES 出現在其他層級時，就不能使用 DEFAULT。

_`sort_expression`_

指示如何對結果資料列進行排序的表示式或整數常數。此表示式可以將 VALUES 結果的欄位引用為 column1，column2 等。有關更多詳細訊息，請參閱 [ORDER BY 子句](select.md#order-by-clause)。

_`operator`_

排序運算符號。有關詳細訊息，請參閱 [ORDER BY 子句](select.md#order-by-clause)。

_`count`_

要回傳的最大資料列數。有關詳情，請參閱 [LIMIT 子句](select.md#limit-clause)。

_`start`_

在開始回傳資料列之前要跳過的列數。有關詳情，請參閱 [LIMIT 子句](select.md#limit-clause)。

## 注意

應該避免使用大量資料列的 VALUES 列表，因為可能會遇到記憶體不足或效能不佳的情況。在 INSERT 中出現的 VALUES 是一種特殊情況（因為所需的欄位型別可從 INSERT 的目標資料表中得知，而不需要透過掃描 VALUES 列表來推斷），所以它可以處理比其他情況實際可用的更大列表。

## 範例

直接的 VALUES 指令：

```text
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

這將回傳一個兩個欄位和三個資料列的資料表。它實際上相當於：

```text
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

更通常的情況是，在更大的 SQL 指令中使用 VALUES。INSERT 中最常見的用法是：

```text
INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');
```

在 INSERT 的指令中，VALUES 列表的項目可以是 DEFAULT，以表示在此應該使用欄位的預設值而不是指定值：

```text
INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, DEFAULT, 'Comedy', '82 minutes'),
    ('T_601', 'Yojimbo', 106, DEFAULT, 'Drama', DEFAULT);
```

在可能寫入子 SELECT 的地方也可以使用 VALUES，例如在 FROM 子句中：

```text
SELECT f.*
  FROM films f, (VALUES('MGM', 'Horror'), ('UA', 'Sci-Fi')) AS t (studio, kind)
  WHERE f.studio = t.studio AND f.kind = t.kind;

UPDATE employees SET salary = salary * v.increase
  FROM (VALUES(1, 200000, 1.2), (2, 400000, 1.4)) AS v (depno, target, increase)
  WHERE employees.depno = v.depno AND employees.sales >= v.target;
```

請注意，在 FROM 子句中使用 VALUES 時需要 AS 子句，對於 SELECT 也是如此。 AS 子句不需要為所有欄位指定名稱，但這是很好的做法。（VALUES 的預設欄位名稱是 PostgreSQL 中的 column1，column2 等，但這些名稱在其他資料庫系統中可能會不同。）

在 INSERT 中使用 VALUES 時，這些值會全部自動強制轉為相應目標欄位的資料型別。 當它在其他指令部份中使用時，可能需要指定正確的資料型別。如果項目都是引用文字常數，強制第一個項目就足以決定所有的假設型別：

```text
SELECT * FROM machines
WHERE ip_address IN (VALUES('192.168.0.1'::inet), ('192.168.0.10'), ('192.168.1.43'));
```

### 小技巧

對於簡單的 IN 測試，最好依賴 IN 的 [scalar 列表](../../the-sql-language/functions-and-operators/row-and-array-comparisons.md#9-23-1-in)形式，而不是像上面那樣撰寫 VALUES 查詢。scalar 列表方式只需要更少的寫入，並且通常效能更高。

## 相容性

VALUES 符合 SQL 標準。LIMIT 和 OFFSET 是 PostgreSQL 的延伸功能；請參閱 [SELECT](select.md) 下的內容。

## 參閱

[INSERT](insert.md), [SELECT](select.md)

