<a id="id-1.11.7.21.10.1"></a>

## dblink

dblink — 在遠端資料庫執行查詢

## 語法

```

dblink(text connname, text sql [, bool fail_on_error]) returns setof record
dblink(text connstr, text sql [, bool fail_on_error]) returns setof record
dblink(text sql [, bool fail_on_error]) returns setof record
```

<a id="id-1.11.7.21.10.5"></a>

## 說明

`dblink` 在遠端資料庫執行查詢（通常為 `SELECT`，但也可以是任何會傳回資料列的 SQL 陳述式）。

提供兩個 `text` 引數時，會先將第一個引數查找為持續連線的名稱；若找到，
便在該連線上執行命令。若找不到，第一個引數會如同 `dblink_connect` 一樣
視為連線資訊字串，並且僅在執行此命令期間建立指定的連線。

<a id="id-1.11.7.21.10.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱；省略此引數時使用未命名連線。

*`connstr`*
:   連線資訊字串，如 `dblink_connect` 先前所述。

*`sql`*
:   要在遠端資料庫執行的 SQL 查詢，例如 `select * from foo`。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本端引發
    錯誤。若為 false，遠端錯誤會在本端以 NOTICE 回報，且此函式不傳回
    資料列。

<a id="id-1.11.7.21.10.7"></a>

## 傳回值

此函式傳回查詢產生的資料列。由於 `dblink` 可以搭配任何查詢使用，
因此它宣告傳回 `record`，而非指定特定的欄位集合。這表示你必須在呼叫
查詢中指定預期的欄位集合，否則 PostgreSQL 不知道應預期什麼。範例如下：

```

SELECT *
    FROM dblink('dbname=mydb options=-csearch_path=',
                'select proname, prosrc from pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

`FROM` 子句的「別名」部分必須指定函式將傳回的欄位名稱及型別。（在別名中
指定欄位名稱其實是標準 SQL 語法，但指定欄位型別是 PostgreSQL 的擴充。）
這讓系統在嘗試執行函式前，能瞭解 `*` 應展開為何者，以及 `WHERE` 子句中
的 `proname` 指涉何者。執行時，若遠端資料庫的實際查詢結果不具有 `FROM`
子句所列的相同欄位數，便會引發錯誤。不過欄位名稱不必相符，`dblink` 也不
要求型別完全相符；只要傳回的資料字串是 `FROM` 子句所宣告欄位型別的有效輸入，
就會成功。

<a id="id-1.11.7.21.10.8"></a>

## 注意事項

若要將 `dblink` 搭配預先確定的查詢使用，方便的方法是建立檢視表。這可將
欄位型別資訊隱藏在檢視表中，而不必在每個查詢中明確寫出。例如：

```

CREATE VIEW myremote_pg_proc AS
  SELECT *
    FROM dblink('dbname=postgres options=-csearch_path=',
                'select proname, prosrc from pg_proc')
    AS t1(proname name, prosrc text);

SELECT * FROM myremote_pg_proc WHERE proname LIKE 'bytea%';
```

<a id="id-1.11.7.21.10.9"></a>

## 範例

```

SELECT * FROM dblink('dbname=postgres options=-csearch_path=',
                     'select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteain    | byteain
 byteaout   | byteaout
(12 rows)

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteain    | byteain
 byteaout   | byteaout
(12 rows)

SELECT dblink_connect('myconn', 'dbname=regression options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('myconn', 'select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 bytearecv  | bytearecv
 byteasend  | byteasend
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteain    | byteain
 byteaout   | byteaout
(14 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-function.html)
