<a id="FUNCTIONS-STATISTICS"></a>

## 9.31. 統計資訊函式 [#](#FUNCTIONS-STATISTICS)

[9.31.1. 檢視 MCV 清單](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

<a id="id-1.5.8.37.2"></a>

PostgreSQL 提供了一個函式，用來檢視使用 `CREATE STATISTICS` 命令定義的複雜統計資訊。

<a id="FUNCTIONS-STATISTICS-MCV"></a>

### 9.31.1. 檢視 MCV 清單 [#](#FUNCTIONS-STATISTICS-MCV)

<a id="id-1.5.8.37.4.2"></a>

```

pg_mcv_list_items ( pg_mcv_list ) → setof record
```

`pg_mcv_list_items` 會回傳一組記錄，描述儲存在多欄位 MCV 清單中的所有項目。它回傳下列欄位：

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">index</code></td><td><code class="type">integer</code></td><td>項目在 <acronym class="acronym">MCV</acronym> 清單中的索引</td></tr><tr><td><code class="literal">values</code></td><td><code class="type">text[]</code></td><td>儲存在 MCV 項目中的值</td></tr><tr><td><code class="literal">nulls</code></td><td><code class="type">boolean[]</code></td><td>標識 <code class="literal">NULL</code> 值的旗標</td></tr><tr><td><code class="literal">frequency</code></td><td><code class="type">double precision</code></td><td>這個 <acronym class="acronym">MCV</acronym> 項目的頻率</td></tr><tr><td><code class="literal">base_frequency</code></td><td><code class="type">double precision</code></td><td>這個 <acronym class="acronym">MCV</acronym> 項目的基本頻率</td></tr></tbody></table>

`pg_mcv_list_items` 函式可以像這樣使用：

```

SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';
```

`pg_mcv_list` 型別的值只能從 `pg_statistic_ext_data`.`stxdmcv` 欄位取得。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-statistics.html)（原文版本：18.6；核對日期：2026-09-11）
