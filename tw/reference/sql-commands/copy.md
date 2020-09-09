---
description: 版本：11
---

# COPY

COPY — 在檔案和資料表之間複製資料

## 語法

```text
COPY table_name [ ( column_name [, ...] ) ]
    FROM { 'filename' | PROGRAM 'command' | STDIN }
    [ [ WITH ] ( option [, ...] ) ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) }
    TO { 'filename' | PROGRAM 'command' | STDOUT }
    [ [ WITH ] ( option [, ...] ) ]

where option can be one of:

    FORMAT format_name
    OIDS [ boolean ]
    FREEZE [ boolean ]
    DELIMITER 'delimiter_character'
    NULL 'null_string'
    HEADER [ boolean ]
    QUOTE 'quote_character'
    ESCAPE 'escape_character'
    FORCE_QUOTE { ( column_name [, ...] ) | * }
    FORCE_NOT_NULL ( column_name [, ...] )
    FORCE_NULL ( column_name [, ...] )
    ENCODING 'encoding_name'
```

## 說明

COPY 在 PostgreSQL 資料表和標準檔案系統的檔案之間移動資料。COPY TO 將資料表的內容複製到檔案，而 COPY FROM 將資料從檔案複製到資料表（將資料附加到資料表中）。COPY TO 還可以複製 SELECT 查詢的結果。

如果指定了欄位列表，則 COPY 將僅將指定欄位中的資料複製到檔案或從檔案複製。如果資料表中有任何欄位不在欄位列表中，則 COPY FROM 將插入這些欄位的預設值。

帶有檔案名稱的 COPY 指示 PostgreSQL 伺服器直接讀取或寫入檔案。PostgreSQL 使用者必須可以存取該檔案（伺服器執行的作業系統使用者 ID），並且必須從伺服器的角度指定名稱。使用 PROGRAM 時，伺服器執行給定的命令並從程序的標準輸出讀取，或寫入程序的標準輸入。必須從伺服器的角度使用該命令，並且該命令可由 PostgreSQL 作業系統使用者執行。指定 STDIN 或 STDOUT 時，資料透過用戶端和伺服器之間的連線傳輸。

## 參數

_`table_name`_

現有資料表的名稱（可選擇性加上綱要）。

_`column_name`_

要複製欄位的選擇性列表。如果未指定欄位列表，則將複製資料表的所有欄位。

_`query`_

[SELECT](select.md)，[VALUES](values.md)，[INSERT](insert.md)，[UPDATE](update.md) 或 [DELETE](delete.md) 指令，其結果將被複製。請注意，查詢周圍需要括號。

對於 INSERT，UPDATE 和 DELETE 查詢，必須提供 RETURNING 子句，並且目標關連不能具有條件規則，也不能具有 ALSO 規則，也不能具有延伸為多個語句的 INSTEAD 規則。

_`filename`_

輸入或輸出檔案的路徑名稱。輸入檔案名稱可以是絕對路徑或相對路徑，但輸出檔案名稱必須是絕對路徑。Windows 使用者可能需要使用 E''字串並將路徑名稱中所使用的任何倒斜線加倍。

`PROGRAM`

要執行的命令。在 COPY FROM 中，從命令的標準輸出讀取輸入；在 COPY TO 中，輸出給寫入命令的標準輸入。

請注意，該命令由 shell 呼叫，因此如果您需要將任何參數傳遞給來自不受信任來源的 shell 命令，則必須小心去除或轉義可能對 shell 具有特殊含義的任何特殊字串。出於安全原因，最好使用固定的命令字串，或者至少避免在其中傳遞任何使用者輸入參數。

`STDIN`

指定輸入來自用戶端應用程式。

`STDOUT`

指定輸出轉到用戶端應用程序式。

_`boolean`_

指定是應打開還是關閉所選選項。您可以寫入TRUE，ON 或 1 以啟用該選項，使用 FALSE，OFF 或 0 來停用它。布林值也可以省略，在這種情況下假定為 TRUE

`FORMAT`

選擇要讀取或寫入的資料格式：text，csv（逗號分隔值）或二進位。預設為 text。

`OIDS`

指定複製每個資料列的 OID。 （如果為沒有 OID 的資料表指定 OIDS，或者在複製查詢的情況下，會引發錯誤。）

