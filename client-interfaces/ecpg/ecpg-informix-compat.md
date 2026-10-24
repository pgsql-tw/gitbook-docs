<a id="ECPG-INFORMIX-COMPAT"></a>

## 34.15. Informix 相容模式 [#](#ecpg-informix-compat) <a href="#ecpg-informix-compat" id="ecpg-informix-compat"></a>

[34.15.1. 額外的型別](ecpg-informix-compat.md#ecpg-informix-types)

[34.15.2. 額外／缺少的嵌入式 SQL 陳述式](ecpg-informix-statements.md#ecpg-informix-statements)

[34.15.3. 與 Informix 相容的 SQLDA 描述區](ecpg-informix-sqlda.md#ecpg-informix-sqlda)

[34.15.4. 額外的函式](ecpg-informix-functions.md#ecpg-informix-functions)

[34.15.5. 額外的常數](ecpg-informix-constants.md#ecpg-informix-constants)

`ecpg` 可以在所謂的 *Informix 相容模式*下執行。啟用此模式時，它會嘗試表現得如同 Informix E/SQL 的 Informix 預編譯器一樣。一般來說，這讓你可以用錢字號取代 `EXEC SQL` 基本指令，來引導嵌入式 SQL 命令：

```

$int j = 3;
$CONNECT TO :dbname;
$CREATE TABLE test(i INT PRIMARY KEY, j INT);
$INSERT INTO test(i, j) VALUES (7, :j);
$COMMIT;
```

### 注意

`$` 與其後的前置處理器指令（也就是 `include`、`define`、`ifdef` 等）之間不可以有任何空白。否則，前置處理器會將該語法單元剖析為主機變數。

相容模式有兩種：`INFORMIX`、`INFORMIX_SE`

連結使用此相容模式的程式時，記得要連結 ECPG 隨附的 `libcompat`。

除了前面說明的語法糖之外，Informix 相容模式還將 E/SQL 中常見的一些資料輸入、輸出與轉換函式，以及嵌入式 SQL 陳述式移植到 ECPG。

Informix 相容模式與 ECPG 的 pgtypeslib 函式庫密切相關。pgtypeslib 將 SQL 資料型別對應到 C 主機程式中的資料型別，而 Informix 相容模式的大多數額外函式，讓你可以對這些 C 主機程式型別進行操作。不過請注意，相容的程度是有限的。它並不試圖複製 Informix 的行為；它讓你可以進行大致相同的操作，並提供名稱相同、基本行為也相同的函式，但如果你目前正在使用 Informix，它並不能直接替換。此外，有些資料型別並不相同。例如，PostgreSQL 的 datetime 與 interval 型別不認得像 `YEAR TO MINUTE` 這樣的範圍，因此你在 ECPG 中也找不到對此的支援。

<a id="ECPG-INFORMIX-TYPES"></a>

### 34.15.1. 額外的型別 [#](#ecpg-informix-types) <a href="#ecpg-informix-types" id="ecpg-informix-types"></a>

Informix 特有的「string」虛擬型別用於儲存已去除右側空白的字元字串資料，現在於 Informix 模式中不需使用 `typedef` 即可支援。事實上，在 Informix 模式中，ECPG 會拒絕處理含有 `typedef sometype string;` 的原始檔。

```

EXEC SQL BEGIN DECLARE SECTION;
string userid; /* this variable will contain trimmed data */
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH MYCUR INTO :userid;
```

<a id="ECPG-INFORMIX-STATEMENTS"></a>

### 34.15.2. 額外／缺少的嵌入式 SQL 陳述式 [#](#ecpg-informix-statements) <a href="#ecpg-informix-statements" id="ecpg-informix-statements"></a>

本節內容請參閱[34.15.2. 額外／缺少的嵌入式 SQL 陳述式](ecpg-informix-statements.md#ecpg-informix-statements)。

<a id="ECPG-INFORMIX-SQLDA"></a>

### 34.15.3. 與 Informix 相容的 SQLDA 描述區 [#](#ecpg-informix-sqlda) <a href="#ecpg-informix-sqlda" id="ecpg-informix-sqlda"></a>

本節內容請參閱[34.15.3. 與 Informix 相容的 SQLDA 描述區](ecpg-informix-sqlda.md#ecpg-informix-sqlda)。

<a id="ECPG-INFORMIX-FUNCTIONS"></a>

### 34.15.4. 額外的函式 [#](#ecpg-informix-functions) <a href="#ecpg-informix-functions" id="ecpg-informix-functions"></a>

本節內容請參閱[34.15.4. 額外的函式](ecpg-informix-functions.md#ecpg-informix-functions)。

<a id="ECPG-INFORMIX-CONSTANTS"></a>

### 34.15.5. 額外的常數 [#](#ecpg-informix-constants) <a href="#ecpg-informix-constants" id="ecpg-informix-constants"></a>

本節內容請參閱[34.15.5. 額外的常數](ecpg-informix-constants.md#ecpg-informix-constants)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
