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

### 參數

_`type_name`_

轉換的資料型別名稱。

_`lang_name`_

轉換程序語言的名稱。

_`from_sql_function_name`_\[\(_`argument_type`_ \[, ...\]\)\]

用於將資料型別從 SQL 環境轉換為程序語言的函數名稱。它必須採用一個資料型別為 internal 且回傳型別為 internal 的參數。實際的參數將是轉換的型別，並且函數應該被撰寫為就像它一樣。（但是，如果沒有至少一個型別為 internal 的參數，則不允許聲明回傳 internal 的 SQL 級函數。）實際回傳值將是特定於語言實作的內容。如果未指定參數列表，則函數名稱在其綱要中必須是唯一的。

_`to_sql_function_name`_\[\(_`argument_type`_ \[, ...\]\)\]

用於將資料型別從程序語言轉換為 SQL 環境的函數名稱。它必須採用型別為 internal 的一個參數，並回傳作為轉換型別的型別。實際參數值將是特定於語言實作的內容。如果未指定參數列表，則函數名稱在其綱要中必須是唯一的。

### 注意

使用 [DROP TRANSFORM](drop-transform.md) 移除轉換。

### 範例

要為型別 hstore 和語言 plpythonu 建立轉換，首先要建立型別和語言：

```text
CREATE TYPE hstore ...;

CREATE LANGUAGE plpythonu ...;
```

然後建立必要的函數：

```text
CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

最後建立轉換將它們連結在一起：

```text
CREATE TRANSFORM FOR hstore LANGUAGE plpythonu (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

實際上，這些指令將被包含在延伸套件中。

contrib 包含許多提供轉換的延伸套件，可以作為真實範例。

### 相容性

這種形式的 CREATE TRANSFORM 是 PostgreSQL 延伸功能。SQL 標準中有一個 CREATE TRANSFORM 指令，但它用於使資料型別適應用戶端語言。 PostgreSQL 不支援這種用法。

### 參閱

[CREATE FUNCTION](create-function.md), [CREATE LANGUAGE](create-language.md), [CREATE TYPE](create-type.md), [DROP TRANSFORM](drop-transform.md)