`FREEZE`

請求複製已經凍結的資料列，就像在執行 VACUUM FREEZE 命令之後一樣。這是初始資料載入的效能選項。只有在目前子事務中建立或清空正在載入的資料表時，才會凍結資料列，而沒有使用中游標，並且此事務不保留舊的快照。

請注意，所有其他連線在成功載入後將立即能夠看到資料。這違反了 MVCC 可見性的正常規則，使用者應該知道這可能的潛在問題。

`DELIMITER`

指定用於分隔檔案每行內欄位的字元。預設值為 text 格式的 tab 字元，CSV 格式的逗號。這必須是一個單位元組字元。採用二進位格式時不允許使用此選項。

`NULL`

指定表示空值的字串。 預設值為 text 格式的 N（倒斜線-N）和 CSV 格式的未加引號的空字串。對於不希望將空值與空字串區分開的情況，即使是 text 格式，也可能更喜歡空字串。採用二進位格式時不允許使用此選項。

**注意**  
使用 COPY FROM 時，與該字串匹配的任何資料項都將儲存為空值，因此您應確保使用與 COPY TO 相同的字串。

`HEADER`

指定該檔案包含標題列，其中包含檔案中每個欄位的名稱。在輸出時，第一行包含資料表中的欄位名稱；在輸入時，第一行將被忽略。僅在採用 CSV 格式時才允許此選項。

`QUOTE`

指定引用資料值時要使用的引用字元。預設為雙引號。這必須是一個單位元組字元。僅在採用 CSV 格式時才允許此選項。

`ESCAPE`

指定應在與 QUOTE 值匹配的資料字元之前出現的字元。預設值與 QUOTE 值相同（因此，如果引號字元出現在資料中，則引號字元加倍）。這必須是一個單位元組字元。僅在使用 CSV 格式時才允許此選項。

`FORCE_QUOTE`

強制引用用於每個指定欄位中的所有非 NULL 值。從不引用 NULL 輸出。如果指定 \*，則將在所有欄位中引用非 NULL 值。此選項僅在 COPY TO 中允許，並且僅在使用 CSV 格式時允許。

`FORCE_NOT_NULL`

不要將指定欄位的值與空字串匹配。在 null 字串為空的預設情況下，這意味著空值將被讀取為零長度字串而不是空值，即使它們未被引用也是如此。此選項僅在 COPY FROM 中允許，並且僅能用在 CSV 格式時。

`FORCE_NULL`

將指定欄位的值與空字串匹配，即使它已被引用，如果找到匹配項，則將值設定為 NULL。在 null 字串為空的預設情況下，這會將帶引號的空字串轉換為 NULL。此選項僅在 COPY FROM 中允許，並且僅能用在 CSV 格式。

`ENCODING`

指定文件在 encoding\_name 中編碼。如果省略此選項，則使用目前用戶端編碼。有關詳細訊息，請參閱下面的註釋。

## 輸出

成功完成後，COPY 命令將回傳命令標記的形式

```text
COPY count
```

計數是複製的資料列數量。

**提醒**  
僅當命令不是 COPY ... TO STDOUT 或等效的 psql 元命令 \copy ... to stdout 時，psql 才會輸出此命令標記。這是為了防止命令標記與剛剛輸出的資料混淆。

## 注意

COPY TO 只能用於普通資料表，而不能用於檢視表。但是，您可以使用 COPY（SELECT \* FROM viewname） ...以被複製檢視表的目前內容。

COPY FROM 可以與普通資料表一起使用，也可以與具有 INSTEAD OF INSERT 觸發器的檢視表一起使用。

COPY 僅處理指定名稱的資料表；它不會將資料複製到子資料表或從子資料表複製資料。因此，例如 COPY table TO 會輸出與 SELECT _FROM ONLY table 相同的資料。但 COPY（SELECT_ FROM table）TO ... 可用於轉存繼承結構中的所有資料。

您必須對其值由 COPY TO 讀取的資料表具有 select 權限，並對透過 COPY FROM 插入值的資料表有 INSERT 權限。在命令中列出的欄位上具有欄位權限就足夠了。

