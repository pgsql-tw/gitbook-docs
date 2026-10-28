<a id="SQL-CREATEDATABASE"></a><a id="id-1.9.3.61.1"></a>

## CREATE DATABASE

CREATE DATABASE — 建立新的資料庫

<a id="id-1.9.3.61.4"></a>

## 語法

```

CREATE DATABASE name
    [ WITH ] [ OWNER [=] user_name ]
           [ TEMPLATE [=] template ]
           [ ENCODING [=] encoding ]
           [ STRATEGY [=] strategy ]
           [ LOCALE [=] locale ]
           [ LC_COLLATE [=] lc_collate ]
           [ LC_CTYPE [=] lc_ctype ]
           [ BUILTIN_LOCALE [=] builtin_locale ]
           [ ICU_LOCALE [=] icu_locale ]
           [ ICU_RULES [=] icu_rules ]
           [ LOCALE_PROVIDER [=] locale_provider ]
           [ COLLATION_VERSION = collation_version ]
           [ TABLESPACE [=] tablespace_name ]
           [ ALLOW_CONNECTIONS [=] allowconn ]
           [ CONNECTION LIMIT [=] connlimit ]
           [ IS_TEMPLATE [=] istemplate ]
           [ OID [=] oid ]
```

<a id="id-1.9.3.61.5"></a>

## 說明

`CREATE DATABASE` 會建立一個新的 PostgreSQL 資料庫。

若要建立資料庫，你必須是超級使用者，或具有特殊的 `CREATEDB` 權限。請參閱 [CREATE ROLE](sql-createrole.md)。

預設情況下，新資料庫會透過複製標準系統資料庫 `template1` 來建立。可以藉由寫出 `TEMPLATE
name` 來指定不同的範本。特別是，寫出 `TEMPLATE template0` 可以建立一個全新的資料庫（其中不存在任何使用者自訂物件，且系統物件未經更動），只包含你所使用的 PostgreSQL 版本預先定義的標準物件。若你希望避免複製任何可能已加入 `template1` 的安裝本地物件，這會很有用。

<a id="id-1.9.3.61.6"></a>

## 參數

<a id="CREATE-DATABASE-NAME"></a>

