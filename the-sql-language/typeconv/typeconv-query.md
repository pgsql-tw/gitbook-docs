<a id="TYPECONV-QUERY"></a>

## 10.4. 值的儲存 [#](#TYPECONV-QUERY)

要插入資料表的值，會依下列步驟轉換為目標欄位的資料型別。

<a id="id-1.5.9.9.3"></a>

**值儲存的型別轉換**

1. 檢查是否與目標完全相符。
2. 否則，嘗試將運算式轉換為目標型別。如果 `pg_cast` 系統目錄中登記了這兩個型別之間的*指派轉換*（assignment cast），就可以進行轉換（請參閱 [CREATE CAST](../../reference/sql-commands/sql-createcast.md)）。另外，如果運算式是型別未知的字面值，則會將該字面值字串的內容交給目標型別的輸入轉換程序處理。
3. 檢查目標型別是否有大小調整轉換（sizing cast）。大小調整轉換是從該型別轉換為自身的型別轉換。如果在 `pg_cast` 系統目錄中找到，就會在存入目標欄位之前，將它套用到運算式上。這類型別轉換的實作函式一定會多接收一個 `integer` 型別的參數，用來接收目標欄位的 `atttypmod` 值（通常是宣告的長度，不過 `atttypmod` 的解讀方式因資料型別而異），也可能接收第三個 `boolean` 參數，表示這次轉換是明確轉換還是隱含轉換。轉換函式負責套用任何與長度相關的語意，例如檢查大小或截斷。

<a id="id-1.5.9.9.4"></a>

**範例 10.9. `character` 儲存的型別轉換**

對於宣告為 `character(20)` 的目標欄位，下列陳述式顯示儲存的值會被調整成正確的大小：

```

CREATE TABLE vv (v character(20));
INSERT INTO vv SELECT 'abc' || 'def';
SELECT v, octet_length(v) FROM vv;

          v           | octet_length
----------------------+--------------
 abcdef               |           20
(1 row)
```

這裡實際發生的事情是：兩個未知型別的字面值預設會被解析為 `text`，使得 `||` 運算子可以解析為 `text` 串接。接著，運算子的 `text` 結果會被轉換為 `bpchar`（「blank-padded char」，即 `character` 資料型別的內部名稱），以符合目標欄位的型別。（由於從 `text` 轉換為 `bpchar` 是二進位相容的，這項轉換並不會插入任何實際的函式呼叫。）最後，系統會在系統目錄中找到大小調整函式 `bpchar(bpchar, integer, boolean)`，並將它套用到運算子的結果與所儲存的欄位長度上。這個特定於型別的函式會執行必要的長度檢查，並補上填充空白。

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/typeconv-query.html)（原文版本：18.6；核對日期：2026-09-11）
