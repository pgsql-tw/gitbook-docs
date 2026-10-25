<a id="LIBPQ-EXEC-NONSELECT"></a>

## 32.3.3. 取得其他結果資訊 [#](#libpq-exec-nonselect) <a href="#libpq-exec-nonselect" id="libpq-exec-nonselect"></a>

這些函式用來從 `PGresult` 物件中擷取其他資訊。

<a id="LIBPQ-PQCMDSTATUS"></a>

### `PQcmdStatus`<a id="id-1.7.3.10.5.3.1.1.2"></a> [#](#libpq-pqcmdstatus) <a href="#libpq-pqcmdstatus" id="libpq-pqcmdstatus"></a>

傳回產生該 `PGresult` 之 SQL 命令的命令狀態標籤。

```

    char *PQcmdStatus(PGresult *res);
```

通常這只是命令的名稱，但也可能包含額外的資料，例如處理的資料列數。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec-main.md#libpq-pqclear) 時，它就會被釋放。

<a id="LIBPQ-PQCMDTUPLES"></a>

### `PQcmdTuples`<a id="id-1.7.3.10.5.3.2.1.2"></a> [#](#libpq-pqcmdtuples) <a href="#libpq-pqcmdtuples" id="libpq-pqcmdtuples"></a>

傳回受該 SQL 命令影響的資料列數。

```

    char *PQcmdTuples(PGresult *res);
```

此函式傳回一個字串，內容為受產生該 `PGresult` 之 SQL 陳述式影響的資料列數。此函式只能在執行 `SELECT`、`CREATE TABLE AS`、`INSERT`、`UPDATE`、`DELETE`、`MERGE`、`MOVE`、`FETCH` 或 `COPY` 陳述式之後，或是以 `EXECUTE` 執行包含 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 陳述式的預備查詢之後使用。若產生該 `PGresult` 的是其他任何命令，[`PQcmdTuples`](libpq-exec-nonselect.md#libpq-pqcmdtuples) 會傳回空字串。呼叫者不應直接釋放此傳回值。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec-main.md#libpq-pqclear) 時，它就會被釋放。

<a id="LIBPQ-PQOIDVALUE"></a>

### `PQoidValue`<a id="id-1.7.3.10.5.3.3.1.2"></a> [#](#libpq-pqoidvalue) <a href="#libpq-pqoidvalue" id="libpq-pqoidvalue"></a>

若該 SQL 命令是將恰好一筆資料列插入具有 OID 之資料表的 `INSERT`，或是以 `EXECUTE` 執行包含適當 `INSERT` 陳述式的預備查詢，則傳回所插入資料列的 OID<a id="id-1.7.3.10.5.3.3.2.1.1"></a>。否則，此函式傳回 `InvalidOid`。若受 `INSERT` 陳述式影響的資料表不包含 OID，此函式也會傳回 `InvalidOid`。

```

    Oid PQoidValue(const PGresult *res);
```

<a id="LIBPQ-PQOIDSTATUS"></a>

### `PQoidStatus`<a id="id-1.7.3.10.5.3.4.1.2"></a> [#](#libpq-pqoidstatus) <a href="#libpq-pqoidstatus" id="libpq-pqoidstatus"></a>

此函式已不建議使用，請改用 [`PQoidValue`](libpq-exec-nonselect.md#libpq-pqoidvalue)，而且它並非執行緒安全。它傳回含有所插入資料列 OID 的字串，而 [`PQoidValue`](libpq-exec-nonselect.md#libpq-pqoidvalue) 則傳回 OID 值。

```

    char *PQoidStatus(const PGresult *res);
```


[返回 32.3. 命令執行函式](libpq-exec.md#libpq-exec)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-exec.html)（原文版本：18.6；核對日期：2026-10-18）
