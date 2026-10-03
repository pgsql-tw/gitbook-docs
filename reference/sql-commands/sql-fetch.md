<a id="SQL-FETCH"></a><a id="id-1.9.3.149.1"></a><a id="id-1.9.3.149.2"></a>

## FETCH

FETCH — 使用游標從查詢中取回資料列

<a id="id-1.9.3.149.5"></a>

## 語法

```

FETCH [ direction ] [ FROM | IN ] cursor_name

where direction can be one of:

    NEXT
    PRIOR
    FIRST
    LAST
    ABSOLUTE count
    RELATIVE count
    count
    ALL
    FORWARD
    FORWARD count
    FORWARD ALL
    BACKWARD
    BACKWARD count
    BACKWARD ALL
```

<a id="id-1.9.3.149.6"></a>

## 說明

`FETCH` 會使用先前建立的游標取回資料列。

游標有一個相關聯的位置，供 `FETCH` 使用。游標位置可以在查詢結果的第一筆資料列之前、結果中的任何特定資料列上，或結果的最後一筆資料列之後。游標建立時，位於第一筆資料列之前。取回一些資料列之後，游標會位於最近一次取回的資料列上。若 `FETCH` 超出了可用資料列的結尾，游標會停留在最後一筆資料列之後；若是向後取回，則停留在第一筆資料列之前。`FETCH ALL` 或 `FETCH BACKWARD
ALL` 一律會讓游標停留在最後一筆資料列之後或第一筆資料列之前。

`NEXT`、`PRIOR`、`FIRST`、`LAST`、`ABSOLUTE`、`RELATIVE` 這些形式會在適當移動游標之後取回單一資料列。若沒有這樣的資料列，則傳回空結果，且游標會視情況停留在第一筆資料列之前或最後一筆資料列之後。

使用 `FORWARD` 與 `BACKWARD` 的形式會朝向前或向後的方向移動，取回指定數量的資料列，並讓游標停留在最後傳回的資料列上（若 *`count`* 超過可用的資料列數，則停留在所有資料列之後／之前）。

`RELATIVE 0`、`FORWARD 0` 與 `BACKWARD 0` 都是要求在不移動游標的情況下取回目前的資料列，也就是重新取回最近一次取回的資料列。除非游標位於第一筆資料列之前或最後一筆資料列之後，否則這會成功；在那種情況下，不會傳回任何資料列。

### 注意

