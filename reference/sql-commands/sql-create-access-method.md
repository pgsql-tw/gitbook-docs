<a id="SQL-CREATE-ACCESS-METHOD"></a><a id="id-1.9.3.56.1"></a>

## CREATE ACCESS METHOD

CREATE ACCESS METHOD — 定義新的存取方法

<a id="id-1.9.3.56.4"></a>

## 語法

```

CREATE ACCESS METHOD name
    TYPE access_method_type
    HANDLER handler_function
```

<a id="id-1.9.3.56.5"></a>

## 說明

`CREATE ACCESS METHOD` 會建立新的存取方法。

存取方法的名稱在資料庫中必須是唯一的。

只有超級使用者可以定義新的存取方法。

<a id="id-1.9.3.56.6"></a>

## 參數

*`name`*
:   要建立之存取方法的名稱。

*`access_method_type`*
:   此子句指定要定義的存取方法類型。
    目前只支援 `TABLE` 與 `INDEX`。

*`handler_function`*
:   *`handler_function`* 是先前已註冊、代表該存取方法之函式的名稱（可能以綱要限定）。處理函式必須宣告為接受單一個 `internal` 型別的參數，其傳回型別則取決於存取方法的類型；對於 `TABLE` 存取方法，傳回型別必須是 `table_am_handler`，對於 `INDEX` 存取方法，則必須是 `index_am_handler`。
    處理函式必須實作的 C 層級 API 依存取方法的類型而異。資料表存取方法 API 說明於[第 62 章](../../internals/tableam/README.md)，索引存取方法 API 說明於[第 63 章](../../internals/indexam/README.md)。

<a id="id-1.9.3.56.7"></a>

## 範例

建立索引存取方法 `heptree`，其處理函式為 `heptree_handler`：

```

CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

<a id="id-1.9.3.56.8"></a>

## 相容性

`CREATE ACCESS METHOD` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.56.9"></a>

## 另請參閱

[DROP ACCESS METHOD](sql-drop-access-method.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [CREATE OPERATOR FAMILY](sql-createopfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-create-access-method.html)（原文版本：18.6；核對日期：2026-10-04）
