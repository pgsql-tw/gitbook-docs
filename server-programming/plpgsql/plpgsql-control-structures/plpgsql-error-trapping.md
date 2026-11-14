# 41.6.8. 捕捉錯誤

<a id="PLPGSQL-ERROR-TRAPPING"></a>

## 41.6.8. 捕捉錯誤 [#](#plpgsql-error-trapping) <a href="#plpgsql-error-trapping" id="plpgsql-error-trapping"></a>

<a id="id-1.8.8.8.10.2"></a>

在預設情況下，PL/pgSQL 函式中發生的任何錯誤都會中止該函式以及外圍交易的執行。你可以使用帶有 `EXCEPTION` 子句的 `BEGIN` 區塊來捕捉錯誤並從中復原。其語法是 `BEGIN` 區塊一般語法的延伸：

```

[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
EXCEPTION
    WHEN condition [ OR condition ... ] THEN
        handler_statements
    [ WHEN condition [ OR condition ... ] THEN
          handler_statements
      ... ]
END;
```

如果沒有發生錯誤，這種形式的區塊就只是執行所有的 *`statements`*，然後控制流程轉移到 `END` 之後的下一個陳述式。但如果在這些 *`statements`* 之中發生錯誤，對 *`statements`* 的後續處理就會被放棄，控制流程轉移到 `EXCEPTION` 清單。系統會在該清單中尋找第一個與所發生之錯誤相符的 *`condition`*。如果找到相符者，就執行對應的 *`handler_statements`*，然後控制流程轉移到 `END` 之後的下一個陳述式。如果沒有找到相符者，錯誤就會向外傳播，彷彿 `EXCEPTION` 子句根本不存在一般：該錯誤可以被外圍帶有 `EXCEPTION` 的區塊捕捉，如果沒有這樣的區塊，它就會中止該函式的處理。

*`condition`* 名稱可以是 [附錄 A](../../../appendixes/errcodes-appendix/README.md) 中所列出的任何一個。類別名稱會與其類別之內的任何錯誤相符。特殊的條件名稱 `OTHERS` 會與除了 `QUERY_CANCELED` 與 `ASSERT_FAILURE` 以外的每一種錯誤型別相符。（要依名稱捕捉那兩種錯誤型別是可行的，但通常並不明智。）條件名稱不區分大小寫。此外，錯誤條件也可以用 `SQLSTATE` 碼來指定；例如下列兩者是等價的：

```

WHEN division_by_zero THEN ...
WHEN SQLSTATE '22012' THEN ...
```

如果在所選定的 *`handler_statements`* 之中發生新的錯誤，它無法被這個 `EXCEPTION` 子句捕捉，而是會向外傳播。外圍的 `EXCEPTION` 子句則有可能捕捉到它。

當錯誤被 `EXCEPTION` 子句捕捉時，PL/pgSQL 函式的區域變數會維持在錯誤發生當下的狀態，但是該區塊之內對持續性資料庫狀態所做的所有變更都會被回復。舉例來說，考慮下面這段程式片段：

```

INSERT INTO mytab(firstname, lastname) VALUES('Tom', 'Jones');
BEGIN
    UPDATE mytab SET firstname = 'Joe' WHERE lastname = 'Jones';
    x := x + 1;
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'caught division_by_zero';
        RETURN x;
END;
```

當控制流程走到對 `y` 的指派時，它會以 `division_by_zero` 錯誤失敗。這個錯誤會被 `EXCEPTION` 子句捕捉。`RETURN` 陳述式所回傳的值會是遞增之後的 `x` 值，但是 `UPDATE` 指令的效果則已經被回復。不過，位於該區塊之前的 `INSERT` 指令並不會被回復，所以最終的結果是資料庫中存放的是 `Tom Jones` 而不是 `Joe Jones`。

### 提示

含有 `EXCEPTION` 子句的區塊，其進入與離開的成本明顯高於沒有該子句的區塊。因此，不要在沒有必要時使用 `EXCEPTION`。

<a id="PLPGSQL-UPSERT-EXAMPLE"></a>

**範例 41.2. 搭配 `UPDATE`/`INSERT` 的例外處理**

這個範例使用例外處理，視情況執行 `UPDATE` 或 `INSERT`。建議應用程式使用帶有 `ON CONFLICT DO UPDATE` 的 `INSERT`，而不要真的採用這種模式。這個範例的主要用意是示範 PL/pgSQL 控制流程結構的用法：

