<a id="id-1.9.3.157.1"></a><a id="id-1.9.3.157.2"></a>

## MOVE

MOVE — 定位游標

## 語法

```

MOVE [ direction ] [ FROM | IN ] cursor_name

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

<a id="id-1.9.3.157.6"></a>

## 說明

`MOVE` 會重新定位游標，但不會取回任何資料。`MOVE` 的運作方式與 `FETCH` 指令完全相同，差別只在於它僅定位游標，不會傳回資料列。

`MOVE` 指令的參數與 `FETCH` 指令完全相同；語法與用法的詳情請參閱 [FETCH](sql-fetch.md)。

<a id="id-1.9.3.157.7"></a>

## 輸出

成功完成後，`MOVE` 指令會傳回下列形式的指令標記：

```

MOVE count
```

*`count`* 是若以相同參數執行 `FETCH` 指令時，原本會傳回的資料列數（可能為零）。

<a id="id-1.9.3.157.8"></a>

## 範例

```

BEGIN WORK;
DECLARE liahona CURSOR FOR SELECT * FROM films;

-- Skip the first 5 rows:
MOVE FORWARD 5 IN liahona;
MOVE 5

-- Fetch the 6th row from the cursor liahona:
FETCH 1 FROM liahona;
 code  | title  | did | date_prod  |  kind  |  len
-------+--------+-----+------------+--------+-------
 P_303 | 48 Hrs | 103 | 1982-10-22 | Action | 01:37
(1 row)

-- Close the cursor liahona and end the transaction:
CLOSE liahona;
COMMIT WORK;
```

<a id="id-1.9.3.157.9"></a>

## 相容性

SQL 標準中沒有 `MOVE` 陳述式。

<a id="id-1.9.3.157.10"></a>

## 另請參閱

[CLOSE](sql-close.md), [DECLARE](sql-declare.md), [FETCH](sql-fetch.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-move.html)（原文版本：18.6；核對日期：2026-09-28）