如果為資料表啟用了資料列級安全性原則，則相關的 SELECT 安全原則將套用於 COPY table TO 語句。目前，具有資料列級安全性的資料表不支援 COPY FROM。請改用等效的 INSERT 語句。

在 COPY 命令中所指名的檔案由伺服器直接讀取或寫入，而不是由用戶端應用程序讀取或寫入。因此，它們必須儲存在資料庫伺服器主機上，或者具有它們的存取能力，而非用戶端。它們必須是 PostgreSQL 使用者帳號（伺服器執行的使用者 ID）可存取，可讀或可寫，而不是用戶端。同樣地，用 PROGRAM 指定的命令是由伺服器直接執行，而不是由用戶端應用程序執行，且必須由 PostgreSQL 使用者執行。COPY 指名的檔案或命令僅允許資料庫超級使用者使用，因為它允許讀取或寫入伺服器有權存取的任何檔案。

不要將 COPY 與 psql 指令 [\copy](../client-applications/psql.md) 混淆。\copy 呼叫 COPY FROM STDIN 或 COPY TO STDOUT，然後將資料讀取/儲存在 psql 用戶端可存取的檔案中。因此，使用 \copy時，檔案可存取性和存取權限取決於用戶端而不是伺服器端。

建議始終都將 COPY 中使用的檔案名稱指定為絕對路徑。這在 COPY TO 的情況下由伺服器是強制執行的，但對於 COPY FROM，您可以選擇由相對路徑指定的檔案中讀取。該路徑將相對於伺服器程序的工作目錄（通常是叢集的資料目錄）作為起點，而不是用戶端的工作目錄。

使用 PROGRAM 執行命令可能受作業系統的存取控制機制（如 SELinux）所限制。

COPY FROM 將呼叫目標資料表上的所有觸發器和檢查限制條件。但是，它不會呼叫規則。

對於標識欄位，COPY FROM 命令將會寫入輸入資料中提供的欄位值，如 INSERT 選項 OVERRIDING SYSTEM VALUE。

COPY 輸入和輸出受 DateStyle 影響。為確保可以使用非預設 DateStyle 設定的其他 PostgreSQL 安裝的可移植性，應在使用 COPY TO 之前將 DateStyle 設定為 ISO。避免使用 IntervalStyle 設定 tosql\_standard 轉存資料也是一個好主意，因為負間隔值可能會被具有不同 IntervalStyle 設定的伺服器所誤解。

輸入資料根據 ENCODING 選項或目前用戶端編碼進行解譯，輸出資料以 ENCODING 或目前用戶端編碼進行編碼，即使資料未透過用戶端而直接由伺服器讀取或寫入檔案。

COPY 會在第一個錯誤時停止操作。這不應該會使 COPY TO 出現問題，但目標資料表已經收到了 COPY FROM 中的之前的資料列。這些資料列將不可見或無法存取，但它們仍佔用磁碟空間。 如果故障發生在大量的複製操作中，則可能相當於浪費大量磁碟空間。您可能需要呼叫 VACUUM 來恢復浪費的空間。

FORCE\_NULL 和 FORCE\_NOT\_NULL 可以在同一個欄位上同時使用。這會導致將帶引號的空字串轉換為空值，將不帶引號的空字串轉換為空字串。

## 檔案格式

### Text Format

When the `text` format is used, the data read or written is a text file with one line per table row. Columns in a row are separated by the delimiter character. The column values themselves are strings generated by the output function, or acceptable to the input function, of each attribute's data type. The specified null string is used in place of columns that are null. `COPY FROM` will raise an error if any line of the input file contains more or fewer columns than are expected. If `OIDS` is specified, the OID is read or written as the first column, preceding the user data columns.

End of data can be represented by a single line containing just backslash-period \(`\.`\). An end-of-data marker is not necessary when reading from a file, since the end of file serves perfectly well; it is needed only when copying data to or from client applications using pre-3.0 client protocol.

