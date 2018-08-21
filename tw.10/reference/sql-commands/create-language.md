---
description: 版本：10
---

# CREATE LANGUAGE

CREATE LANGUAGE — 宣告一種新的程序語言

### 語法

```text
CREATE [ OR REPLACE ] [ PROCEDURAL ] LANGUAGE name
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
    HANDLER call_handler [ INLINE inline_handler ] [ VALIDATOR valfunction ]
```

### 說明

CREATE LANGUAGE 使用 PostgreSQL 資料庫註冊新的程序語言。隨後即可使用這種新語言定義函數和觸發器程序。

**注意**  
從 PostgreSQL 9.1 開始，大多數程序語言都被製作成「extension」，因此應該使用 [CREATE EXTENSION](create-extension.md) 而不是 CREATE LANGUAGE 安裝。現在應該直接使用 CREATE LANGUAGE 來限制性的延伸套件安裝腳本。如果資料庫中存在有純粹的程序語言（可能是升級後的結果），則可以使用 CREATE EXTENSION langname FROM unpackaged 將其轉換為延伸套件。

CREATE LANGUAGE 有效地將語言名稱與負責執行用該語言撰寫的函數與語言處理函數相關聯。有關語言處理程序的更多訊息，請參閱[第 55 章](../../internals/writing-a-procedural-language-handler.md)。

CREATE LANGUAGE 指令有兩種形式。在第一種形式中，使用者只提供所需語言的名稱，PostgreSQL 伺服器查詢 pg\_pltemplatesystem 目錄以確定正確的參數。在第二種形式中，使用者提供語言參數以及語言名稱。第二種形式可用於建立未在 pg\_pltemplate 中定義的語言，但此方法被視為是過時的。

當伺服器在 pg\_pltemplate 目錄中找到指定的語言名稱項目時，即使該命令包含語言參數，它也將使用目錄的資訊。此行為簡化了舊的備份檔案載入，這些備份檔案可能包含有關語言支援功能但過時的訊息。

通常，使用者必須具有 PostgreSQL 超級使用者權限才能註冊新的語言。但是，如果語言在 pg\_pltemplate 目錄中列出並且標記為允許由資料庫擁有者建立（tmpldbacreate 為 true），則資料庫的擁有者可以在該資料庫中註冊新的語言。預設情況下，資料庫擁有者可以建立受信任的語言，但超級使用者可以透過修改 pg\_pltemplate 的內容來調整它。語言的建立者成為其擁有者，以後可以將其移除，重新命名或將其分配給新的擁有者。

CREATE OR REPLACE LANGUAGE 將註冊新的語言或更換現有的定義。如果該語言已存在，則其參數將根據指定的值或從 pg\_pltemplate 取得，但語言的擁有權和權限設定不會更改，並且假定使用該語言撰寫的任何現有函數仍然有效。除了建立語言的普通權限要求之外，使用者還必須是現有語言的擁有者或超級使用者。REPLACE 主要用於確保語言存在。如果該語言具有 pg\_pltemplate 項目，則 REPLACE 實際上不會變更現有定義的任何內容，除非在建立語言後修改了 pg\_pltemplate 項目的特殊情況。

### Parameters

`TRUSTED`

`TRUSTED` specifies that the language does not grant access to data that the user would not otherwise have. If this key word is omitted when registering the language, only users with the PostgreSQL superuser privilege can use this language to create new functions.

`PROCEDURAL`

This is a noise word.

_`name`_

The name of the new procedural language. The name must be unique among the languages in the database.

For backward compatibility, the name can be enclosed by single quotes.

`HANDLER` _`call_handler`_

_`call_handler`_ is the name of a previously registered function that will be called to execute the procedural language's functions. The call handler for a procedural language must be written in a compiled language such as C with version 1 call convention and registered with PostgreSQL as a function taking no arguments and returning the `language_handler`type, a placeholder type that is simply used to identify the function as a call handler.

`INLINE` _`inline_handler`_

_`inline_handler`_ is the name of a previously registered function that will be called to execute an anonymous code block \([DO](https://www.postgresql.org/docs/10/static/sql-do.html) command\) in this language. If no _`inline_handler`_function is specified, the language does not support anonymous code blocks. The handler function must take one argument of type `internal`, which will be the `DO` command's internal representation, and it will typically return `void`. The return value of the handler is ignored.

`VALIDATOR` _`valfunction`_

_`valfunction`_ is the name of a previously registered function that will be called when a new function in the language is created, to validate the new function. If no validator function is specified, then a new function will not be checked when it is created. The validator function must take one argument of type `oid`, which will be the OID of the to-be-created function, and will typically return `void`.

A validator function would typically inspect the function body for syntactical correctness, but it can also look at other properties of the function, for example if the language cannot handle certain argument types. To signal an error, the validator function should use the `ereport()` function. The return value of the function is ignored.

The `TRUSTED` option and the support function name\(s\) are ignored if the server has an entry for the specified language name in `pg_pltemplate`.

### Notes

Use [DROP LANGUAGE](https://www.postgresql.org/docs/10/static/sql-droplanguage.html) to drop procedural languages.

The system catalog `pg_language` \(see [Section 51.29](https://www.postgresql.org/docs/10/static/catalog-pg-language.html)\) records information about the currently installed languages. Also, the psql command `\dL` lists the installed languages.

To create functions in a procedural language, a user must have the `USAGE` privilege for the language. By default, `USAGE` is granted to `PUBLIC` \(i.e., everyone\) for trusted languages. This can be revoked if desired.

Procedural languages are local to individual databases. However, a language can be installed into the `template1` database, which will cause it to be available automatically in all subsequently-created databases.

The call handler function, the inline handler function \(if any\), and the validator function \(if any\) must already exist if the server does not have an entry for the language in `pg_pltemplate`. But when there is an entry, the functions need not already exist; they will be automatically defined if not present in the database. \(This might result in `CREATE LANGUAGE`failing, if the shared library that implements the language is not available in the installation.\)

In PostgreSQL versions before 7.3, it was necessary to declare handler functions as returning the placeholder type `opaque`, rather than `language_handler`. To support loading of old dump files, `CREATE LANGUAGE` will accept a function declared as returning `opaque`, but it will issue a notice and change the function's declared return type to `language_handler`.

### 範例

建立任何標準程序語言的最好方式是：

```text
CREATE LANGUAGE plperl;
```

對於 pg\_pltemplate 目錄中未知的語言，需要這樣的指令程序：

```text
CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

### 相容性

CREATE LANGUAGE 是 PostgreSQL 的延伸功能。

### 參閱

[ALTER LANGUAGE](alter-language.md), [CREATE FUNCTION](create-function.md), [DROP LANGUAGE](drop-language.md), [GRANT](grant.md), [REVOKE](revoke.md)