*`name`* [#](#CREATE-DATABASE-NAME)
:   要建立的資料庫名稱。
<a id="CREATE-DATABASE-USER-NAME"></a>

*`user_name`* [#](#CREATE-DATABASE-USER-NAME)
:   將擁有新資料庫之使用者的角色名稱，或使用 `DEFAULT` 表示採用預設值（也就是執行該命令的使用者）。若要建立由另一個角色擁有的資料庫，你必須能夠 `SET ROLE` 為該角色。
<a id="CREATE-DATABASE-TEMPLATE"></a>

*`template`* [#](#CREATE-DATABASE-TEMPLATE)
:   用來建立新資料庫的範本名稱，或使用 `DEFAULT` 表示採用預設範本（`template1`）。
<a id="CREATE-DATABASE-ENCODING"></a>

*`encoding`* [#](#CREATE-DATABASE-ENCODING)
:   新資料庫所使用的字元集編碼。可指定字串常數（例如 `'SQL_ASCII'`）、整數編碼編號，或使用 `DEFAULT` 表示採用預設編碼（也就是範本資料庫的編碼）。PostgreSQL 伺服器支援的字元集說明請參閱[第 23.3.1 節](../../server-administration/charset/multibyte.md#multibyte-charset-supported)。其他限制請見下文。
<a id="CREATE-DATABASE-STRATEGY"></a>

*`strategy`* [#](#CREATE-DATABASE-STRATEGY)
:   建立新資料庫時所使用的策略。若使用 `WAL_LOG` 策略，資料庫會逐區塊複製，且每個區塊都會分別寫入預寫式日誌。在範本資料庫較小的情況下，這是最有效率的策略，因此它是預設值。也可以使用較舊的 `FILE_COPY` 策略。此策略會針對目標資料庫所使用的每個資料表空間，在預寫式日誌中寫入一筆小型紀錄。每一筆這樣的紀錄，代表在檔案系統層級將整個目錄複製到新位置。雖然這確實能大幅減少預寫式日誌的量（尤其是在範本資料庫很大時），但它也會強制系統在建立新資料庫之前與之後各執行一次檢查點。在某些情況下，這可能會對整體系統效能造成明顯的負面影響。`FILE_COPY` 策略會受到 [file_copy_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-COPY-METHOD) 設定的影響。
<a id="CREATE-DATABASE-LOCALE"></a>

*`locale`* [#](#CREATE-DATABASE-LOCALE)
:   設定新資料庫中的預設定序順序與字元分類。定序會影響套用於字串的排序順序，例如在帶有 `ORDER BY` 的查詢中，以及文字欄位上的索引所使用的順序。字元分類會影響字元的歸類，例如小寫、大寫與數字。此外也會設定作業系統環境中的相關面向，即 `LC_COLLATE` 與 `LC_CTYPE`。預設值與範本資料庫的設定相同。詳情請參閱[第 23.2.2.3.1 節](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-LIBC)與[第 23.2.2.3.2 節](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-ICU)。

    可以藉由個別設定 [*`lc_collate`*](sql-createdatabase.md#CREATE-DATABASE-LC-COLLATE)、[*`lc_ctype`*](sql-createdatabase.md#CREATE-DATABASE-LC-CTYPE)、[*`builtin_locale`*](sql-createdatabase.md#CREATE-DATABASE-BUILTIN-LOCALE) 或 [*`icu_locale`*](sql-createdatabase.md#CREATE-DATABASE-ICU-LOCALE) 來覆寫。

    若 [*`locale_provider`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) 為 `builtin`，則必須指定 *`locale`* 或 *`builtin_locale`*，並將其設為 `C`、`C.UTF-8` 或 `PG_UNICODE_FAST` 其中之一。

    <a id="id-1.9.3.61.6.2.6.2.4"></a>

    ### 提示

    其他的區域設定 [lc_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MESSAGES)、[lc_monetary](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MONETARY)、[lc_numeric](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-NUMERIC) 與 [lc_time](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-TIME) 並非每個資料庫固定，也不會由此命令設定。若你想讓它們成為特定資料庫的預設值，可以使用 `ALTER DATABASE
    ... SET`。
<a id="CREATE-DATABASE-LC-COLLATE"></a>

*`lc_collate`* [#](#CREATE-DATABASE-LC-COLLATE)

設定資料庫伺服器作業系統環境中的 `LC_COLLATE`。若有指定 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE)，預設值為該設定；否則與範本資料庫的設定相同。其他限制請見下文。

若 [*`locale_provider`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) 為 `libc`，此參數也會設定新資料庫中使用的預設定序順序，並覆寫 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE) 設定。
<a id="CREATE-DATABASE-LC-CTYPE"></a>

*`lc_ctype`* [#](#CREATE-DATABASE-LC-CTYPE)

設定資料庫伺服器作業系統環境中的 `LC_CTYPE`。若有指定 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE)，預設值為該設定；否則與範本資料庫的設定相同。其他限制請見下文。

若 [*`locale_provider`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) 為 `libc`，此參數也會設定新資料庫中使用的預設字元分類，並覆寫 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE) 設定。
<a id="CREATE-DATABASE-BUILTIN-LOCALE"></a>

*`builtin_locale`* [#](#CREATE-DATABASE-BUILTIN-LOCALE)

指定內建（builtin）提供者的區域設定，用於資料庫的預設定序順序與字元分類，並覆寫 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE) 設定。[區域設定提供者](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER)必須是 `builtin`。若有指定 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE)，預設值為該設定；否則與範本資料庫的設定相同。

`builtin` 提供者可用的區域設定為 `C`、`C.UTF-8` 與 `PG_UNICODE_FAST`。
<a id="CREATE-DATABASE-ICU-LOCALE"></a>

*`icu_locale`* [#](#CREATE-DATABASE-ICU-LOCALE)
:   指定 ICU 區域設定（請參閱[第 23.2.2.3.2 節](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-ICU)），用於資料庫的預設定序順序與字元分類，並覆寫 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE) 設定。[區域設定提供者](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER)必須是 ICU。若有指定 [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE)，預設值為該設定；否則與範本資料庫的設定相同。
<a id="CREATE-DATABASE-ICU-RULES"></a>

*`icu_rules`* [#](#CREATE-DATABASE-ICU-RULES)
:   指定額外的定序規則，用來自訂此資料庫預設定序的行為。此功能僅支援 ICU。詳情請參閱[第 23.2.3.4 節](../../server-administration/charset/collation.md#ICU-TAILORING-RULES)。
<a id="CREATE-DATABASE-LOCALE-PROVIDER"></a>

*`locale_provider`* [#](#CREATE-DATABASE-LOCALE-PROVIDER)
:   指定此資料庫中預設定序所使用的提供者。可能的值為 `builtin`、`icu`<a id="id-1.9.3.61.6.2.12.2.1.3"></a>（若伺服器建置時加入了 ICU 支援）或 `libc`。預設情況下，提供者與 [*`template`*](sql-createdatabase.md#CREATE-DATABASE-TEMPLATE) 的提供者相同。詳情請參閱[第 23.1.4 節](../../server-administration/charset/locale.md#locale-providers)。
<a id="CREATE-DATABASE-COLLATION-VERSION"></a>

*`collation_version`* [#](#CREATE-DATABASE-COLLATION-VERSION)

指定要與資料庫一起儲存的定序版本字串。通常應該省略此參數，這會使版本由作業系統所提供之資料庫定序的實際版本計算而得。此選項的用途是讓 `pg_upgrade` 從現有安裝中複製版本。

關於如何處理資料庫定序版本不符的問題，另請參閱 [ALTER DATABASE](sql-alterdatabase.md)。
<a id="CREATE-DATABASE-TABLESPACE-NAME"></a>

*`tablespace_name`* [#](#CREATE-DATABASE-TABLESPACE-NAME)
:   將與新資料庫關聯之資料表空間的名稱，或使用 `DEFAULT` 表示採用範本資料庫的資料表空間。此資料表空間將成為在此資料庫中所建立之物件的預設資料表空間。更多資訊請參閱 [CREATE TABLESPACE](sql-createtablespace.md)。
<a id="CREATE-DATABASE-ALLOWCONN"></a>

*`allowconn`* [#](#CREATE-DATABASE-ALLOWCONN)
:   若為 false，則任何人都無法連線到此資料庫。預設值為 true，允許連線（但仍受其他機制限制，例如 `GRANT`/`REVOKE CONNECT`）。
<a id="CREATE-DATABASE-CONNLIMIT"></a>

*`connlimit`* [#](#CREATE-DATABASE-CONNLIMIT)
:   可以對此資料庫建立多少個並行連線。-1（預設值）表示沒有限制。
<a id="CREATE-DATABASE-ISTEMPLATE"></a>

*`istemplate`* [#](#CREATE-DATABASE-ISTEMPLATE)
:   若為 true，則任何具有 `CREATEDB` 權限的使用者都可以複製此資料庫；若為 false（預設值），則只有超級使用者或該資料庫的擁有者可以複製它。
<a id="CREATE-DATABASE-OID"></a>

*`oid`* [#](#CREATE-DATABASE-OID)
:   新資料庫要使用的物件識別碼。若未指定此參數，PostgreSQL 會自動選擇一個合適的 OID。此參數主要供 pg_upgrade 內部使用，而且只有 pg_upgrade 可以指定小於 16384 的值。

選用參數可以依任何順序撰寫，不限於上述所示的順序。

<a id="id-1.9.3.61.7"></a>

## 注意事項

`CREATE DATABASE` 不能在交易區塊內執行。

類似「could not initialize database directory」的錯誤，最可能與資料目錄的權限不足、磁碟已滿或其他檔案系統問題有關。

使用 [`DROP DATABASE`](sql-dropdatabase.md) 來移除資料庫。

程式 [createdb](../reference-client/app-createdb.md) 是包裝此命令的程式，為了方便而提供。

資料庫層級的設定參數（透過 [`ALTER DATABASE`](sql-alterdatabase.md) 設定）與資料庫層級的權限（透過 [`GRANT`](sql-grant.md) 設定）不會從範本資料庫複製過來。

雖然可以藉由將 `template1` 以外的資料庫名稱指定為範本來複製該資料庫，但這（尚）不打算作為通用的「`COPY DATABASE`」功能。主要的限制是，在複製範本資料庫期間，不能有其他工作階段連線到該範本資料庫。若 `CREATE
DATABASE` 開始時存在任何其他連線，它就會失敗；否則，在 `CREATE DATABASE` 完成之前，對範本資料庫的新連線都會被擋在外面。更多資訊請參閱[第 22.3 節](../../server-administration/managing-databases/manage-ag-templatedbs.md)。

為新資料庫指定的字元集編碼，必須與所選的區域設定（`LC_COLLATE` 與 `LC_CTYPE`）相容。若區域設定為 `C`（或等同的 `POSIX`），則允許所有編碼；但對於其他區域設定，只有一種編碼可以正常運作。（不過在 Windows 上，UTF-8 編碼可以與任何區域設定搭配使用。）`CREATE DATABASE` 允許超級使用者不論區域設定為何都指定 `SQL_ASCII` 編碼，但這個選擇已不建議使用，而且若資料庫中儲存了與區域設定編碼不相容的資料，可能會導致字串函式行為異常。

編碼與區域設定必須與範本資料庫的設定相符，除非使用 `template0` 作為範本。這是因為其他資料庫可能包含與指定編碼不符的資料，或可能包含排序順序受 `LC_COLLATE` 與 `LC_CTYPE` 影響的索引。複製這類資料會產生一個依新設定而言已損毀的資料庫。不過，已知 `template0` 不包含任何會受到影響的資料或索引。

目前沒有選項可以使用具有非確定性比較的資料庫區域設定（說明請參閱 [`CREATE
COLLATION`](sql-createcollation.md)）。若有此需要，就必須使用個別欄位的定序。

`CONNECTION LIMIT` 選項只會大約地強制執行；若資料庫只剩下一個連線「槽位」時，有兩個新工作階段大約同時啟動，則兩者都有可能失敗。此外，此限制不會對超級使用者或背景工作程序強制執行。

<a id="id-1.9.3.61.8"></a>

## 範例

建立新的資料庫：

```

CREATE DATABASE lusiadas;
```

建立由使用者 `salesapp` 擁有、預設資料表空間為 `salesspace` 的資料庫 `sales`：

```

CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;
```

建立使用不同區域設定的資料庫 `music`：

```

CREATE DATABASE music
    LOCALE 'sv_SE.utf8'
    TEMPLATE template0;
```

在此範例中，若指定的區域設定與 `template1` 中的不同，則 `TEMPLATE template0` 子句為必要。（若沒有不同，則明確指定區域設定是多餘的。）

建立使用不同區域設定與不同字元集編碼的資料庫 `music2`：

```

CREATE DATABASE music2
    LOCALE 'sv_SE.iso885915'
    ENCODING LATIN9
    TEMPLATE template0;
```

指定的區域設定與編碼設定必須相符，否則會回報錯誤。

請注意，區域設定名稱是作業系統特有的，因此上述命令可能不會在每個地方都以相同方式運作。

<a id="id-1.9.3.61.9"></a>

## 相容性

SQL 標準中沒有 `CREATE DATABASE` 陳述式。資料庫等同於目錄（catalog），而目錄的建立方式由實作自行定義。

<a id="id-1.9.3.61.10"></a>

## 另請參閱

[ALTER DATABASE](sql-alterdatabase.md), [DROP DATABASE](sql-dropdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createdatabase.html)（原文版本：18.6；核對日期：2026-10-04）