```

CREATE TABLE db (a INT PRIMARY KEY, b TEXT);

CREATE FUNCTION merge_db(key INT, data TEXT) RETURNS VOID AS
$$
BEGIN
    LOOP
        -- first try to update the key
        UPDATE db SET b = data WHERE a = key;
        IF found THEN
            RETURN;
        END IF;
        -- not there, so try to insert the key
        -- if someone else inserts the same key concurrently,
        -- we could get a unique-key failure
        BEGIN
            INSERT INTO db(a,b) VALUES (key, data);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

SELECT merge_db(1, 'david');
SELECT merge_db(1, 'dennis');
```

這段程式碼假設 `unique_violation` 錯誤是由該 `INSERT` 所造成，而不是由例如該資料表上某個觸發程序函式中的 `INSERT` 所造成。如果該資料表上有一個以上的唯一值索引，它也可能會有不正確的行為，因為不論錯誤是由哪一個索引所引起，它都會重試該操作。若使用接下來要討論的功能來檢查所捕捉到的錯誤是否就是所預期的那一個，就能得到更高的安全性。

<br><a id="PLPGSQL-EXCEPTION-DIAGNOSTICS"></a>

### 41.6.8.1. 取得錯誤的相關資訊 [#](#plpgsql-exception-diagnostics) <a href="#plpgsql-exception-diagnostics" id="plpgsql-exception-diagnostics"></a>

例外處理常式經常需要識別發生的特定錯誤。在 PL/pgSQL 中有兩種方式可以取得目前例外的相關資訊：特殊變數，以及 `GET STACKED DIAGNOSTICS` 指令。

在例外處理常式之內，特殊變數 `SQLSTATE` 含有對應於所拋出之例外的錯誤碼（可能的錯誤碼清單請參閱 [表 A.1](../../../appendixes/errcodes-appendix/README.md#errcodes-table)）。特殊變數 `SQLERRM` 則含有與該例外相關聯的錯誤訊息。這些變數在例外處理常式之外是未定義的。

在例外處理常式之內，也可以使用 `GET STACKED DIAGNOSTICS` 指令取得目前例外的相關資訊，其形式為：

```

GET STACKED DIAGNOSTICS variable { = | := } item [ , ... ];
```

每一個 *`item`* 都是一個關鍵字，用以指出要指派給指定之 *`variable`*（其資料型別應該要能接收該值）的狀態值。目前可用的狀態項目列於 [表 41.2](#plpgsql-exception-diagnostics-values)。

<a id="PLPGSQL-EXCEPTION-DIAGNOSTICS-VALUES"></a>

### 表 41.2. 錯誤診斷資訊項目 [#](#plpgsql-exception-diagnostics-values) <a href="#plpgsql-exception-diagnostics-values" id="plpgsql-exception-diagnostics-values"></a>

<table border="1" class="table" summary="錯誤診斷資訊項目"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">RETURNED_SQLSTATE</code></td><td><code class="type">text</code></td><td>該例外的 SQLSTATE 錯誤碼</td></tr><tr><td><code class="literal">COLUMN_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之欄位的名稱</td></tr><tr><td><code class="literal">CONSTRAINT_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之限制條件的名稱</td></tr><tr><td><code class="literal">PG_DATATYPE_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之資料型別的名稱</td></tr><tr><td><code class="literal">MESSAGE_TEXT</code></td><td><code class="type">text</code></td><td>該例外主要訊息的文字內容</td></tr><tr><td><code class="literal">TABLE_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之資料表的名稱</td></tr><tr><td><code class="literal">SCHEMA_NAME</code></td><td><code class="type">text</code></td><td>與例外相關之綱要的名稱</td></tr><tr><td><code class="literal">PG_EXCEPTION_DETAIL</code></td><td><code class="type">text</code></td><td>該例外詳細訊息的文字內容（若有的話）</td></tr><tr><td><code class="literal">PG_EXCEPTION_HINT</code></td><td><code class="type">text</code></td><td>該例外提示訊息的文字內容（若有的話）</td></tr><tr><td><code class="literal">PG_EXCEPTION_CONTEXT</code></td><td><code class="type">text</code></td><td>描述例外發生當時之呼叫堆疊的文字行（見 <a class="xref" href="../plpgsql-control-structures.md#plpgsql-call-stack">第 41.6.9 節</a>）</td></tr></tbody></table>

<br>

如果該例外並未為某個項目設定值，回傳的就會是空字串。

以下是一個範例：

```

DECLARE
  text_var1 text;
  text_var2 text;
  text_var3 text;
BEGIN
  -- some processing which might cause an exception
  ...
EXCEPTION WHEN OTHERS THEN
  GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
                          text_var2 = PG_EXCEPTION_DETAIL,
                          text_var3 = PG_EXCEPTION_HINT;
END;
```

<a id="PLPGSQL-CALL-STACK"></a>

[返回 41.6. 控制結構](../plpgsql-control-structures.md#plpgsql-control-structures)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-control-structures.html)（原文版本：18.6；核對日期：2026-09-24）
