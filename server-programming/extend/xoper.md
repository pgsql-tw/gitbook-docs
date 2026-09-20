<a id="XOPER"></a>
## 36.14. 使用者自訂運算子 [#](#XOPER)

<a id="id-1.8.3.17.2"></a>

每個運算子都是呼叫底層函式（真正執行工作的函式）的「語法糖」；因此你必須先建立底層函式，才能建立運算子。不過，運算子*不僅僅*是語法糖，因為它還帶有額外的資訊，能協助查詢規劃器最佳化使用該運算子的查詢。下一節會專門說明這些額外的資訊。

PostgreSQL 支援前置與中置運算子。運算子可以多載；<a id="id-1.8.3.17.4.2"></a>也就是說，同一個運算子名稱可以用於運算元個數與型別皆不同的多個不同運算子。執行查詢時，系統會依據所提供運算元的個數與型別，來判斷要呼叫哪一個運算子。

以下是建立一個用來把兩個複數相加的運算子的範例。我們假設已經先建立了 `complex` 型別的定義（見[第 36.13 節](xtypes.md)）。首先我們需要一個真正執行工作的函式，然後才能定義運算子：

```

CREATE FUNCTION complex_add(complex, complex)
    RETURNS complex
    AS 'filename', 'complex_add'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR + (
    leftarg = complex,
    rightarg = complex,
    function = complex_add,
    commutator = +
);
```

現在我們可以執行像這樣的查詢：

```

SELECT (a + b) AS c FROM test_complex;

        c
-----------------
 (5.2,6.05)
 (133.42,144.95)
```

我們在這裡示範了如何建立一個二元運算子。若要建立前置運算子，只要省略 `leftarg` 即可。`function` 子句與引數子句，是 `CREATE OPERATOR` 中唯二必要的項目。範例中所示範的 `commutator` 子句，則是給查詢最佳化器的選用提示。關於 `commutator` 與其他最佳化器提示的更多細節，將在下一節說明。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xoper.html)（原文版本：18.6；核對日期：2026-09-15）
