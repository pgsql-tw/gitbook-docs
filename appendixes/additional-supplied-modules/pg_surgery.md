<a id="PGSURGERY"></a>

# F.34. pg_surgery

[F.34.1. 函式](#id-1.11.7.43.4)

[F.34.2. 作者](#id-1.11.7.43.5)

<a id="id-1.11.7.43.2"></a>

`pg_surgery` 模組提供多種函式，可對受損的關聯進行修復。這些函式在設計上並不安全，使用它們可能損壞（或進一步損壞）資料庫。例如，這些函式很容易使資料表與自身索引不一致、造成 `UNIQUE` 或 `FOREIGN KEY` 限制條件違規，甚至讓讀取時會造成資料庫伺服器當機的資料列變得可見。只能極度謹慎地使用它們，並且僅能作為最後手段。

<a id="id-1.11.7.43.4"></a>

## F.34.1. 函式

`heap_force_kill(regclass, tid[]) returns void`

`heap_force_kill` 不檢查資料列內容，便將「已使用」的行指標標記為「已死亡」。此函式的用途是強制移除無法透過其他方式存取的資料列。例如：

```

test=> select * from t1 where ctid = '(0, 1)';
ERROR:  could not access status of transaction 4007513275
DETAIL:  Could not open file "pg_xact/0EED": No such file or directory.

test=# select heap_force_kill('t1'::regclass, ARRAY['(0, 1)']::tid[]);
 heap_force_kill
-----------------

(1 row)

test=# select * from t1 where ctid = '(0, 1)';
(0 rows)
```

`heap_force_freeze(regclass, tid[]) returns void`

`heap_force_freeze` 不檢查資料列內容，便將資料列標記為已凍結。此函式的用途是讓因可見性資訊損壞而無法存取的資料列得以存取，或讓因可見性資訊損壞而無法成功執行清理的資料表得以清理。例如：

```

test=> vacuum t1;
ERROR:  found xmin 507 from before relfrozenxid 515
CONTEXT:  while scanning block 0 of relation "public.t1"

test=# select ctid from t1 where xmin = 507;
 ctid
-------
 (0,3)
(1 row)

test=# select heap_force_freeze('t1'::regclass, ARRAY['(0, 3)']::tid[]);
 heap_force_freeze
-------------------

(1 row)

test=# select ctid from t1 where xmin = 2;
 ctid
-------
 (0,3)
(1 row)
```

<a id="id-1.11.7.43.5"></a>

## F.34.2. 作者

Ashutosh Sharma <code class="email">&lt;<a class="email" href="mailto:ashu.coek88@gmail.com">ashu.coek88@gmail.com</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/pgsurgery.html)
