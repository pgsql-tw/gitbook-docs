<a id="TYPECONV-UNION-CASE"></a>

## 10.5. `UNION`、`CASE` 與相關結構 [#](#TYPECONV-UNION-CASE)

<a id="id-1.5.9.10.2"></a><a id="id-1.5.9.10.3"></a><a id="id-1.5.9.10.4"></a><a id="id-1.5.9.10.5"></a><a id="id-1.5.9.10.6"></a><a id="id-1.5.9.10.7"></a>

SQL 的 `UNION` 結構必須將可能不相同的型別統一起來，才能成為單一的結果集合。解析演算法會分別套用到 union 查詢的每一個輸出欄位。`INTERSECT` 與 `EXCEPT` 結構也以與 `UNION` 相同的方式解析不相同的型別。其他一些結構，包括 `CASE`、`ARRAY`、`VALUES`，以及 `GREATEST` 與 `LEAST` 函式，也使用完全相同的演算法來統一其組成運算式並選擇結果資料型別。

<a id="id-1.5.9.10.9"></a>

**`UNION`、`CASE` 與相關結構的型別解析**

1. 如果所有輸入都是相同型別，且該型別不是 `unknown`，就解析為該型別。
2. 如果任何輸入是網域型別，在後續所有步驟中都將它視為該網域的基礎型別。
   [<a id="id-1.5.9.10.9.3.1.1"></a>[12]](#ftn.id-1.5.9.10.9.3.1.1)
3. 如果所有輸入都是 `unknown` 型別，就解析為 `text` 型別（字串類別的優先型別）。否則，在其餘規則中會忽略 `unknown` 輸入。
4. 如果非 unknown 的輸入並非全都屬於同一個型別類別，就失敗。
5. 選擇第一個非 unknown 的輸入型別作為候選型別，然後由左至右依序考慮其他每一個非 unknown 的輸入型別。
   [<a id="id-1.5.9.10.9.6.1.1"></a>[13]](#ftn.id-1.5.9.10.9.6.1.1)
   如果候選型別可以隱含轉換為另一個型別，但反過來不行，就選擇另一個型別作為新的候選型別。接著繼續考慮其餘的輸入。如果在這個過程的任何階段選到了優先型別，就不再考慮其他輸入。
6. 將所有輸入轉換為最終的候選型別。如果某個輸入型別無法隱含轉換為候選型別，就失敗。

以下是一些範例。

<a id="id-1.5.9.10.11"></a>

**範例 10.10. Union 中型別未完整指定時的型別解析**

```

SELECT text 'a' AS "text" UNION SELECT 'b';

 text
------
 a
 b
(2 rows)
```

這裡，型別未知的字面值 `'b'` 會被解析為 `text` 型別。

<br><a id="id-1.5.9.10.12"></a>

**範例 10.11. 簡單 Union 中的型別解析**

```

SELECT 1.2 AS "numeric" UNION SELECT 1;

 numeric
---------
       1
     1.2
(2 rows)
```

字面值 `1.2` 的型別是 `numeric`，而 `integer` 值 `1` 可以隱含轉換為 `numeric`，因此會使用該型別。

<br><a id="id-1.5.9.10.13"></a>

**範例 10.12. 對調順序的 Union 中的型別解析**

```

SELECT 1 AS "real" UNION SELECT CAST('2.2' AS REAL);

 real
------
    1
  2.2
(2 rows)
```

這裡，由於 `real` 型別無法隱含轉換為 `integer`，但 `integer` 可以隱含轉換為 `real`，因此 union 的結果型別會解析為 `real`。

<br><a id="id-1.5.9.10.14"></a>

**範例 10.13. 巢狀 Union 中的型別解析**

```

SELECT NULL UNION SELECT NULL UNION SELECT 1;

ERROR:  UNION types text and integer cannot be matched
```

會發生這個錯誤，是因為 PostgreSQL 將多個 `UNION` 視為一連串兩兩配對的巢狀運算；也就是說，這個輸入等同於

```

(SELECT NULL UNION SELECT NULL) UNION SELECT 1;
```

依照上述規則，內層的 `UNION` 會被解析為輸出 `text` 型別。接著外層 `UNION` 的輸入型別是 `text` 與 `integer`，因而產生上述錯誤。要解決這個問題，可以確保最左邊的 `UNION` 至少有一個輸入是想要的結果型別。

`INTERSECT` 與 `EXCEPT` 運算同樣是兩兩配對解析。不過，本節所述的其他結構則會在單一解析步驟中考慮所有輸入。

<br>

<br>

---

<a id="ftn.id-1.5.9.10.9.3.1.1"></a>

[[12]](#id-1.5.9.10.9.3.1.1) 
與運算子和函式對網域輸入的處理方式有些類似，這項行為讓網域型別能夠在 `UNION` 或類似結構中保留下來，前提是使用者必須小心確保所有輸入都以隱含或明確的方式屬於該確切型別。否則會使用該網域的基礎型別。

<a id="ftn.id-1.5.9.10.9.6.1.1"></a>

[[13]](#id-1.5.9.10.9.6.1.1) 
由於歷史因素，`CASE` 會將它的 `ELSE` 子句（如果有的話）視為「第一個」輸入，之後才考慮 `THEN` 子句。在其他所有情況下，「由左至右」指的是運算式在查詢文字中出現的順序。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv-union-case.html)（原文版本：18.6；核對日期：2026-09-11）
