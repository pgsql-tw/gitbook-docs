## OPEN

OPEN — 開啟動態游標

## 語法

```

OPEN cursor_name
OPEN cursor_name USING value [, ... ]
OPEN cursor_name USING SQL DESCRIPTOR descriptor_name
```

<a id="id-1.7.5.20.12.3"></a>

## 說明

`OPEN` 開啟游標，並可選擇將實際值繫結至游標宣告中的預留位置。游標必須事先以 `DECLARE` 命令宣告。執行 `OPEN` 會使查詢開始在伺服器上執行。

<a id="id-1.7.5.20.12.4"></a>

## 參數

<a id="ECPG-SQL-OPEN-CURSOR-NAME"></a>

*`cursor_name`* [#](#ECPG-SQL-OPEN-CURSOR-NAME)
:   要開啟的游標名稱。可以是 SQL 識別字或主機變數。
<a id="ECPG-SQL-OPEN-VALUE"></a>

*`value`* [#](#ECPG-SQL-OPEN-VALUE)
:   要繫結至游標預留位置的值。可以是 SQL 常數、主機變數，或含指標的主機變數。
<a id="ECPG-SQL-OPEN-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-OPEN-DESCRIPTOR-NAME)
:   含有要繫結至游標預留位置之值的描述區名稱。可以是 SQL 識別字或主機變數。

<a id="id-1.7.5.20.12.5"></a>

## 範例

```

EXEC SQL OPEN a;
EXEC SQL OPEN d USING 1, 'test';
EXEC SQL OPEN c1 USING SQL DESCRIPTOR mydesc;
EXEC SQL OPEN :curname1;
```

<a id="id-1.7.5.20.12.6"></a>

## 相容性

SQL 標準規定了 `OPEN`。

<a id="id-1.7.5.20.12.7"></a>

## 另請參閱

[DECLARE](ecpg-sql-declare.md), [CLOSE](../../reference/sql-commands/sql-close.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-open.html)（英文原文，待翻譯）