本頁說明的是在 SQL 命令層級使用游標的方式。若您要在 PL/pgSQL 函式中使用游標，規則有所不同——請參閱[第 41.7.3 節](../../server-programming/plpgsql/plpgsql-cursors.md#PLPGSQL-CURSOR-USING)。

<a id="id-1.9.3.149.7"></a>

## 參數

*`direction`*
:   *`direction`* 定義取回的方向以及要取回的資料列數。它可以是下列其中之一：

    `NEXT`
    :   取回下一筆資料列。若省略 *`direction`*，這是預設值。

    `PRIOR`
    :   取回前一筆資料列。

    `FIRST`
    :   取回查詢的第一筆資料列（與 `ABSOLUTE 1` 相同）。

    `LAST`
    :   取回查詢的最後一筆資料列（與 `ABSOLUTE -1` 相同）。

    `ABSOLUTE count`
    :   取回查詢的第 *`count`* 筆資料列；若 *`count`* 為負數，則取回從結尾算起的第 `abs(count)` 筆資料列。若 *`count`* 超出範圍，則定位在第一筆資料列之前或最後一筆資料列之後；特別是，`ABSOLUTE 0` 會定位在第一筆資料列之前。

    `RELATIVE count`
    :   取回其後的第 *`count`* 筆資料列；若 *`count`* 為負數，則取回其前的第 `abs(count)` 筆資料列。`RELATIVE 0` 會重新取回目前的資料列（若有的話）。

    *`count`*
    :   取回接下來的 *`count`* 筆資料列（與 `FORWARD count` 相同）。

    `ALL`
    :   取回所有剩餘的資料列（與 `FORWARD ALL` 相同）。

    `FORWARD`
    :   取回下一筆資料列（與 `NEXT` 相同）。

    `FORWARD count`
    :   取回接下來的 *`count`* 筆資料列。`FORWARD 0` 會重新取回目前的資料列。

    `FORWARD ALL`
    :   取回所有剩餘的資料列。

    `BACKWARD`
    :   取回前一筆資料列（與 `PRIOR` 相同）。

    `BACKWARD count`
    :   取回之前的 *`count`* 筆資料列（向後掃描）。`BACKWARD 0` 會重新取回目前的資料列。

    `BACKWARD ALL`
    :   取回之前所有的資料列（向後掃描）。

*`count`*
:   *`count`* 是可能帶有正負號的整數常數，用來決定要取回的位置或資料列數。在 `FORWARD` 與 `BACKWARD` 的情況下，指定負的 *`count`* 等同於將 `FORWARD` 與 `BACKWARD` 的方向對調。

*`cursor_name`*
:   已開啟游標的名稱。

<a id="id-1.9.3.149.8"></a>

## 輸出

成功完成時，`FETCH` 命令會傳回下列形式的命令標籤：

```

FETCH count
```

*`count`* 是取回的資料列數（可能為零）。請注意，在 psql 中實際上不會顯示命令標籤，因為 psql 會改為顯示取回的資料列。

<a id="id-1.9.3.149.9"></a>

## 注意事項

若打算使用 `FETCH NEXT` 或搭配正數 count 的 `FETCH FORWARD` 以外的任何 `FETCH` 變體，則應該以 `SCROLL` 選項宣告游標。對於簡單的查詢，PostgreSQL 會允許從未以 `SCROLL` 宣告的游標向後取回，但最好不要依賴這種行為。若游標是以 `NO SCROLL` 宣告，則不允許任何向後取回。

`ABSOLUTE` 取回並不會比以相對移動的方式前往目標資料列更快：底層實作無論如何都必須走訪所有中間的資料列。負數的絕對取回甚至更糟：必須將查詢讀到結尾才能找到最後一筆資料列，然後再從那裡向後走訪。不過，倒回到查詢的開頭（如 `FETCH ABSOLUTE 0`）是很快的。

[`DECLARE`](sql-declare.md) 用來定義游標。使用 [`MOVE`](sql-move.md) 可以在不取回資料的情況下變更游標位置。

<a id="id-1.9.3.149.10"></a>

## 範例

下列範例使用游標走訪資料表：

```

BEGIN WORK;

-- Set up a cursor:
DECLARE liahona SCROLL CURSOR FOR SELECT * FROM films;

-- Fetch the first 5 rows in the cursor liahona:
FETCH FORWARD 5 FROM liahona;

 code  |          title          | did | date_prod  |   kind   |  len
-------+-------------------------+-----+------------+----------+-------
 BL101 | The Third Man           | 101 | 1949-12-23 | Drama    | 01:44
 BL102 | The African Queen       | 101 | 1951-08-11 | Romantic | 01:43
 JL201 | Une Femme est une Femme | 102 | 1961-03-12 | Romantic | 01:25
 P_301 | Vertigo                 | 103 | 1958-11-14 | Action   | 02:08
 P_302 | Becket                  | 103 | 1964-02-03 | Drama    | 02:28

-- Fetch the previous row:
FETCH PRIOR FROM liahona;

 code  |  title  | did | date_prod  |  kind  |  len
-------+---------+-----+------------+--------+-------
 P_301 | Vertigo | 103 | 1958-11-14 | Action | 02:08

-- Close the cursor and end the transaction:
CLOSE liahona;
COMMIT WORK;
```

<a id="id-1.9.3.149.11"></a>

## 相容性

SQL 標準定義的 `FETCH` 僅供嵌入式 SQL 使用。此處所述的 `FETCH` 變體會將資料以如同 `SELECT` 結果的方式傳回，而不是將其放入主變數中。除此之外，`FETCH` 完全向上相容於 SQL 標準。

涉及 `FORWARD` 與 `BACKWARD` 的 `FETCH` 形式，以及隱含 `FORWARD` 的 `FETCH count` 與 `FETCH
ALL` 形式，都是 PostgreSQL 擴充功能。

SQL 標準只允許在游標名稱之前使用 `FROM`；可選擇使用 `IN` 或完全省略它們，則是擴充功能。

<a id="id-1.9.3.149.12"></a>

## 另請參閱

[CLOSE](sql-close.md), [DECLARE](sql-declare.md), [MOVE](sql-move.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-fetch.html)（原文版本：18.6；核對日期：2026-10-03）
