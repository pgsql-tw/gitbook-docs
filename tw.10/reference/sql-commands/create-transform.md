---
description: 版本：10
---

# CREATE TRANSFORM

CREATE TRANSFORM — 定義一個新的轉變

### 語法

```text
CREATE [ OR REPLACE ] TRANSFORM FOR type_name LANGUAGE lang_name (
    FROM SQL WITH FUNCTION from_sql_function_name [ (argument_type [, ...]) ],
    TO SQL WITH FUNCTION to_sql_function_name [ (argument_type [, ...]) ]
);
```

### 說明

CREATE TRANSFORM 定義一個新的轉換。CREATE OR REPLACE TRANSFORM 將建立新的轉換，或替換現有定義。

Transform 指的是如何讓資料型別為程序語言進行轉換。例如，當使用 hstore 型別在 PL/Python 中撰寫函數時，PL/Python 並不具備如何在 Python 環境中呈現 hstore 值的實作方法。語言實作通常預設使用字串型別，但是如果關聯陣列或列表更合適時，這會很不方便的。

轉換指定了兩個函數：

* 「from SQL」函數，用於將型別從 SQL 環境轉換為某個程序語言。將使用該語言撰寫的函數的參數呼叫此函數。
* 「to SQL」函數，用於將型別從某程序語言轉換到 SQL 環境。將使用該語言撰寫的函數呼叫此函數回傳值。

沒有一定要提供這兩種功能。如果未指定，則必要時將使用特定於語言的預設行為。（為了防止某個方向的轉換發生，你也可以寫一個總是出錯的轉換函數。）

為了能夠建立轉換，您必須擁有該型別的 USAGE 權限，擁有該語言的 USAGE 權限，並且擁有對 from-SQL 和 to-SQL 函數的 EXECUTE 權限（如果已指定）。

### Parameters

_`type_name`_

The name of the data type of the transform.

_`lang_name`_

The name of the language of the transform.

_`from_sql_function_name`_\[\(_`argument_type`_ \[, ...\]\)\]

The name of the function for converting the type from the SQL environment to the language. It must take one argument of type `internal` and return type `internal`. The actual argument will be of the type for the transform, and the function should be coded as if it were. \(But it is not allowed to declare an SQL-level function returning `internal` without at least one argument of type `internal`.\) The actual return value will be something specific to the language implementation. If no argument list is specified, the function name must be unique in its schema.

_`to_sql_function_name`_\[\(_`argument_type`_ \[, ...\]\)\]

The name of the function for converting the type from the language to the SQL environment. It must take one argument of type `internal` and return the type that is the type for the transform. The actual argument value will be something specific to the language implementation. If no argument list is specified, the function name must be unique in its schema.

### Notes

Use [DROP TRANSFORM](https://www.postgresql.org/docs/10/static/sql-droptransform.html) to remove transforms.

### Examples

To create a transform for type `hstore` and language `plpythonu`, first set up the type and the language:

```text
CREATE TYPE hstore ...;

CREATE LANGUAGE plpythonu ...;
```

Then create the necessary functions:

```text
CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

And finally create the transform to connect them all together:

```text
CREATE TRANSFORM FOR hstore LANGUAGE plpythonu (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

In practice, these commands would be wrapped up in extensions.

The `contrib` section contains a number of extensions that provide transforms, which can serve as real-world examples.

### Compatibility

This form of `CREATE TRANSFORM` is a PostgreSQL extension. There is a `CREATE TRANSFORM` command in the SQL standard, but it is for adapting data types to client languages. That usage is not supported by PostgreSQL.

### See Also

[CREATE FUNCTION](https://www.postgresql.org/docs/10/static/sql-createfunction.html), [CREATE LANGUAGE](https://www.postgresql.org/docs/10/static/sql-createlanguage.html), [CREATE TYPE](https://www.postgresql.org/docs/10/static/sql-createtype.html), [DROP TRANSFORM](https://www.postgresql.org/docs/10/static/sql-droptransform.html)

