<a id="ECPG-VARIABLES"></a>

## 34.4. 使用主機變數 [#](#ecpg-variables) <a href="#ecpg-variables" id="ecpg-variables"></a>

[34.4.1. 概觀](ecpg-variables.md#ecpg-variables-overview)

[34.4.2. 宣告區段](ecpg-variables.md#ecpg-declare-sections)

[34.4.3. 取得查詢結果](ecpg-variables.md#ecpg-retrieving)

[34.4.4. 型別對應](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)

[34.4.5. 處理非基本 SQL 資料型別](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql)

[34.4.6. 指示變數](ecpg-variables.md#ecpg-indicators)

在[第 34.3 節](ecpg-commands.md)中，你已經看到如何從嵌入式 SQL 程式執行 SQL 陳述式。其中有些陳述式只使用固定的值，無法把使用者提供的值放進陳述式，也無法讓程式處理查詢傳回的值。這類陳述式在實際的應用程式中並不實用。本節將詳細說明如何透過一種稱為*主機變數*的簡單機制，在 C 程式與嵌入式 SQL 陳述式之間傳遞資料。在嵌入式 SQL 程式中，我們把 SQL 陳述式視為 C 程式碼中的*客人*，而 C 程式碼則是*主機語言*。因此，C 程式的變數稱為*主機變數*。

在 PostgreSQL 後端與 ECPG 應用程式之間交換值的另一種方式是使用 SQL 描述區，詳見[第 34.7 節](ecpg-descriptors.md)。

<a id="ECPG-VARIABLES-OVERVIEW"></a>

### 34.4.1. 概觀 [#](#ecpg-variables-overview) <a href="#ecpg-variables-overview" id="ecpg-variables-overview"></a>

在嵌入式 SQL 中，於 C 程式與 SQL 陳述式之間傳遞資料特別簡單。你不必讓程式把資料貼進陳述式（這會帶來各種麻煩，例如必須正確地為值加上引號），只要把 C 變數的名稱加上冒號前綴寫進 SQL 陳述式即可。例如：

```

EXEC SQL INSERT INTO sometable VALUES (:v1, 'foo', :v2);
```

這個陳述式參照了兩個名為 `v1` 與 `v2` 的 C 變數，同時也使用了一般的 SQL 字串常數，以說明你並不受限於只能使用其中一種資料。

這種在 SQL 陳述式中插入 C 變數的寫法，在 SQL 陳述式中任何預期出現值表示式的地方都可以使用。

<a id="ECPG-DECLARE-SECTIONS"></a>

### 34.4.2. 宣告區段 [#](#ecpg-declare-sections) <a href="#ecpg-declare-sections" id="ecpg-declare-sections"></a>

若要把資料從程式傳給資料庫（例如作為查詢的參數），或把資料從資料庫傳回程式，用來存放這些資料的 C 變數必須宣告在特別標示的區段中，讓嵌入式 SQL 前置處理器得以知道它們。

這個區段以下列敘述開始：

```

EXEC SQL BEGIN DECLARE SECTION;
```

並以下列敘述結束：

```

EXEC SQL END DECLARE SECTION;
```

在這兩行之間必須是一般的 C 變數宣告，例如：

```

int   x = 4;
char  foo[16], bar[16];
```

如你所見，你可以選擇為變數指定初始值。變數的作用範圍取決於其宣告區段在程式中的位置。你也可以使用下列語法宣告變數，這會隱含地建立一個宣告區段：

```

EXEC SQL int i = 4;
```

一個程式中可以有任意多個宣告區段。

這些宣告也會以一般 C 變數的形式輸出到輸出檔案中，因此不需要再宣告一次。不打算在 SQL 命令中使用的變數，可以在這些特殊區段之外以一般方式宣告。

結構（struct）或聯合（union）的定義也必須列在 `DECLARE` 區段之內。否則前置處理器無法處理這些型別，因為它不知道其定義。

<a id="ECPG-RETRIEVING"></a>

### 34.4.3. 取得查詢結果 [#](#ecpg-retrieving) <a href="#ecpg-retrieving" id="ecpg-retrieving"></a>

現在你應該已經能把程式產生的資料傳入 SQL 命令了。但要如何取得查詢的結果呢？為此，嵌入式 SQL 提供了常用命令 `SELECT` 與 `FETCH` 的特殊變體。這些命令有一個特殊的 `INTO` 子句，用來指定取得的值要存放到哪些主機變數中。`SELECT` 用於只傳回單一資料列的查詢，而 `FETCH` 則搭配游標，用於傳回多筆資料列的查詢。

以下是一個範例：

```

/*
 * assume this table:
 * CREATE TABLE test1 (a int, b varchar(50));
 */

EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL SELECT a, b INTO :v1, :v2 FROM test;
```

譯註：原文範例註解假設的資料表名稱為 test1，但 SELECT 陳述式查詢的是 test；範例程式碼依原文保留，實際使用時兩者應一致。

所以 `INTO` 子句出現在選取清單與 `FROM` 子句之間。選取清單中的元素數目必須與 `INTO` 之後的清單（也稱為目標清單）的元素數目相等。

以下是使用 `FETCH` 命令的範例：

```

EXEC SQL BEGIN DECLARE SECTION;
int v1;
VARCHAR v2;
EXEC SQL END DECLARE SECTION;

 ...

EXEC SQL DECLARE foo CURSOR FOR SELECT a, b FROM test;

 ...

do
{
    ...
    EXEC SQL FETCH NEXT FROM foo INTO :v1, :v2;
    ...
} while (...);
```

這裡的 `INTO` 子句出現在所有一般子句之後。

<a id="ECPG-VARIABLES-TYPE-MAPPING"></a>

### 34.4.4. 型別對應 [#](#ecpg-variables-type-mapping) <a href="#ecpg-variables-type-mapping" id="ecpg-variables-type-mapping"></a>

本節內容請參閱[34.4.4. 型別對應](ecpg-variables-type-mapping.md#ecpg-variables-type-mapping)。

<a id="ECPG-VARIABLES-ARRAYS"></a>

### 34.4.4.3.1. 陣列 [#](#ecpg-variables-arrays) <a href="#ecpg-variables-arrays" id="ecpg-variables-arrays"></a>

本節內容請參閱[34.4.4.3.1. 陣列](ecpg-variables-nonprimitive-c.md#ecpg-variables-arrays)。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL"></a>

### 34.4.5. 處理非基本 SQL 資料型別 [#](#ecpg-variables-nonprimitive-sql) <a href="#ecpg-variables-nonprimitive-sql" id="ecpg-variables-nonprimitive-sql"></a>

本節內容請參閱[34.4.5. 處理非基本 SQL 資料型別](ecpg-variables-nonprimitive-sql.md#ecpg-variables-nonprimitive-sql)。

<a id="ECPG-INDICATORS"></a>

### 34.4.6. 指示變數 [#](#ecpg-indicators) <a href="#ecpg-indicators" id="ecpg-indicators"></a>

上面的範例都沒有處理空值。事實上，如果取得資料的範例從資料庫取得空值，就會引發錯誤。為了能把空值傳給資料庫，或從資料庫取得空值，你需要為每個存放資料的主機變數再附加第二個主機變數規格。這第二個主機變數稱為*指示變數*（indicator），其中包含一個旗標，指出該資料是否為空值；若為空值，實際主機變數的值會被忽略。以下是一個正確處理取得空值的範例：

```

EXEC SQL BEGIN DECLARE SECTION;
VARCHAR val;
int val_ind;
EXEC SQL END DECLARE SECTION:

 ...

EXEC SQL SELECT b INTO :val :val_ind FROM test1;
```

譯註：原文此範例中 END DECLARE SECTION 之後的冒號應為分號；範例程式碼依原文保留。

若值不是空值，指示變數 `val_ind` 會是零；若值是空值，則會是負數。（若要啟用 Oracle 特有的行為，請參閱[第 34.16 節](ecpg-oracle-compat.md)。）

指示變數還有另一項功能：若指示變數的值為正數，表示該值不是空值，但在存入主機變數時被截斷了。

如果把引數 `-r no_indicator` 傳給前置處理器 `ecpg`，它會以「無指示變數」模式運作。在無指示變數模式下，若未指定指示變數，空值會（在輸入與輸出時）以下列方式表示：字元字串型別以空字串表示，整數型別則以該型別可能的最小值表示（例如 `int` 的 `INT_MIN`）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
