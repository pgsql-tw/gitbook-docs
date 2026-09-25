<a id="JIT-DECISION"></a>

## 30.2. 何時該使用 JIT？ [#](#JIT-DECISION)

JIT 編譯主要對長時間執行、CPU 密集型的查詢有益。
這類查詢通常是分析型查詢。對於短查詢而言，
執行 JIT 編譯所增加的額外負擔，往往會高於它所能節省的時間。

為判斷是否應使用 JIT 編譯，
系統會使用該查詢的總估計成本（參見
[第 69 章](../../internals/planner-stats-details/README.md) 與
[第 19.7.2 節](../runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)）。
該查詢的估計成本會與 [jit_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-ABOVE-COST) 的設定值進行比較。若成本較高，
就會執行 JIT 編譯。
接著還需要再做兩項決定。
首先，若估計成本高
於 [jit_inline_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST) 的設定值，查詢中使用的短
函式與運算子就會被內嵌。
其次，若估計成本高於 [jit_optimize_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST) 的設定值，就會套用成本較高的最佳化以
改善產生的程式碼。
這些選項各自都會增加 JIT 編譯的額外負擔，
但能大幅縮短查詢執行時間。

這些基於成本的決策會在規劃期（plan time）做出，而非執行期。
這代表當使用預備陳述式（prepared statement），並採用通用計畫（generic plan，參見 [PREPARE](../../reference/sql-commands/sql-prepare.md)）時，
控制這些決策的是預備（prepare）當下生效的組態參數值，
而不是執行時的設定值。

### 注意

若 [jit](../runtime-config/runtime-config-query.md#GUC-JIT) 設為 `off`，或沒有可用的
JIT 實作（例如因為
伺服器編譯時未加上 `--with-llvm`），
即使依上述準則判斷會有效益，仍不會執行 JIT。將 [jit](../runtime-config/runtime-config-query.md#GUC-JIT)
設為 `off`，在規劃期與執行期都會產生效果。

可以使用 [EXPLAIN](../../reference/sql-commands/sql-explain.md) 來查看是否使用了
JIT。舉例來說，以下是一個未使用
JIT 的查詢：

```

=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=0.303..0.303 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.017..0.111 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.116 ms
 Execution Time: 0.365 ms
```

考量到該計畫的成本，完全沒有使用
JIT 是合理的；使用 JIT 的成本會
大於它所能帶來的潛在節省。調整成本門檻
就會促使系統使用 JIT：

```

=# SET jit_above_cost = 10;
SET
=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=6.049..6.049 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.019..0.052 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.133 ms
 JIT:
   Functions: 3
   Options: Inlining false, Optimization false, Expressions true, Deforming true
   Timing: Generation 1.259 ms (Deform 0.000 ms), Inlining 0.000 ms, Optimization 0.797 ms, Emission 5.048 ms, Total 7.104 ms
 Execution Time: 7.416 ms
```

如上所示，這次使用了 JIT，但沒有進行內嵌與
高成本的最佳化。若也調低 [jit_inline_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST) 或 [jit_optimize_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST)，
情況就會改變。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-decision.html)（原文版本：18.6；核對日期：2026-09-25）
