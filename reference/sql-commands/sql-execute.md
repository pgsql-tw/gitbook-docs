<a id="SQL-EXECUTE"></a><a id="id-1.9.3.147.1"></a><a id="id-1.9.3.147.2"></a>

## EXECUTE

EXECUTE — 執行預備陳述式

<a id="id-1.9.3.147.5"></a>

## 語法

```

EXECUTE name [ ( parameter [, ...] ) ]
```

<a id="id-1.9.3.147.6"></a>

## 說明

`EXECUTE` 用來執行先前預備好的陳述式。由於預備陳述式只在工作階段期間存在，因此該預備陳述式必須是由目前工作階段中稍早執行的 `PREPARE` 陳述式所建立。

若建立該陳述式的 `PREPARE` 陳述式指定了一些參數，則必須將一組相容的參數傳給 `EXECUTE` 陳述式，否則會引發錯誤。請注意，預備陳述式（不同於函式）不會依據其參數的型別或數量進行多載；預備陳述式的名稱在資料庫工作階段中必須是唯一的。

有關預備陳述式建立與使用的更多資訊，請參閱 [PREPARE](sql-prepare.md)。

<a id="id-1.9.3.147.7"></a>

## 參數

*`name`*
:   要執行的預備陳述式名稱。

*`parameter`*
:   傳給預備陳述式之參數的實際值。這必須是一個運算式，其產生的值與此參數的資料型別相容，而該資料型別是在建立預備陳述式時所決定的。

<a id="id-1.9.3.147.8"></a>

## 輸出

`EXECUTE` 傳回的命令標籤是該預備陳述式的命令標籤，而不是 `EXECUTE`。

<a id="id-1.9.3.147.9"></a>

## 範例

範例收錄於 [PREPARE](sql-prepare.md) 文件的[範例](sql-prepare.md#SQL-PREPARE-EXAMPLES)一節中。

<a id="id-1.9.3.147.10"></a>

## 相容性

SQL 標準包含 `EXECUTE` 陳述式，但它僅供嵌入式 SQL 使用。此版本的 `EXECUTE` 陳述式所使用的語法也略有不同。

<a id="id-1.9.3.147.11"></a>

## 另請參閱

[DEALLOCATE](sql-deallocate.md), [PREPARE](sql-prepare.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-execute.html)（原文版本：18.6；核對日期：2026-10-03）
