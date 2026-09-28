<a id="id-1.9.3.171.1"></a>

## SECURITY LABEL

SECURITY LABEL — 定義或變更套用於某個物件的安全性標籤

## 語法

```

SECURITY LABEL [ FOR provider ] ON
{
  TABLE object_name |
  COLUMN table_name.column_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  DATABASE object_name |
  DOMAIN object_name |
  EVENT TRIGGER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  LARGE OBJECT large_object_oid |
  MATERIALIZED VIEW object_name |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  PUBLICATION object_name |
  ROLE object_name |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  SCHEMA object_name |
  SEQUENCE object_name |
  SUBSCRIPTION object_name |
  TABLESPACE object_name |
  TYPE object_name |
  VIEW object_name
} IS { string_literal | NULL }

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

<a id="id-1.9.3.171.5"></a>

## 說明

`SECURITY LABEL` 會將安全性標籤套用到資料庫物件上。
給定的資料庫物件可以關聯任意數量的安全性標籤，每個標籤提供者一個。
標籤提供者是可載入的模組，會透過
`register_label_provider` 函式自行註冊。

### 注意

`register_label_provider` 並非 SQL 函式；它只能從載入後端的
C 程式碼中呼叫。

標籤提供者決定給定的標籤是否有效，以及是否允許將該標籤指派給
給定的物件。給定標籤的意義，同樣由標籤提供者自行決定。
PostgreSQL 對標籤提供者應如何（或是否）解讀安全性標籤，
不做任何限制；它只是提供一個儲存標籤的機制。實務上，此功能的用意
在於能與以標籤為基礎的強制存取控制（MAC）系統（例如
SELinux）整合。這類系統會完全依據物件標籤來做出所有存取控制決策，
而非傳統的自主存取控制（DAC）概念，如使用者與群組。

你必須擁有該資料庫物件，才能使用 `SECURITY LABEL`。

<a id="id-1.9.3.171.6"></a>

## 參數

*`object_name`*<br>*`table_name.column_name`*<br>*`aggregate_name`*<br>*`function_name`*<br>*`procedure_name`*<br>*`routine_name`*
:   要加上標籤之物件的名稱。位於綱要中的物件名稱（資料表、函式等）
    可以加上綱要限定。

*`provider`*
:   要與此標籤關聯的提供者名稱。所指定的提供者必須已載入，
    且必須同意這項標籤操作的提議。若剛好只載入一個提供者，
    為求簡潔可以省略提供者名稱。

*`argmode`*
:   函式、程序或彙總函式引數的模式：`IN`、`OUT`、
    `INOUT`，或 `VARIADIC`。
    若省略，預設為 `IN`。
    請注意，`SECURITY LABEL` 實際上並不理會
    `OUT` 引數，因為只需要輸入引數即可判斷函式的身分。
    因此只需列出 `IN`、`INOUT`
    與 `VARIADIC` 引數即可。

*`argname`*
:   函式、程序或彙總函式引數的名稱。
    請注意，`SECURITY LABEL` 實際上並不理會引數名稱，
    因為只需要引數的資料型別即可判斷函式的身分。

*`argtype`*
:   函式、程序或彙總函式引數的資料型別。

*`large_object_oid`*
:   大型物件的 OID。

`PROCEDURAL`
:   這是一個語意上無作用的贅字。

*`string_literal`*
:   安全性標籤的新設定值，以字串常值寫成。

`NULL`
:   寫入 `NULL` 可移除該安全性標籤。

<a id="id-1.9.3.171.7"></a>

## 範例

以下範例顯示如何設定或變更某資料表的安全性標籤：

```

SECURITY LABEL FOR selinux ON TABLE mytable IS 'system_u:object_r:sepgsql_table_t:s0';
```

移除該標籤：

```

SECURITY LABEL FOR selinux ON TABLE mytable IS NULL;
```

<a id="id-1.9.3.171.8"></a>

## 相容性

SQL 標準中沒有 `SECURITY LABEL` 命令。

<a id="id-1.9.3.171.9"></a>

## 另請參閱

[sepgsql](../../appendixes/contrib/sepgsql.md)、`src/test/modules/dummy_seclabel`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-security-label.html)（原文版本：18.6；核對日期：2026-09-28）
