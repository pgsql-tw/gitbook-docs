# 10.5. UNION、CASE 等相關結構

SQL UNION 結構必須匹配可能不相似的型別才能成為單個結果集合。解析演算法分別套用於合併集合查詢的每個輸出欄位。INTERSECT 和 EXCEPT 結構以與 UNION 相同的方式解析不同型別。CASE，ARRAY，VALUES，GREATEST 和 LEAST 結構使用相同的演算法來匹配其組合表示式並選擇結果資料型別。

**UNION，CASE 和相關結構的型別解析**

1. 如果所有輸入屬於同一型別且不是未知，就以該型別解析。
2.  如果任何輸入屬於 domain 型別，則將其視為 domain 的基本型別進行所有後續步驟。

    **註：有點像處理運算子和函數的 domain 輸入，這種行為允許透過 UNION 或類似結構保留 doamin 型別，只要使用者小心確保所有輸入都能確定該型別。否則， domain 的基本型別將是首選。**
3. 如果所有輸入都是未知類型，則解析為 text 型別（字串類別的偏好型別）。否則，為了剩餘規則的處理，將忽略未知輸入。
4. 如果非未知輸入不是所有相同的型別類別，則失敗。
5. 選擇第一個非未知輸入型別，如果有，則選擇該類別中的偏好型別。
6. 否則，選擇允許所有前面的非未知輸入直接轉換為它的最後一個非未知輸入型別。 （總是有這樣的型別，因為列表中至少第一個型別必須滿足這個條件。）
7. 將所有輸入轉換為所選型別。如果沒有從給予輸入到所選型別的轉換，則失敗。

一些例子如下。

**Example 10.10. 在 UNION 中使用未指定型別輸入解析方案**

```
SELECT text 'a' AS "text" UNION SELECT 'b';

 text
------
 a
 b
(2 rows)
```

在這裡，未知型別文字「b」將被解析為 text 型別。\


**Example 10.11. 在簡單 UNION 中的型別解析**

```
SELECT 1.2 AS "numeric" UNION SELECT 1;

 numeric
---------
       1
     1.2
(2 rows)
```

文字 1.2 是數字型別，整數值 1 可以直接轉換為數字，因此使用該型別。\


**Example 10.12. 在轉置 UNION 中的型別轉換**

```
SELECT 1 AS "real" UNION SELECT CAST('2.2' AS REAL);

 real
------
    1
  2.2
(2 rows)
```

這裡，由於型別 real 不能直接轉換為整數，但整數可以直接轉換為實數，因此 union 結果型別被解析為 real。\


**Example 10.13. 在巢狀 UNION 中的型別解析**

```
SELECT NULL UNION SELECT NULL UNION SELECT 1;

ERROR:  UNION types text and integer cannot be matched
```

此失敗是因為 PostgreSQL 將多個 UNION 視為巢狀的成對操作；也就是說，與以下的輸入是相同的

```
(SELECT NULL UNION SELECT NULL) UNION SELECT 1;
```

根據上面給予的規則，內部 UNION 被解析為 text。然後外部 UNION 具有 text 和 integer 型別的輸入，導致觀察的錯誤。可以透過確保最左邊的 UNION 至少具有所需結果型別的一種輸入來解決此問題。

INTERSECT 和 EXCEPT 操作同樣成對處理。然而，本節中描述的其他結構同樣在一套解析步驟中考慮它們的所有輸入。\
\


