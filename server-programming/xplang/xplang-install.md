<a id="XPLANG-INSTALL"></a>

## 40.1. 安裝程序語言 [#](#XPLANG-INSTALL)

程序語言必須「安裝」到每一個要使用它的資料庫中。不過，安裝在 `template1` 資料庫中的程序語言會自動在之後建立的所有資料庫中可用，因為它們在 `template1` 中的項目會被 `CREATE DATABASE` 複製過去。因此資料庫管理者可以決定哪些語言在哪些資料庫中可用，也可以視需要讓某些語言預設就可用。

對於標準發行版所提供的語言，只要執行 `CREATE EXTENSION` *`language_name`* 就能把該語言安裝到目前的資料庫中。下面說明的手動程序，只建議用來安裝尚未被封裝成擴充套件的語言。

<a id="id-1.8.7.5.4"></a>

**手動安裝程序語言**

安裝程序語言到資料庫中共有五個步驟，而且必須由資料庫超級使用者執行。在大多數情況下，所需的 SQL 指令應該封裝成「擴充套件」的安裝腳本，如此便可以用 `CREATE EXTENSION` 來執行它們。

<a id="XPLANG-INSTALL-CR1"></a>1. 語言處理常式的共用物件必須先編譯好，並安裝到適當的程式庫目錄中。這與建置並安裝含有一般使用者定義 C 函式的模組的方式相同；請參閱[第 36.10.5 節](../extend/xfunc-c.md#DFUNC)。語言處理常式通常會相依於某個提供實際程式語言引擎的外部程式庫；若是如此，那個程式庫也必須一併安裝。
<a id="XPLANG-INSTALL-CR2"></a>2. 必須用以下指令宣告該處理常式

   ```

   CREATE FUNCTION handler_function_name()
       RETURNS language_handler
       AS 'path-to-shared-object'
       LANGUAGE C;
   ```

   `language_handler` 這個特殊的回傳型別會告訴資料庫系統，此函式並不回傳任何一種已定義的 SQL 資料型別，也不能直接用在 SQL 陳述式中。
<a id="XPLANG-INSTALL-CR3"></a>3. 語言處理常式可以選擇性地提供一個「行內」處理常式函式，用來執行以該語言撰寫的匿名程式碼區塊（[`DO`](../../reference/sql-commands/sql-do.md) 指令）。如果該語言有提供行內處理常式函式，請用類似以下的指令宣告它

   ```

   CREATE FUNCTION inline_function_name(internal)
       RETURNS void
       AS 'path-to-shared-object'
       LANGUAGE C;
   ```
<a id="XPLANG-INSTALL-CR4"></a>4. 語言處理常式也可以選擇性地提供一個「驗證器」函式，在不實際執行函式定義的情況下檢查其正確性。若驗證器函式存在，`CREATE FUNCTION` 會呼叫它。如果該語言有提供驗證器函式，請用類似以下的指令宣告它

   ```

   CREATE FUNCTION validator_function_name(oid)
       RETURNS void
       AS 'path-to-shared-object'
       LANGUAGE C STRICT;
   ```
<a id="XPLANG-INSTALL-CR5"></a>5. 最後，必須用以下指令宣告該 PL

   ```

   CREATE [TRUSTED] LANGUAGE language_name
       HANDLER handler_function_name
       [INLINE inline_function_name]
       [VALIDATOR validator_function_name] ;
   ```

   選用的關鍵字 `TRUSTED` 表示該語言不會授予使用者原本無法取得的資料存取權。受信任的語言是為一般資料庫使用者（沒有超級使用者權限的使用者）設計的，讓他們能夠安全地建立函式與程序。由於 PL 函式是在資料庫伺服器內部執行的，`TRUSTED` 旗標只應該給予那些不允許存取資料庫伺服器內部或檔案系統的語言。PL/pgSQL、PL/Tcl 與 PL/Perl 這些語言被視為受信任的；而 PL/TclU、PL/PerlU 與 PL/PythonU 這些語言則是設計來提供不受限制的功能，因此*不*應該被標記為受信任。

[範例 40.1](xplang-install.md#XPLANG-INSTALL-EXAMPLE) 示範了手動安裝程序如何套用在 PL/Perl 語言上。

<a id="XPLANG-INSTALL-EXAMPLE"></a>

**範例 40.1. 手動安裝 PL/Perl**

以下指令告訴資料庫伺服器到哪裡去找 PL/Perl 語言之呼叫處理常式函式的共用物件：

```

CREATE FUNCTION plperl_call_handler() RETURNS language_handler AS
    '$libdir/plperl' LANGUAGE C;
```

PL/Perl 有行內處理常式函式與驗證器函式，因此我們也一併宣告它們：

```

CREATE FUNCTION plperl_inline_handler(internal) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;

CREATE FUNCTION plperl_validator(oid) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;
```

接著這個指令：

```

CREATE TRUSTED LANGUAGE plperl
    HANDLER plperl_call_handler
    INLINE plperl_inline_handler
    VALIDATOR plperl_validator;
```

定義了對於語言屬性為 `plperl` 的函式與程序，應呼叫先前所宣告的那些函式。

<br>

在預設的 PostgreSQL 安裝中，PL/pgSQL 語言的處理常式會被建置並安裝到「程式庫」目錄中；此外，PL/pgSQL 語言本身也會安裝到所有資料庫中。如果設定時納入了 Tcl 支援，PL/Tcl 與 PL/TclU 的處理常式會被建置並安裝到程式庫目錄中，但該語言本身預設不會安裝到任何資料庫。同樣地，若設定時納入了 Perl 支援，PL/Perl 與 PL/PerlU 的處理常式會被建置並安裝；若設定時納入了 Python 支援，PL/PythonU 的處理常式也會被安裝，但這些語言預設都不會被安裝。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xplang-install.html)（原文版本：18.6；核對日期：2026-09-13）
