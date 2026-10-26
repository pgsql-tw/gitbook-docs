<a id="SQL-CREATEOPERATOR"></a><a id="id-1.9.3.72.1"></a>

## CREATE OPERATOR

CREATE OPERATOR — 定義新的運算子

<a id="id-1.9.3.72.4"></a>

## 語法

```

CREATE OPERATOR name (
    {FUNCTION|PROCEDURE} = function_name
    [, LEFTARG = left_type ] [, RIGHTARG = right_type ]
    [, COMMUTATOR = com_op ] [, NEGATOR = neg_op ]
    [, RESTRICT = res_proc ] [, JOIN = join_proc ]
    [, HASHES ] [, MERGES ]
)
```

<a id="id-1.9.3.72.5"></a>

## 說明

`CREATE OPERATOR` 會定義一個新的運算子 *`name`*。定義運算子的使用者會成為其擁有者。若有給定綱要名稱，運算子就會建立在指定的綱要中；否則會建立在目前的綱要中。

運算子名稱是由下列清單中的字元所組成的序列，最多 `NAMEDATALEN`-1 個字元（預設為 63）：

<br>
+ - \* / < > = ~ ! @ # % ^ & | ` ?<br>

名稱的選擇有幾項限制：

* `--` 與 `/*` 不能出現在運算子名稱中的任何位置，因為它們會被視為註解的開頭。
* 多字元的運算子名稱不能以 `+` 或
  `-` 結尾，
  除非名稱中也包含下列字元中的至少一個：

  <br>
  ~ ! @ # % ^ & | ` ?<br>

  例如，`@-` 是允許的運算子名稱，
  但 `*-` 不是。
  這項限制讓 PostgreSQL 能夠剖析符合 SQL 規範的命令，而不需要在語彙單元之間加上空格。
* 符號 `=>` 由 SQL 文法保留，
  因此不能用作運算子名稱。

運算子 `!=` 在輸入時會被對應為 `<>`，因此這兩個名稱永遠是等價的。

對二元運算子而言，`LEFTARG` 與 `RIGHTARG` 都必須定義。對前置運算子而言，只應該定義 `RIGHTARG`。*`function_name`* 函式必須事先使用 `CREATE
FUNCTION` 定義，而且必須定義為接受正確數量（一個或兩個）、且為指定型別的引數。

在 `CREATE OPERATOR` 的語法中，關鍵字 `FUNCTION` 與 `PROCEDURE` 是等價的，但所參照的函式無論如何都必須是函式，而不是程序。此處使用關鍵字 `PROCEDURE` 是歷史因素，且已不建議使用。

其他子句指定的是選用的運算子最佳化屬性。它們的意義在[第 36.15 節](../../server-programming/extend/xoper-optimization.md)中有詳細說明。

若要能夠建立運算子，你必須在引數型別與傳回型別上具有 `USAGE` 權限，以及在底層函式上具有 `EXECUTE` 權限。若指定了交換子或否定子運算子，你必須擁有這些運算子。

<a id="id-1.9.3.72.6"></a>

## 參數

*`name`*
:   要定義之運算子的名稱。允許的字元請參閱上文。名稱可以用綱要限定，例如 `CREATE OPERATOR myschema.+ (...)`。若未限定，運算子會建立在目前的綱要中。同一個綱要中的兩個運算子，若作用於不同的資料型別，就可以具有相同的名稱。這稱為*多載*（*overloading*）。

*`function_name`*
:   用來實作此運算子的函式。

*`left_type`*
:   運算子左運算元（若有的話）的資料型別。前置運算子會省略此選項。

*`right_type`*
:   運算子右運算元的資料型別。

*`com_op`*
:   此運算子的交換子。

*`neg_op`*
:   此運算子的否定子。

*`res_proc`*
:   此運算子的限制選擇性估算函式。

*`join_proc`*
:   此運算子的連接選擇性估算函式。

`HASHES`
:   表示此運算子可以支援雜湊連接。

