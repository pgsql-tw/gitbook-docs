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

## 23.3.2. 設定字元集

initdb 定義 PostgreSQL 叢集的預設字元集（編碼）。例如，

```text
initdb -E EUC_JP
```

將預設字元集設定為 EUC\_JP（日本語的延伸 Unix 代碼）。如果您喜歡更長的選項字串，則可以使用 --encoding 而不是 -E。如果使用 -E 或 --encoding 選項，initdb 將嘗試根據指定的或預設的語言環境決定要使用的相對應編碼。

您可以在資料庫建立時指定非預設編碼，前提是該編碼與所選語言環境相容：

```text
createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

這將建立一個名為 korean 的資料庫，該資料庫使用字元集 EUC\_KR 和語言環境 ko\_KR。另一種方法是使用此 SQL 指令：

```text
CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

請注意，上述指令指定複製 template0 資料庫。複製任何其他資料庫時，無法更改原資料庫的編碼和語言環境設定，因為這可能會導致資料損壞。有關更多訊息，請參閱[第 22.3 節](../managing-databases/template-databases.md)。

資料庫的編碼儲存在系統目錄 pg\_database 中。您可以使用 psql -l 選項或 \l 指令查看。

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

**注意**  
在大多數現代作業系統上，PostgreSQL 可以確定 LC\_CTYPE 設定所隱含的字元集，並強制只使用相符合的資料庫編碼。在較舊的系統上，您有責任確保使用所選區域設定所需的編碼。此區域中的錯誤可能會導致與區域設定相關操作（如排序）的奇怪行為。

即使 LC\_CTYPE 不是 C 或 POSIX，PostgreSQL 也允許超級使用者使用 SQL\_ASCII 編碼建立資料庫。如上所述，SQL\_ASCII 不強制儲存在資料庫中的資料具有任何特定編碼，因此這種選擇會帶來相依於語言環境的錯誤行為風險。不推薦使用這種設定組合，有一天可能會被禁止使用。

## 23.3.3. 伺服器和用戶端之間的自動字元集轉換

PostgreSQL 支援伺服器和用戶端之間針對某些字元集組合的自動字元集轉換。轉換訊息儲存在 pg\_conversion 系統目錄中。PostgreSQL 帶有一些預先定義的轉換，如 [Table 23.2](character-set-support.md#table-23-2-client-server-character-set-conversions) 所示。您可以使用 SQL 指令 CREATE CONVERSION 建立新的轉換。

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

要啟用自動字元集轉換，您必須告訴 PostgreSQL 您要在用戶端中使用的字元集（編碼）。有幾種方法可以實現此目的：

* 在 psql 中使用 \encoding 指令。\encoding 允許您即時更改用戶端編碼。例如，要將編碼更改為 SJIS，請鍵入：

  ```text
  \encoding SJIS
  ```

* libpq（[第 33.10 節](../../client-interfaces/libpq-c-library/control-functions.md)）具有控制用戶端編碼的功能。
* 使用 SET client\_encoding TO。可以使用以下 SQL 指令設定用戶端編碼：

  ```text
  SET CLIENT_ENCODING TO 'value';
  ```

  您還可以使用標準 SQL 語法 SET NAMES 來達到此目的：

  ```text
  SET NAMES 'value';
  ```

  要查詢目前用戶端編碼：

  ```text
  SHOW client_encoding;
  ```

  要回傳預設編碼：

  ```text
  RESET client_encoding;
  ```

* 使用 PGCLIENTENCODING。如果在用戶端環境中定義了環境變數 PGCLIENTENCODING，則在建立與伺服器的連線時會自動選擇該用戶端編碼。（這可以隨後使用上面提到的任何其他方法覆蓋。）
* 使用組態變數 client\_encoding。如果設定了 [client\_encoding](../server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#client_encoding-string) 變數，則在建立與伺服器的連線時會自動選擇該用戶端編碼。（這可以隨後使用上面提到的任何其他方法覆蓋。）

如果無法轉換特定字元 - 假設您為伺服器選擇了 EUC\_JP 而為用戶端選擇了 LATIN1，並且回傳了一些在 LATIN1 中沒有表示的日文字元 - 回報錯誤。

如果用戶端字元集定義為 SQL\_ASCII，則無論伺服器的字元集如何，都將停用編碼轉換。就像伺服器一樣，除非使用全 ASCII 資料，否則使用 SQL\_ASCII 是不明智的。

## 23.3.4. 延伸閱讀

這些是開始學習各種編碼系統的好資源。

* CJKV 訊息處理：中文，日文，韓文和越南文運算
  * 包含 EUC\_JP，EUC\_CN，EUC\_KR，EUC\_TW 的詳細說明。
* [http://www.unicode.org/](http://www.unicode.org/)
  * Unicode Consortium 的網站。
* RFC 3629
  * UTF-8 \(8-bit UCS/Unicode Transformation Format\) 定義在這裡

