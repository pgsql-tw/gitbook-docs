# 41.5.5. 取得結果狀態

<a id="PLPGSQL-STATEMENTS-DIAGNOSTICS"></a>

## 41.5.5. 取得結果狀態 [#](#plpgsql-statements-diagnostics) <a href="#plpgsql-statements-diagnostics" id="plpgsql-statements-diagnostics"></a>

有好幾種方式可以判斷一個指令的效果。第一種方式是使用 `GET DIAGNOSTICS` 指令，其形式為：

```

GET [ CURRENT ] DIAGNOSTICS variable { = | := } item [ , ... ];
```

這個指令可以取得系統的狀態指標。`CURRENT` 是一個無作用的字詞（但另請參閱[第 41.6.8.1 節](../plpgsql-control-structures.md#PLPGSQL-EXCEPTION-DIAGNOSTICS)中的 `GET STACKED DIAGNOSTICS`）。每一個 *`item`* 都是一個關鍵字，用來標明要指派給指定之 *`variable`*（該變數的資料型別應該要能接收它）的狀態值。目前可用的狀態項目列於[表 41.1](#plpgsql-current-diagnostics-values)。冒號等號（`:=`）可以用來取代 SQL 標準的 `=` 語彙單元。一個例子：

```

GET DIAGNOSTICS integer_var = ROW_COUNT;
```

<a id="PLPGSQL-CURRENT-DIAGNOSTICS-VALUES"></a>

### 表 41.1. 可用的診斷資訊項目 [#](#plpgsql-current-diagnostics-values) <a href="#plpgsql-current-diagnostics-values" id="plpgsql-current-diagnostics-values"></a>

<table border="1" class="table" summary="可用的診斷資訊項目"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="varname">ROW_COUNT</code></td><td><code class="type">bigint</code></td><td>最近一個 <acronym class="acronym">SQL</acronym> 指令所處理的資料列數</td></tr><tr><td><code class="literal">PG_CONTEXT</code></td><td><code class="type">text</code></td><td>描述目前呼叫堆疊的文字行（參閱<a class="xref" href="../plpgsql-control-structures.md#plpgsql-call-stack">第 41.6.9 節</a>）</td></tr><tr><td><code class="literal">PG_ROUTINE_OID</code></td><td><code class="type">oid</code></td><td>目前函式的 OID</td></tr></tbody></table>

<br>

判斷指令效果的第二種方式，是檢查名為 `FOUND` 的特殊變數，其型別為 `boolean`。在每次 PL/pgSQL 函式呼叫中，`FOUND` 一開始是 false。它會被下列各種陳述式設定：

* `SELECT INTO` 陳述式在有資料列被指派時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。
* `PERFORM` 陳述式在產生（並捨棄）一筆以上的資料列時把 `FOUND` 設為 true，若沒有產生資料列則設為 false。
* `UPDATE`、`INSERT`、`DELETE` 與 `MERGE` 陳述式在至少有一筆資料列受影響時把 `FOUND` 設為 true，若沒有資料列受影響則設為 false。
* `FETCH` 陳述式在回傳一筆資料列時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。
* `MOVE` 陳述式在成功重新定位游標時把 `FOUND` 設為 true，否則設為 false。
* `FOR` 或 `FOREACH` 陳述式在迭代一次以上時把 `FOUND` 設為 true，否則設為 false。`FOUND` 是在迴圈離開時才這樣設定；在迴圈的執行過程中，`FOUND` 不會被該迴圈陳述式修改，不過它有可能被迴圈主體內其他陳述式的執行所改變。
* `RETURN QUERY` 與 `RETURN QUERY EXECUTE` 陳述式在查詢至少回傳一筆資料列時把 `FOUND` 設為 true，若沒有回傳資料列則設為 false。

其他的 PL/pgSQL 陳述式不會改變 `FOUND` 的狀態。特別要注意的是，`EXECUTE` 會改變 `GET DIAGNOSTICS` 的輸出，但不會改變 `FOUND`。

`FOUND` 在每個 PL/pgSQL 函式中都是一個區域變數；對它所做的任何變更都只影響目前的函式。

[返回 41.5. 基本陳述式](../plpgsql-statements.md#plpgsql-statements)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-statements.html)（原文版本：18.6；核對日期：2026-09-13）
