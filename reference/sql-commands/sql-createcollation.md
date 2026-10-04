<a id="SQL-CREATECOLLATION"></a><a id="id-1.9.3.59.1"></a>

## CREATE COLLATION

CREATE COLLATION — 定義新的定序

<a id="id-1.9.3.59.4"></a>

## 語法

```

CREATE COLLATION [ IF NOT EXISTS ] name (
    [ LOCALE = locale, ]
    [ LC_COLLATE = lc_collate, ]
    [ LC_CTYPE = lc_ctype, ]
    [ PROVIDER = provider, ]
    [ DETERMINISTIC = boolean, ]
    [ RULES = rules, ]
    [ VERSION = version ]
)
CREATE COLLATION [ IF NOT EXISTS ] name FROM existing_collation
```

<a id="SQL-CREATECOLLATION-DESCRIPTION"></a>

## 說明

`CREATE COLLATION` 會使用指定的作業系統區域設定，或藉由複製現有的定序，來定義新的定序。

要建立定序，你必須在目標綱要上具有 `CREATE` 權限。

<a id="id-1.9.3.59.6"></a>

## 參數

`IF NOT EXISTS`
:   若已存在同名的定序，不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的定序與原本會建立的定序有任何相似之處。

*`name`*
:   定序的名稱。定序名稱可以用綱要限定；若未限定，定序會定義在目前的綱要中。定序名稱在該綱要中必須是唯一的。（系統目錄可以包含適用於其他編碼的同名定序，但若資料庫編碼不相符，這些定序會被忽略。）

*`locale`*
:   此定序的區域名稱。詳情請參閱[第 23.2.2.3.1 節](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-LIBC)與[第 23.2.2.3.2 節](../../server-administration/charset/collation.md#COLLATION-MANAGING-CREATE-ICU)。

    若 *`provider`* 為 `libc`，這是一次同時設定 `LC_COLLATE` 與 `LC_CTYPE` 的簡寫。若你指定了 *`locale`*，就不能再指定這兩個參數中的任何一個。

    若 *`provider`* 為 `builtin`，則必須指定 *`locale`*，且必須設為 `C`、`C.UTF-8` 或 `PG_UNICODE_FAST` 其中之一。

*`lc_collate`*
:   若 *`provider`* 為 `libc`，則對 `LC_COLLATE` 區域類別使用指定的作業系統區域設定。

*`lc_ctype`*
:   若 *`provider`* 為 `libc`，則對 `LC_CTYPE` 區域類別使用指定的作業系統區域設定。

*`provider`*
:   指定與此定序相關之區域服務所使用的提供者。可能的值為 `builtin`、`icu`<a id="id-1.9.3.59.6.2.6.2.1.3"></a>（若伺服器建置時有 ICU 支援）或 `libc`。`libc` 是預設值。詳情請參閱[第 23.1.4 節](../../server-administration/charset/locale.md#LOCALE-PROVIDERS)。

`DETERMINISTIC`
:   指定定序是否應使用確定性比較。預設為 true。確定性比較會將位元組不相等的字串視為不相等，即使比較認為它們在邏輯上相等也是如此。PostgreSQL 會使用逐位元組比較來決定平手的情況。非確定性的比較可以使定序成為例如不區分大小寫或不區分重音符號的定序。為此，你需要選擇適當的 `LOCALE` 設定，*並且*在此將定序設為非確定性。

    只有 ICU 提供者支援非確定性定序。

*`rules`*
:   指定額外的定序規則，以自訂定序的行為。只有 ICU 支援此功能。詳情請參閱[第 23.2.3.4 節](../../server-administration/charset/collation.md#ICU-TAILORING-RULES)。

*`version`*
:   指定要與定序一併儲存的版本字串。通常應該省略此項，這會使版本根據作業系統所提供之定序的實際版本計算而得。此選項的用途是讓 `pg_upgrade` 從現有的安裝中複製版本。

    另請參閱 [ALTER COLLATION](sql-altercollation.md)，了解如何處理定序版本不相符的情況。

*`existing_collation`*
:   要複製的現有定序名稱。新的定序會具有與現有定序相同的屬性，但它會是一個獨立的物件。

<a id="SQL-CREATECOLLATION-NOTES"></a>

## 注意事項

`CREATE COLLATION` 會在 `pg_collation` 系統目錄上取得 `SHARE ROW
EXCLUSIVE` 鎖定，此鎖定會與自身衝突，因此一次只能執行一個 `CREATE COLLATION` 命令。

使用 `DROP COLLATION` 移除使用者定義的定序。

關於如何建立定序的更多資訊，請參閱[第 23.2.2.3 節](../../server-administration/charset/collation.md#COLLATION-CREATE)。

使用 `libc` 定序提供者時，區域設定必須適用於目前的資料庫編碼。確切的規則請參閱 [CREATE DATABASE](sql-createdatabase.md)。

<a id="SQL-CREATECOLLATION-EXAMPLES"></a>

## 範例

從作業系統區域設定 `fr_FR.utf8` 建立定序（假設目前的資料庫編碼為 `UTF8`）：

```

CREATE COLLATION french (locale = 'fr_FR.utf8');
```

使用 ICU 提供者，以德文電話簿排序順序建立定序：

```

CREATE COLLATION german_phonebook (provider = icu, locale = 'de-u-co-phonebk');
```

使用 ICU 提供者，以 ICU 根區域設定為基礎，並搭配自訂規則建立定序：

```

CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

關於規則語法的更多細節與範例，請參閱[第 23.2.3.4 節](../../server-administration/charset/collation.md#ICU-TAILORING-RULES)。

從現有的定序建立定序：

```

CREATE COLLATION german FROM "de_DE";
```

這樣可以方便在應用程式中使用與作業系統無關的定序名稱。

<a id="SQL-CREATECOLLATION-COMPAT"></a>

## 相容性

SQL 標準中有 `CREATE COLLATION` 陳述式，但它僅限於複製現有的定序。建立新定序的語法是 PostgreSQL 的擴充語法。

<a id="SQL-CREATECOLLATION-SEEALSO"></a>

## 另請參閱

[ALTER COLLATION](sql-altercollation.md), [DROP COLLATION](sql-dropcollation.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createcollation.html)（原文版本：18.6；核對日期：2026-10-04）