`MERGES`
:   表示此運算子可以支援合併連接。

若要在 *`com_op`* 或其他選用引數中給定以綱要限定的運算子名稱，請使用 `OPERATOR()` 語法，例如：

```

COMMUTATOR = OPERATOR(myschema.===) ,
```

<a id="id-1.9.3.72.7"></a>

## 注意事項

更多資訊請參閱[第 36.14 節](../../server-programming/extend/xoper.md)與[第 36.15 節](../../server-programming/extend/xoper-optimization.md)。

定義自我交換的運算子時，直接定義即可。定義一對互為交換的運算子時，事情就稍微棘手一些：先定義的那一個要如何參照尚未定義的另一個？這個問題有三種解決方式：

* 一種方式是在你定義的第一個運算子中省略 `COMMUTATOR` 子句，然後在第二個運算子的定義中提供該子句。由於 PostgreSQL 知道交換運算子是成對出現的，當它看到第二個定義時，會自動回頭填入第一個定義中缺少的 `COMMUTATOR` 子句。
* 另一種更直接的方式，是在兩個定義中都包含 `COMMUTATOR` 子句。當 PostgreSQL 處理第一個定義並發現 `COMMUTATOR` 參照的是不存在的運算子時，系統會在系統目錄中為該運算子建立一個虛擬項目。這個虛擬項目只有運算子名稱、左右運算元型別與擁有者具有有效資料，因為這些是 PostgreSQL 在此時能推斷出的全部資訊。第一個運算子的目錄項目會連結到這個虛擬項目。之後當你定義第二個運算子時，系統會以第二個定義中的額外資訊更新該虛擬項目。若你在虛擬運算子被填入之前就嘗試使用它，只會得到錯誤訊息。
* 或者，也可以在定義兩個運算子時都不使用 `COMMUTATOR` 子句，然後使用 `ALTER OPERATOR` 設定它們的交換子連結。對這一對中的任一個執行 `ALTER` 就足夠了。

在這三種情況下，你都必須擁有這兩個運算子，才能將它們標記為交換子。

成對的否定子運算子，可以使用與交換子配對相同的方法來定義。

無法在 `CREATE OPERATOR` 中指定運算子的語彙優先順序，因為剖析器的優先順序行為是寫死的。優先順序的詳細資訊請參閱[第 4.1.6 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#sql-precedence)。

已過時的選項 `SORT1`、`SORT2`、`LTCMP` 與 `GTCMP` 以前用來指定與可合併連接之運算子相關聯的排序運算子名稱。現在已不再需要這樣做，因為相關聯運算子的資訊改為透過查看 B-tree 運算子家族來取得。若給定了這些選項中的某一個，它會被忽略，只是會隱含地將 `MERGES` 設為 true。

請使用 [`DROP OPERATOR`](sql-dropoperator.md) 從資料庫刪除使用者定義的運算子。請使用 [`ALTER OPERATOR`](sql-alteroperator.md) 修改資料庫中的運算子。

<a id="id-1.9.3.72.8"></a>

## 範例

下列命令為資料型別 `box` 定義一個新的運算子：面積相等（area-equality）：

```

CREATE OPERATOR === (
    LEFTARG = box,
    RIGHTARG = box,
    FUNCTION = area_equal_function,
    COMMUTATOR = ===,
    NEGATOR = !==,
    RESTRICT = area_restriction_function,
    JOIN = area_join_function,
    HASHES, MERGES
);
```

<a id="id-1.9.3.72.9"></a>

## 相容性

`CREATE OPERATOR` 是 PostgreSQL 的擴充語法。SQL 標準中沒有關於使用者定義運算子的規定。

<a id="id-1.9.3.72.10"></a>

## 另請參閱

[ALTER OPERATOR](sql-alteroperator.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [DROP OPERATOR](sql-dropoperator.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createoperator.html)（原文版本：18.6；核對日期：2026-10-04）
