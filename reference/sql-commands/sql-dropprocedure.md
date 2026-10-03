<a id="SQL-DROPPROCEDURE"></a><a id="id-1.9.3.124.1"></a>

## DROP PROCEDURE

DROP PROCEDURE — 移除程序

<a id="id-1.9.3.124.4"></a>

## 語法

```

DROP PROCEDURE [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.124.5"></a>

## 說明

`DROP PROCEDURE` 會移除一個或多個現有程序的定義。要執行此命令，使用者必須是該（些）程序的擁有者。通常必須指定程序的引數型別，因為可能存在多個名稱相同但引數列表不同的程序。

<a id="id-1.9.3.124.6"></a>

## 參數

`IF EXISTS`
:   程序不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有程序的名稱（可選擇以綱要限定）。

*`argmode`*
:   引數的模式：`IN`、`OUT`、
    `INOUT` 或 `VARIADIC`。若省略，
    預設為 `IN`（但請參閱下文）。

*`argname`*
:   引數的名稱。
    請注意，`DROP PROCEDURE` 實際上並不理會引數名稱，因為只有引數的資料型別會用來判定程序的身分。

*`argtype`*
:   程序引數（若有）的資料型別（可選擇以綱要限定）。
    詳細資訊請參閱下文。

`CASCADE`
:   自動移除相依於程序的物件，以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於程序則拒絕移除。這是預設行為。

<a id="SQL-DROPPROCEDURE-NOTES"></a>

## 注意事項

若給定名稱的程序只有一個，則可以省略引數列表。此情況下括號也要一併省略。

在 PostgreSQL 中，只需列出輸入引數（包括 `INOUT`）就足夠了，因為不允許兩個同名的常式具有相同的輸入引數列表。此外，`DROP` 命令實際上並不會檢查您是否正確寫出 `OUT` 引數的型別；因此任何明確標記為 `OUT` 的引數都只是雜訊。但為了與對應的 `CREATE` 命令保持一致，建議還是寫出它們。

為了與 SQL 標準相容，也允許寫出所有引數的資料型別（包括 `OUT` 引數的型別），而不加任何 *`argmode`* 標記。這樣做時，程序 `OUT` 引數的型別*將會*依據命令加以驗證。這項規定造成了歧義：當引數列表不含任何 *`argmode`* 標記時，無法明確得知要套用哪一種規則。`DROP` 命令會以兩種方式嘗試查找，若找到兩個不同的程序則會擲出錯誤。為了避免這種歧義的風險，建議明確寫出 `IN` 標記，而不要讓它採用預設值，藉此強制使用傳統的 PostgreSQL 解讀方式。

剛才說明的查找規則，也適用於其他作用在現有程序上的命令，例如 `ALTER PROCEDURE` 與 `COMMENT ON PROCEDURE`。

<a id="SQL-DROPPROCEDURE-EXAMPLES"></a>

## 範例

若只有一個程序 `do_db_maintenance`，以下命令就足以移除它：

```

DROP PROCEDURE do_db_maintenance;
```

給定以下程序定義：

```

CREATE PROCEDURE do_db_maintenance(IN target_schema text, OUT results text) ...
```

以下任何一個命令都可以移除它：

```

DROP PROCEDURE do_db_maintenance(IN target_schema text, OUT results text);
DROP PROCEDURE do_db_maintenance(IN text, OUT text);
DROP PROCEDURE do_db_maintenance(IN text);
DROP PROCEDURE do_db_maintenance(text);
DROP PROCEDURE do_db_maintenance(text, text);  -- potentially ambiguous
```

不過，若同時還存在例如以下的程序，最後一個範例就會有歧義：

```

CREATE PROCEDURE do_db_maintenance(IN target_schema text, IN options text) ...
```

<a id="SQL-DROPPROCEDURE-COMPATIBILITY"></a>

## 相容性

此命令符合 SQL 標準，但有以下 PostgreSQL 擴充功能：

* 標準只允許每個命令移除一個程序。
* `IF EXISTS` 選項是擴充功能。
* 指定引數模式與名稱的能力是擴充功能，而且在給定模式時，查找規則有所不同。

<a id="id-1.9.3.124.10"></a>

## 另請參閱

[CREATE PROCEDURE](sql-createprocedure.md), [ALTER PROCEDURE](sql-alterprocedure.md), [DROP FUNCTION](sql-dropfunction.md), [DROP ROUTINE](sql-droproutine.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropprocedure.html)（原文版本：18.6；核對日期：2026-10-03）