Backslash characters \(`\`\) can be used in the `COPY` data to quote data characters that might otherwise be taken as row or column delimiters. In particular, the following characters _must_ be preceded by a backslash if they appear as part of a column value: backslash itself, newline, carriage return, and the current delimiter character.

The specified null string is sent by `COPY TO` without adding any backslashes; conversely, `COPY FROM` matches the input against the null string before removing backslashes. Therefore, a null string such as `\N` cannot be confused with the actual data value `\N` \(which would be represented as `\\N`\).

The following special backslash sequences are recognized by `COPY FROM`:

| Sequence | Represents |
| :--- | :--- |
| `\b` | Backspace \(ASCII 8\) |
| `\f` | Form feed \(ASCII 12\) |
| `\n` | Newline \(ASCII 10\) |
| `\r` | Carriage return \(ASCII 13\) |
| `\t` | Tab \(ASCII 9\) |
| `\v` | Vertical tab \(ASCII 11\) |
| `\`_`digits`_ | Backslash followed by one to three octal digits specifies the character with that numeric code |
| `\x`_`digits`_ | Backslash `x` followed by one or two hex digits specifies the character with that numeric code |

Presently, `COPY TO` will never emit an octal or hex-digits backslash sequence, but it does use the other sequences listed above for those control characters.

Any other backslashed character that is not mentioned in the above table will be taken to represent itself. However, beware of adding backslashes unnecessarily, since that might accidentally produce a string matching the end-of-data marker \(`\.`\) or the null string \(`\N` by default\). These strings will be recognized before any other backslash processing is done.

It is strongly recommended that applications generating `COPY` data convert data newlines and carriage returns to the `\n` and `\r` sequences respectively. At present it is possible to represent a data carriage return by a backslash and carriage return, and to represent a data newline by a backslash and newline. However, these representations might not be accepted in future releases. They are also highly vulnerable to corruption if the `COPY` file is transferred across different machines \(for example, from Unix to Windows or vice versa\).

`COPY TO` will terminate each row with a Unix-style newline \(“`\n`”\). Servers running on Microsoft Windows instead output carriage return/newline \(“`\r\n`”\), but only for `COPY` to a server file; for consistency across platforms, `COPY TO STDOUT` always sends “`\n`” regardless of server platform. `COPY FROM` can handle lines ending with newlines, carriage returns, or carriage return/newlines. To reduce the risk of error due to un-backslashed newlines or carriage returns that were meant as data, `COPY FROM` will complain if the line endings in the input are not all alike.

### CSV Format

此格式選項用於匯入和匯出許多其他應用程式（例如試算表）也常使用的逗號分隔（CSV, Comma Separated Value）檔案格式。它不會使用 PostgreSQL 的標準文字格式所使用轉譯規則，而是產成通用的 CSV 轉譯機制。

每個記錄中的值由 DELIMITER 字元分隔。如果該值包含 DELIMITER，QUOTE 字元，NULL 字串，Carriage Return 或換行字元，則整個值將以 QUOTE 字元前後夾住，以及在 QUOTE 字元或 ESCAPE 字元前面有轉譯字元。在特定欄位中輸出非 NULL 值時，也可以使用 FORCE\_QUOTE 強制使用引號。

CSV 格式沒有區分空值和空字串的標準方法。PostgreSQL 的 COPY 透過引號來處理。輸出 NULL 作為 NULL 參數字串，並且不加引號，而與 NULL 參數字串相符的非 NULL 值則被加引號。例如，使用預設設定，將 NULL 寫入未加引號的空字串，而將空字串資料值寫入雙引號（""）。 讀取時則遵循類似的規則。您可以使用 FORCE\_NOT\_NULL 來防止對特定欄位進行 NULL 輸入比較。您還可以使用 FORCE\_NULL 將帶引號的空字串轉換為 NULL。

由於反斜線不是 CSV 格式的特殊字元，因此 .（資料結尾標記）也可能會顯示為資料。 為避免任何誤解，請使用 . 在行上顯示為單獨項目的資料將在輸出上自動加上引號，並且在輸入（如果加引號）時不會被解釋為資料結束標記。如果要載入的檔案是由另一個應用程式產生的，該檔案只有一個未加引號的欄位，並且值可能為 .，則可能需要在輸入檔案中將值加上引號。

### 注意

{% hint style="info" %}
在 CSV 格式中，所有字元均為有效字元。用引號括起來的值用空格或除 DELIMITER 以外的任何字元包圍，將包括這些字元。如果從從空白行填充到固定寬度的 CSV 行的系統中匯入資料，則可能會導致錯誤。如果出現這種情況，在將資料匯入 PostgreSQL 之前，可能需要預處理 CSV 檔案以除去尾隨的空白字元。
{% endhint %}

{% hint style="info" %}
CSV 格式將識別並產生帶有括號的 CSV 檔案，這些值包含嵌入式回車字元和換行字元。因此，與文字格式的檔案相比，檔案並非嚴格限於每筆資料一行。
{% endhint %}

{% hint style="info" %}
許多程式會產生奇怪的，有時是錯誤的 CSV 檔案，因此檔案格式更像是一種約定，而不是一種標準。因此，您可能會遇到一些無法使用此機制匯入的檔案，並且 COPY 也可能會產生成其他程式無法處理的檔案內容。
{% endhint %}

### Binary 格式

binary 格式選項使所有資料以二進位格式而不是文字形式儲存/讀取。它比 text 和 CSV 格式快一些，但二進位格式檔案在機器架構和 PostgreSQL 版本之間的可移植性較低。此外，二進位格式是資料型別專屬的；例如，它不能從 smallint 欄位輸出二進位資料並將其讀入 int 欄位，即使它在 text 格式中可以正常運作。

二進位檔案格式由檔案標頭，包含資料列資料的零個或多個 tuple 以及檔案結尾組成。標頭和資料按 network byte order 排列。

**注意**  
7.4 之前的 PostgreSQL 版本使用了不同的二進位檔案格式。

**File Header**

The file header consists of 15 bytes of fixed fields, followed by a variable-length header extension area. The fixed fields are:Signature

11-byte sequence `PGCOPY\n\377\r\n\0` — note that the zero byte is a required part of the signature. \(The signature is designed to allow easy identification of files that have been munged by a non-8-bit-clean transfer. This signature will be changed by end-of-line-translation filters, dropped zero bytes, dropped high bits, or parity changes.\)Flags field

32-bit integer bit mask to denote important aspects of the file format. Bits are numbered from 0 \(LSB\) to 31 \(MSB\). Note that this field is stored in network byte order \(most significant byte first\), as are all the integer fields used in the file format. Bits 16-31 are reserved to denote critical file format issues; a reader should abort if it finds an unexpected bit set in this range. Bits 0-15 are reserved to signal backwards-compatible format issues; a reader should simply ignore any unexpected bits set in this range. Currently only one flag bit is defined, and the rest must be zero:Bit 16

if 1, OIDs are included in the data; if 0, notHeader extension area length

32-bit integer, length in bytes of remainder of header, not including self. Currently, this is zero, and the first tuple follows immediately. Future changes to the format might allow additional data to be present in the header. A reader should silently skip over any header extension data it does not know what to do with.

The header extension area is envisioned to contain a sequence of self-identifying chunks. The flags field is not intended to tell readers what is in the extension area. Specific design of header extension contents is left for a later release.

This design allows for both backwards-compatible header additions \(add header extension chunks, or set low-order flag bits\) and non-backwards-compatible changes \(set high-order flag bits to signal such changes, and add supporting data to the extension area if needed\).

**Tuples**

Each tuple begins with a 16-bit integer count of the number of fields in the tuple. \(Presently, all tuples in a table will have the same count, but that might not always be true.\) Then, repeated for each field in the tuple, there is a 32-bit length word followed by that many bytes of field data. \(The length word does not include itself, and can be zero.\) As a special case, -1 indicates a NULL field value. No value bytes follow in the NULL case.

There is no alignment padding or any other extra data between fields.

Presently, all data values in a binary-format file are assumed to be in binary format \(format code one\). It is anticipated that a future extension might add a header field that allows per-column format codes to be specified.

To determine the appropriate binary format for the actual tuple data you should consult the PostgreSQL source, in particular the `*send` and `*recv` functions for each column's data type \(typically these functions are found in the `src/backend/utils/adt/` directory of the source distribution\).

If OIDs are included in the file, the OID field immediately follows the field-count word. It is a normal field except that it's not included in the field-count. In particular it has a length word — this will allow handling of 4-byte vs. 8-byte OIDs without too much pain, and will allow OIDs to be shown as null if that ever proves desirable.

**File Trailer**

The file trailer consists of a 16-bit integer word containing -1. This is easily distinguished from a tuple's field-count word.

A reader should report an error if a field-count word is neither -1 nor the expected number of columns. This provides an extra check against somehow getting out of sync with the data.

## 範例

以下範例使用破折號「\|」作為欄位分隔符把資料表複製到用戶端：

```text
COPY country TO STDOUT (DELIMITER '|');
```

要將檔案中的資料複製到 country 資料表中：

```text
COPY country FROM '/usr1/proj/bray/sql/country_data';
```

要將名稱以「A」開頭的國家複製到檔案中：

```text
COPY (SELECT * FROM country WHERE country_name LIKE 'A%') TO '/usr1/proj/bray/sql/a_list_countries.copy';
```

要複製到壓縮檔案，可以透過外部壓縮程序輸出：

```text
COPY country TO PROGRAM 'gzip > /usr1/proj/bray/sql/country_data.gz';
```

以下是適合從 STDIN 複製到資料表中的資料範例：

```text
AF      AFGHANISTAN
AL      ALBANIA
DZ      ALGERIA
ZM      ZAMBIA
ZW      ZIMBABWE
```

請注意，每行上的空白實際上是 tab 字元。

以下是相同的資料，以二進位格式輸出。在透過 Unix 實用工具 od -c 過濾後顯示資料。該資料表有三個欄位；第一個是 char\(2\) 型別，第二個是 text 型別，第三個是 integer 型別。所有行在第三欄位中都具有空值。

```text
0000000   P   G   C   O   P   Y  \n 377  \r  \n  \0  \0  \0  \0  \0  \0
0000020  \0  \0  \0  \0 003  \0  \0  \0 002   A   F  \0  \0  \0 013   A
0000040   F   G   H   A   N   I   S   T   A   N 377 377 377 377  \0 003
0000060  \0  \0  \0 002   A   L  \0  \0  \0 007   A   L   B   A   N   I
0000100   A 377 377 377 377  \0 003  \0  \0  \0 002   D   Z  \0  \0  \0
0000120 007   A   L   G   E   R   I   A 377 377 377 377  \0 003  \0  \0
0000140  \0 002   Z   M  \0  \0  \0 006   Z   A   M   B   I   A 377 377
0000160 377 377  \0 003  \0  \0  \0 002   Z   W  \0  \0  \0  \b   Z   I
0000200   M   B   A   B   W   E 377 377 377 377 377 377
```

## 相容性

SQL 標準中沒有 COPY 語句。

在 PostgreSQL 版本 9.0 之前使用了以下語法並且仍然支援：

```text
COPY table_name [ ( column_name [, ...] ) ]
    FROM { 'filename' | STDIN }
    [ [ WITH ]
          [ BINARY ]
          [ OIDS ]
          [ DELIMITER [ AS ] 'delimiter' ]
          [ NULL [ AS ] 'null string' ]
          [ CSV [ HEADER ]
                [ QUOTE [ AS ] 'quote' ]
                [ ESCAPE [ AS ] 'escape' ]
                [ FORCE NOT NULL column_name [, ...] ] ] ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) }
    TO { 'filename' | STDOUT }
    [ [ WITH ]
          [ BINARY ]
          [ OIDS ]
          [ DELIMITER [ AS ] 'delimiter' ]
          [ NULL [ AS ] 'null string' ]
          [ CSV [ HEADER ]
                [ QUOTE [ AS ] 'quote' ]
                [ ESCAPE [ AS ] 'escape' ]
                [ FORCE QUOTE { column_name [, ...] | * } ] ] ]
```

請注意，在此語法中，BINARY 和 CSV 被視為獨立的關鍵字，而不是 FORMAT 選項的參數。

在 PostgreSQL 版本 7.3 之前使用了以下語法，並且仍然支援：

```text
COPY [ BINARY ] table_name [ WITH OIDS ]
    FROM { 'filename' | STDIN }
    [ [USING] DELIMITERS 'delimiter' ]
    [ WITH NULL AS 'null string' ]

COPY [ BINARY ] table_name [ WITH OIDS ]
    TO { 'filename' | STDOUT }
    [ [USING] DELIMITERS 'delimiter' ]
    [ WITH NULL AS 'null string' ]
```

