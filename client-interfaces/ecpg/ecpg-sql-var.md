## VAR

VAR — 定義變數

## 語法

```

VAR varname IS ctype
```

<a id="id-1.7.5.20.18.3"></a>

## 說明

`VAR` 命令會將新的 C 資料型別指派給主機變數。主機變數必須事先在宣告區段中宣告。

<a id="id-1.7.5.20.18.4"></a>

## 參數

<a id="ECPG-SQL-VAR-VARNAME"></a>

*`varname`* [#](#ECPG-SQL-VAR-VARNAME)
:   C 變數名稱。
<a id="ECPG-SQL-VAR-CTYPE"></a>

*`ctype`* [#](#ECPG-SQL-VAR-CTYPE)
:   C 型別規格。

<a id="id-1.7.5.20.18.5"></a>

## 範例

```

Exec sql begin declare section;
short a;
exec sql end declare section;
EXEC SQL VAR a IS int;
```

<a id="id-1.7.5.20.18.6"></a>

## 相容性

`VAR` 命令是 PostgreSQL 擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-var.html)（英文原文，待翻譯）
