<a id="SQL-CREATEOPFAMILY"></a><a id="id-1.9.3.74.1"></a>

## CREATE OPERATOR FAMILY

CREATE OPERATOR FAMILY — 定義新的運算子家族

<a id="id-1.9.3.74.4"></a>

## 語法

```

CREATE OPERATOR FAMILY name USING index_method
```

<a id="id-1.9.3.74.5"></a>

## 說明

`CREATE OPERATOR FAMILY` 會建立新的運算子家族。運算子家族定義了一組相關的運算子類別，也可能包含一些額外的運算子與支援函式；這些運算子與函式和這些運算子類別相容，但對任何個別索引的運作而言並非必要。（對索引而言必要的運算子與函式，應該歸入相關的運算子類別，而不是「鬆散地」放在運算子家族中。通常，單一資料型別的運算子會綁定在運算子類別上，而跨資料型別的運算子則可以鬆散地放在一個同時包含兩種資料型別之運算子類別的運算子家族中。）

新的運算子家族一開始是空的。應該接著執行 `CREATE OPERATOR CLASS` 命令加入其所包含的運算子類別，並可選擇執行 `ALTER OPERATOR FAMILY` 命令加入「鬆散的」運算子及其對應的支援函式，以充實其內容。

若有提供綱要名稱，運算子家族會建立在指定的綱要中；否則會建立在目前的綱要中。同一綱要中的兩個運算子家族，只有在用於不同的索引方法時才可以同名。

定義運算子家族的使用者會成為其擁有者。目前，建立者必須是超級使用者。（之所以有此限制，是因為錯誤的運算子家族定義可能使伺服器混亂，甚至使伺服器當機。）

更多資訊請參閱[第 36.16 節](../../server-programming/extend/xindex.md)。

<a id="id-1.9.3.74.6"></a>

## 參數

*`name`*
:   要建立之運算子家族的名稱。名稱可以用綱要限定。

*`index_method`*
:   此運算子家族所適用之索引方法的名稱。

<a id="id-1.9.3.74.7"></a>

## 相容性

`CREATE OPERATOR FAMILY` 是 PostgreSQL 的擴充語法。SQL 標準中沒有 `CREATE OPERATOR FAMILY` 陳述式。

<a id="id-1.9.3.74.8"></a>

## 另請參閱

[ALTER OPERATOR FAMILY](sql-alteropfamily.md), [DROP OPERATOR FAMILY](sql-dropopfamily.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [ALTER OPERATOR CLASS](sql-alteropclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createopfamily.html)（原文版本：18.6；核對日期：2026-10-04）
