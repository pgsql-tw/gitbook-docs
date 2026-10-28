<a id="SQL-CREATELANGUAGE"></a><a id="id-1.9.3.70.1"></a>

## CREATE LANGUAGE

CREATE LANGUAGE — 定義新的程序語言

<a id="id-1.9.3.70.4"></a>

## 語法

```

CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
    HANDLER call_handler [ INLINE inline_handler ] [ VALIDATOR valfunction ]
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
```

<a id="SQL-CREATELANGUAGE-DESCRIPTION"></a>

## 說明

`CREATE LANGUAGE` 會向 PostgreSQL 資料庫註冊新的程序語言。之後，就可以用這個新語言定義函式與程序。

`CREATE LANGUAGE` 實際上是將語言名稱與負責執行以該語言撰寫之函式的處理函式關聯起來。關於語言處理常式的更多資訊，請參閱[第 57 章](../../internals/plhandler/README.md)。

`CREATE OR REPLACE LANGUAGE` 會建立新的語言，或取代現有的定義。若該語言已存在，其參數會依命令更新，但該語言的擁有權與權限設定不會改變，且以該語言撰寫的任何現有函式都會被假定仍然有效。

必須具備 PostgreSQL 超級使用者權限，才能註冊新語言或變更現有語言的參數。不過，語言建立之後，可以將其擁有權指派給非超級使用者，該使用者之後便可以移除它、變更其權限、重新命名它，或將它指派給新的擁有者。（不過，不要將底層 C 函式的擁有權指派給非超級使用者；那會為該使用者造成權限提升的途徑。）

未提供任何處理函式的 `CREATE LANGUAGE` 形式已經過時。為了與舊的傾印檔向後相容，它會被解讀為 `CREATE EXTENSION`。若該語言已被封裝成同名的擴充功能，這樣就能運作；這也是設置程序語言的慣用方式。

<a id="SQL-CREATELANGUAGE-PARAMETERS"></a>

## 參數

`TRUSTED`
:   `TRUSTED` 指定該語言不會授予使用者原本沒有的資料存取權。若註冊語言時省略此關鍵字，則只有具備 PostgreSQL 超級使用者權限的使用者，才能使用此語言建立新函式。

`PROCEDURAL`
:   這是一個贅字。

*`name`*
:   新程序語言的名稱。此名稱在資料庫內的語言之間必須是唯一的。

`HANDLER` *`call_handler`*
:   *`call_handler`* 是先前已註冊之函式的名稱，會被呼叫來執行該程序語言的函式。程序語言的呼叫處理常式必須以編譯式語言（例如 C）並使用第 1 版呼叫慣例撰寫，並在 PostgreSQL 中註冊為不接受任何引數、回傳
    `language_handler` 型別的函式；這個佔位型別僅用來將該函式識別為呼叫處理常式。

`INLINE` *`inline_handler`*
:   *`inline_handler`* 是先前已註冊之函式的名稱，會被呼叫來執行此語言中的匿名程式碼區塊（[`DO`](sql-do.md) 命令）。
    若未指定 *`inline_handler`* 函式，該語言就不支援匿名程式碼區塊。
    該處理函式必須接受一個 `internal` 型別的引數，即 `DO` 命令的內部表示形式，且通常會回傳
    `void`。處理函式的回傳值會被忽略。

`VALIDATOR` *`valfunction`*

*`valfunction`* 是先前已註冊之函式的名稱，會在以該語言建立新函式時被呼叫，用以驗證該新函式。
若未指定驗證函式，則新函式在建立時不會受到檢查。
驗證函式必須接受一個 `oid` 型別的引數，即將要建立之函式的 OID，且通常會回傳 `void`。

驗證函式通常會檢查函式主體的語法是否正確，但它也可以檢查函式的其他屬性，例如該語言是否無法處理某些引數型別。要發出錯誤訊號，驗證函式應該使用 `ereport()`
函式。該函式的回傳值會被忽略。

<a id="SQL-CREATELANGUAGE-NOTES"></a>

## 注意事項

使用 [`DROP LANGUAGE`](sql-droplanguage.md) 來移除程序語言。

系統目錄 `pg_language`（請參閱[第 52.29 節](../../internals/catalogs/catalog-pg-language.md)）記錄了目前已安裝之語言的資訊。此外，psql 的
`\dL` 命令會列出已安裝的語言。

要在程序語言中建立函式，使用者必須具備該語言的 `USAGE` 權限。預設情況下，可信任語言的
`USAGE` 權限會授予 `PUBLIC`（亦即所有人）。必要時可以撤銷此權限。

程序語言是各個資料庫專屬的。不過，語言可以安裝到 `template1`
資料庫中，這會使它自動出現在之後建立的所有資料庫中。

<a id="SQL-CREATELANGUAGE-EXAMPLES"></a>

## 範例

建立新程序語言的最精簡步驟如下：

```

CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

這通常會寫在擴充功能的建立腳本中，而使用者會執行下列命令來安裝該擴充功能：

```

CREATE EXTENSION plsample;
```

<a id="SQL-CREATELANGUAGE-COMPAT"></a>

## 相容性

`CREATE LANGUAGE` 是
PostgreSQL 的擴充語法。

<a id="id-1.9.3.70.10"></a>

## 另請參閱

[ALTER LANGUAGE](sql-alterlanguage.md), [CREATE FUNCTION](sql-createfunction.md), [DROP LANGUAGE](sql-droplanguage.md), [GRANT](sql-grant.md), [REVOKE](sql-revoke.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createlanguage.html)（原文版本：18.6；核對日期：2026-10-04）
