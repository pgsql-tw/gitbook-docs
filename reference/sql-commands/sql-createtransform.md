<a id="SQL-CREATETRANSFORM"></a><a id="id-1.9.3.92.1"></a>

## CREATE TRANSFORM

CREATE TRANSFORM — 定義新的轉換

<a id="id-1.9.3.92.4"></a>

## 語法

```

CREATE [ OR REPLACE ] TRANSFORM FOR type_name LANGUAGE lang_name (
    FROM SQL WITH FUNCTION from_sql_function_name [ (argument_type [, ...]) ],
    TO SQL WITH FUNCTION to_sql_function_name [ (argument_type [, ...]) ]
);
```

<a id="SQL-CREATETRANSFORM-DESCRIPTION"></a>

## 說明

`CREATE TRANSFORM` 會定義新的轉換（transform）。`CREATE OR REPLACE TRANSFORM` 會建立新的轉換，或是取代現有的定義。

轉換指定如何讓某個資料型別適用於某個程序語言。例如，在 PL/Python 中撰寫使用 `hstore` 型別的函式時，PL/Python 事先並不知道該如何在 Python 環境中呈現 `hstore` 值。語言實作通常預設使用文字表示法，但這在某些情況下並不方便，例如使用關聯陣列或串列會更合適的時候。

轉換會指定兩個函式：

* 一個「from SQL」函式，負責將該型別從 SQL 環境轉換到該語言。此函式會在以該語言撰寫之函式的引數上被呼叫。
* 一個「to SQL」函式，負責將該型別從該語言轉換到 SQL 環境。此函式會在以該語言撰寫之函式的傳回值上被呼叫。

不一定要提供這兩個函式。若未指定其中一個，必要時會使用該語言特有的預設行為。（若要完全阻止某個方向的轉換發生，您也可以撰寫一個一律產生錯誤的轉換函式。）

要能夠建立轉換，您必須擁有該型別並具有其 `USAGE` 權限、具有該語言的 `USAGE` 權限，並且擁有 from-SQL 與 to-SQL 函式（若有指定）並具有其 `EXECUTE` 權限。

<a id="id-1.9.3.92.6"></a>

## 參數

*`type_name`*
:   此轉換所針對之資料型別的名稱。

*`lang_name`*
:   此轉換所針對之語言的名稱。

`from_sql_function_name[(argument_type [, ...])]`
:   用於將該型別從 SQL 環境轉換到該語言之函式的名稱。它必須接受一個型別為 `internal` 的引數，並傳回型別 `internal`。實際的引數將是此轉換所針對的型別，而函式應該依此撰寫，彷彿引數就是該型別。（但不允許宣告一個傳回 `internal` 卻沒有至少一個型別為 `internal` 之引數的 SQL 層級函式。）實際的傳回值將是該語言實作特有的內容。若未指定引數列表，則函式名稱在其綱要中必須是唯一的。

`to_sql_function_name[(argument_type [, ...])]`
:   用於將該型別從該語言轉換到 SQL 環境之函式的名稱。它必須接受一個型別為 `internal` 的引數，並傳回此轉換所針對的型別。實際的引數值將是該語言實作特有的內容。若未指定引數列表，則函式名稱在其綱要中必須是唯一的。

<a id="SQL-CREATETRANSFORM-NOTES"></a>

## 注意事項

使用 [`DROP TRANSFORM`](sql-droptransform.md) 移除轉換。

<a id="SQL-CREATETRANSFORM-EXAMPLES"></a>

## 範例

若要為型別 `hstore` 與語言 `plpython3u` 建立轉換，首先設定好該型別與語言：

```

CREATE TYPE hstore ...;

CREATE EXTENSION plpython3u;
```

接著建立必要的函式：

```

CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

最後建立轉換，將它們全部連結在一起：

```

CREATE TRANSFORM FOR hstore LANGUAGE plpython3u (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

實務上，這些命令會被包裝在一個擴充功能中。

`contrib` 部分包含許多提供轉換的擴充功能，可作為實際範例參考。

<a id="SQL-CREATETRANSFORM-COMPAT"></a>

## 相容性

這種形式的 `CREATE TRANSFORM` 是 PostgreSQL 擴充功能。SQL 標準中有一個 `CREATE
TRANSFORM` 命令，但它是用於讓資料型別適用於用戶端語言。PostgreSQL 不支援該用法。

<a id="SQL-CREATETRANSFORM-SEEALSO"></a>

## 另請參閱

[CREATE FUNCTION](sql-createfunction.md),
[CREATE LANGUAGE](sql-createlanguage.md),
[CREATE TYPE](sql-createtype.md),
[DROP TRANSFORM](sql-droptransform.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtransform.html)（原文版本：18.6；核對日期：2026-10-03）
