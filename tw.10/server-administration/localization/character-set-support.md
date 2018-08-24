---
description: 版本：10
---

# 23.3. 字元集支援

PostgreSQL 中的字元集支援允許您將文字以各種字元集（也稱為編碼）儲存，包括單位元組字元集（如 ISO 8859 系列）和多位元組字元集，如 EUC（延伸 Unix 代碼）， UTF-8 和 Mule 內部代碼。用戶端可以透通地使用所有支援的字元集，但有一些並不支援在伺服器中使用（即作為伺服器端編碼）。使用 initdb 初始化 PostgreSQL 資料庫叢集時，會選擇預設字元集。建立資料庫時可以覆寫它，因此您可以擁有多個資料庫，每個資料庫具有不同的字元集。

但是，一個重要的限制是每個資料庫的字元集必須與資料庫的 LC\_CTYPE（字元分類）和 LC\_COLLATE（字串排序順序）語言環境設定相容。對於 C 或 POSIX 語言環境，允許使用任何字元集，但對於其他 libc 提供的語言環境，只有一個字元集可以正常工作。（但在 Windows 上，UTF-8 編碼可以與任何語言環境一起使用。）如果您配置了 ICU 支援，ICU 提供的語言環境可以與大多數但不是所有伺服器端編碼一起使用。

## 23.3.1. 支援的字元集

[Table 23.1](character-set-support.md#table-23-1-postgresql-character-sets) 顯示了可在 PostgreSQL 中使用的字元集。

#### **Table 23.1. PostgreSQL Character Sets**

| Name | Description | Language | Server? | ICU? | Bytes/Char | Aliases |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BIG5` | Big Five | Traditional Chinese | No | No | 1-2 | `WIN950`, `Windows950` |
| `EUC_CN` | Extended UNIX Code-CN | Simplified Chinese | Yes | Yes | 1-3 |   |
| `EUC_JP` | Extended UNIX Code-JP | Japanese | Yes | Yes | 1-3 |   |
| `EUC_JIS_2004` | Extended UNIX Code-JP, JIS X 0213 | Japanese | Yes | No | 1-3 |   |
| `EUC_KR` | Extended UNIX Code-KR | Korean | Yes | Yes | 1-3 |   |
| `EUC_TW` | Extended UNIX Code-TW | Traditional Chinese, Taiwanese | Yes | Yes | 1-3 |   |
| `GB18030` | National Standard | Chinese | No | No | 1-4 |   |
| `GBK` | Extended National Standard | Simplified Chinese | No | No | 1-2 | `WIN936`, `Windows936` |
| `ISO_8859_5` | ISO 8859-5, ECMA 113 | Latin/Cyrillic | Yes | Yes | 1 |   |
| `ISO_8859_6` | ISO 8859-6, ECMA 114 | Latin/Arabic | Yes | Yes | 1 |   |
| `ISO_8859_7` | ISO 8859-7, ECMA 118 | Latin/Greek | Yes | Yes | 1 |   |
| `ISO_8859_8` | ISO 8859-8, ECMA 121 | Latin/Hebrew | Yes | Yes | 1 |   |
| `JOHAB` | JOHAB | Korean \(Hangul\) | No | No | 1-3 |   |
| `KOI8R` | KOI8-R | Cyrillic \(Russian\) | Yes | Yes | 1 | `KOI8` |
| `KOI8U` | KOI8-U | Cyrillic \(Ukrainian\) | Yes | Yes | 1 |   |
| `LATIN1` | ISO 8859-1, ECMA 94 | Western European | Yes | Yes | 1 | `ISO88591` |
| `LATIN2` | ISO 8859-2, ECMA 94 | Central European | Yes | Yes | 1 | `ISO88592` |
| `LATIN3` | ISO 8859-3, ECMA 94 | South European | Yes | Yes | 1 | `ISO88593` |
| `LATIN4` | ISO 8859-4, ECMA 94 | North European | Yes | Yes | 1 | `ISO88594` |
| `LATIN5` | ISO 8859-9, ECMA 128 | Turkish | Yes | Yes | 1 | `ISO88599` |
| `LATIN6` | ISO 8859-10, ECMA 144 | Nordic | Yes | Yes | 1 | `ISO885910` |
| `LATIN7` | ISO 8859-13 | Baltic | Yes | Yes | 1 | `ISO885913` |
| `LATIN8` | ISO 8859-14 | Celtic | Yes | Yes | 1 | `ISO885914` |
| `LATIN9` | ISO 8859-15 | LATIN1 with Euro and accents | Yes | Yes | 1 | `ISO885915` |
| `LATIN10` | ISO 8859-16, ASRO SR 14111 | Romanian | Yes | No | 1 | `ISO885916` |
| `MULE_INTERNAL` | Mule internal code | Multilingual Emacs | Yes | No | 1-4 |   |
| `SJIS` | Shift JIS | Japanese | No | No | 1-2 | `Mskanji`, `ShiftJIS`, `WIN932`, `Windows932` |
| `SHIFT_JIS_2004` | Shift JIS, JIS X 0213 | Japanese | No | No | 1-2 |   |
| `SQL_ASCII` | unspecified \(see text\) | _any_ | Yes | No | 1 |   |
| `UHC` | Unified Hangul Code | Korean | No | No | 1-2 | `WIN949`, `Windows949` |
| `UTF8` | Unicode, 8-bit | _all_ | Yes | Yes | 1-4 | `Unicode` |
| `WIN866` | Windows CP866 | Cyrillic | Yes | Yes | 1 | `ALT` |
| `WIN874` | Windows CP874 | Thai | Yes | No | 1 |   |
| `WIN1250` | Windows CP1250 | Central European | Yes | Yes | 1 |   |
| `WIN1251` | Windows CP1251 | Cyrillic | Yes | Yes | 1 | `WIN` |
| `WIN1252` | Windows CP1252 | Western European | Yes | Yes | 1 |   |
| `WIN1253` | Windows CP1253 | Greek | Yes | Yes | 1 |   |
| `WIN1254` | Windows CP1254 | Turkish | Yes | Yes | 1 |   |
| `WIN1255` | Windows CP1255 | Hebrew | Yes | Yes | 1 |   |
| `WIN1256` | Windows CP1256 | Arabic | Yes | Yes | 1 |   |
| `WIN1257` | Windows CP1257 | Baltic | Yes | Yes | 1 |   |
| `WIN1258` | Windows CP1258 | Vietnamese | Yes | Yes | 1 | `ABC`, `TCVN`, `TCVN5712`, `VSCII` |

並非所有用戶端 API 都支援所有列出的字元集。例如，PostgreSQL JDBC 驅動程式就不支援 MULE\_INTERNAL，LATIN6，LATIN8 和 LATIN10。

SQL\_ASCII 設定與其他設定的行為大不相同。當伺服器字元集是 SQL\_ASCII 時，伺服器根據 ASCII 標準解譯位元組值 0-127，而位元組值 128-255 作為未解譯的字元。當設定為 SQL\_ASCII 時，不會進行編碼轉換。因此，這個設定並不是使用特定編碼的宣告，而是對編碼的未知宣告。在大多數情況下，如果您使用任何非 ASCII 資料，使用 SQL\_ASCII 設定是不明智的，因為 PostgreSQL 將無法透過轉換或驗證非 ASCII 字元來幫助您。

## 23.3.2. Setting the Character Set

`initdb` defines the default character set \(encoding\) for a PostgreSQL cluster. For example,

```text
initdb -E EUC_JP
```

sets the default character set to `EUC_JP` \(Extended Unix Code for Japanese\). You can use `--encoding` instead of `-E` if you prefer longer option strings. If no `-E` or `--encoding` option is given, `initdb` attempts to determine the appropriate encoding to use based on the specified or default locale.

You can specify a non-default encoding at database creation time, provided that the encoding is compatible with the selected locale:

```text
createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

This will create a database named `korean` that uses the character set `EUC_KR`, and locale `ko_KR`. Another way to accomplish this is to use this SQL command:

```text
CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

Notice that the above commands specify copying the `template0` database. When copying any other database, the encoding and locale settings cannot be changed from those of the source database, because that might result in corrupt data. For more information see [Section 22.3](https://www.postgresql.org/docs/10/static/manage-ag-templatedbs.html).

The encoding for a database is stored in the system catalog `pg_database`. You can see it by using the `psql` `-l` option or the `\l` command.

```text
$ psql -l
                                         List of databases
   Name    |  Owner   | Encoding  |  Collation  |    Ctype    |          Access Privileges          
-----------+----------+-----------+-------------+-------------+-------------------------------------
 clocaledb | hlinnaka | SQL_ASCII | C           | C           | 
 englishdb | hlinnaka | UTF8      | en_GB.UTF8  | en_GB.UTF8  | 
 japanese  | hlinnaka | UTF8      | ja_JP.UTF8  | ja_JP.UTF8  | 
 korean    | hlinnaka | EUC_KR    | ko_KR.euckr | ko_KR.euckr | 
 postgres  | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | 
 template0 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
 template1 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
(7 rows)
```

#### Important

On most modern operating systems, PostgreSQL can determine which character set is implied by the `LC_CTYPE` setting, and it will enforce that only the matching database encoding is used. On older systems it is your responsibility to ensure that you use the encoding expected by the locale you have selected. A mistake in this area is likely to lead to strange behavior of locale-dependent operations such as sorting.

PostgreSQL will allow superusers to create databases with `SQL_ASCII` encoding even when `LC_CTYPE` is not `C` or `POSIX`. As noted above, `SQL_ASCII` does not enforce that the data stored in the database has any particular encoding, and so this choice poses risks of locale-dependent misbehavior. Using this combination of settings is deprecated and may someday be forbidden altogether.

## 23.3.3. Automatic Character Set Conversion Between Server and Client

PostgreSQL supports automatic character set conversion between server and client for certain character set combinations. The conversion information is stored in the `pg_conversion` system catalog. PostgreSQL comes with some predefined conversions, as shown in [Table 23.2](https://www.postgresql.org/docs/10/static/multibyte.html#MULTIBYTE-TRANSLATION-TABLE). You can create a new conversion using the SQL command `CREATE CONVERSION`.

#### **Table 23.2. Client/Server Character Set Conversions**

| Server Character Set | Available Client Character Sets |
| :--- | :--- |
| `BIG5` | _not supported as a server encoding_ |
| `EUC_CN` | _EUC\_CN_, `MULE_INTERNAL`, `UTF8` |
| `EUC_JP` | _EUC\_JP_, `MULE_INTERNAL`, `SJIS`, `UTF8` |
| `EUC_KR` | _EUC\_KR_, `MULE_INTERNAL`, `UTF8` |
| `EUC_TW` | _EUC\_TW_, `BIG5`, `MULE_INTERNAL`, `UTF8` |
| `GB18030` | _not supported as a server encoding_ |
| `GBK` | _not supported as a server encoding_ |
| `ISO_8859_5` | _ISO\_8859\_5_, `KOI8R`, `MULE_INTERNAL`, `UTF8`, `WIN866`, `WIN1251` |
| `ISO_8859_6` | _ISO\_8859\_6_, `UTF8` |
| `ISO_8859_7` | _ISO\_8859\_7_, `UTF8` |
| `ISO_8859_8` | _ISO\_8859\_8_, `UTF8` |
| `JOHAB` | _JOHAB_, `UTF8` |
| `KOI8R` | _KOI8R_, `ISO_8859_5`, `MULE_INTERNAL`, `UTF8`, `WIN866`, `WIN1251` |
| `KOI8U` | _KOI8U_, `UTF8` |
| `LATIN1` | _LATIN1_, `MULE_INTERNAL`, `UTF8` |
| `LATIN2` | _LATIN2_, `MULE_INTERNAL`, `UTF8`, `WIN1250` |
| `LATIN3` | _LATIN3_, `MULE_INTERNAL`, `UTF8` |
| `LATIN4` | _LATIN4_, `MULE_INTERNAL`, `UTF8` |
| `LATIN5` | _LATIN5_, `UTF8` |
| `LATIN6` | _LATIN6_, `UTF8` |
| `LATIN7` | _LATIN7_, `UTF8` |
| `LATIN8` | _LATIN8_, `UTF8` |
| `LATIN9` | _LATIN9_, `UTF8` |
| `LATIN10` | _LATIN10_, `UTF8` |
| `MULE_INTERNAL` | _MULE\_INTERNAL_, `BIG5`, `EUC_CN`, `EUC_JP`, `EUC_KR`, `EUC_TW`, `ISO_8859_5`, `KOI8R`, `LATIN1` to `LATIN4`, `SJIS`, `WIN866`, `WIN1250`, `WIN1251` |
| `SJIS` | _not supported as a server encoding_ |
| `SQL_ASCII` | _any \(no conversion will be performed\)_ |
| `UHC` | _not supported as a server encoding_ |
| `UTF8` | _all supported encodings_ |
| `WIN866` | _WIN866_, `ISO_8859_5`, `KOI8R`, `MULE_INTERNAL`, `UTF8`, `WIN1251` |
| `WIN874` | _WIN874_, `UTF8` |
| `WIN1250` | _WIN1250_, `LATIN2`, `MULE_INTERNAL`, `UTF8` |
| `WIN1251` | _WIN1251_, `ISO_8859_5`, `KOI8R`, `MULE_INTERNAL`, `UTF8`, `WIN866` |
| `WIN1252` | _WIN1252_, `UTF8` |
| `WIN1253` | _WIN1253_, `UTF8` |
| `WIN1254` | _WIN1254_, `UTF8` |
| `WIN1255` | _WIN1255_, `UTF8` |
| `WIN1256` | _WIN1256_, `UTF8` |
| `WIN1257` | _WIN1257_, `UTF8` |
| `WIN1258` | _WIN1258_, `UTF8` |

To enable automatic character set conversion, you have to tell PostgreSQL the character set \(encoding\) you would like to use in the client. There are several ways to accomplish this:

* Using the `\encoding` command in psql. `\encoding` allows you to change client encoding on the fly. For example, to change the encoding to `SJIS`, type:

  ```text
  \encoding SJIS
  ```

* libpq \([Section 33.10](https://www.postgresql.org/docs/10/static/libpq-control.html)\) has functions to control the client encoding.
* Using `SET client_encoding TO`. Setting the client encoding can be done with this SQL command:

  ```text
  SET CLIENT_ENCODING TO 'value';
  ```

  Also you can use the standard SQL syntax `SET NAMES` for this purpose:

  ```text
  SET NAMES 'value';
  ```

  To query the current client encoding:

  ```text
  SHOW client_encoding;
  ```

  To return to the default encoding:

  ```text
  RESET client_encoding;
  ```

* Using `PGCLIENTENCODING`. If the environment variable `PGCLIENTENCODING` is defined in the client's environment, that client encoding is automatically selected when a connection to the server is made. \(This can subsequently be overridden using any of the other methods mentioned above.\)
* Using the configuration variable [client\_encoding](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-CLIENT-ENCODING). If the `client_encoding` variable is set, that client encoding is automatically selected when a connection to the server is made. \(This can subsequently be overridden using any of the other methods mentioned above.\)

If the conversion of a particular character is not possible — suppose you chose `EUC_JP` for the server and `LATIN1` for the client, and some Japanese characters are returned that do not have a representation in `LATIN1` — an error is reported.

If the client character set is defined as `SQL_ASCII`, encoding conversion is disabled, regardless of the server's character set. Just as for the server, use of `SQL_ASCII` is unwise unless you are working with all-ASCII data.

## 23.3.4. 延伸閱讀

這些是開始學習各種編碼系統的好資源。

* CJKV 訊息處理：中文，日文，韓文和越南文運算
  * 包含 EUC\_JP，EUC\_CN，EUC\_KR，EUC\_TW 的詳細說明。
* [http://www.unicode.org/](http://www.unicode.org/)
  * Unicode Consortium 的網站。
* RFC 3629
  * UTF-8 \(8-bit UCS/Unicode Transformation Format\) 定義在這裡

