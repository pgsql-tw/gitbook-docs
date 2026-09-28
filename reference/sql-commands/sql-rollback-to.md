<a id="id-1.9.3.169.1"></a><a id="id-1.9.3.169.2"></a>

## ROLLBACK TO SAVEPOINT

ROLLBACK TO SAVEPOINT — 回復到某個儲存點

## 語法

```

ROLLBACK [ WORK | TRANSACTION ] TO [ SAVEPOINT ] savepoint_name
```

<a id="id-1.9.3.169.6"></a>

## 說明

回復自建立該儲存點之後所執行的所有指令，然後在相同的交易層級啟動一個新的子交易。
該儲存點本身仍然有效，之後如有需要，仍可再次回復到它。

`ROLLBACK TO SAVEPOINT` 會隱含地摧毀所有在指定儲存點之後
建立的儲存點。

<a id="id-1.9.3.169.7"></a>

## 參數

*`savepoint_name`*
:   要回復到的儲存點。

<a id="id-1.9.3.169.8"></a>

## 注意

請使用 [`RELEASE SAVEPOINT`](sql-release-savepoint.md) 來摧毀一個儲存點，
但不捨棄該儲存點建立之後所執行指令的效果。

指定一個尚未建立過的儲存點名稱會導致錯誤。

游標相對於儲存點而言，有一些非交易性的行為。任何在某個儲存點內開啟的游標，都會在該儲存點被回復時關閉。如果先前已開啟的游標，在某個之後被回復的儲存點內，受到
`FETCH` 或 `MOVE` 指令的影響，該游標會停留在
`FETCH` 使其指向的位置（也就是說，由
`FETCH` 造成的游標移動不會被回復）。
關閉游標也同樣不會因回復而被撤銷。
然而，由該游標的查詢所造成的其他副作用（例如該查詢所呼叫之易變函式的副作用），如果是發生在之後被回復的儲存點期間，則*會*被回復。
一個執行過程中導致交易中止的游標，會進入無法執行的狀態，因此雖然可以用
`ROLLBACK TO SAVEPOINT` 還原該交易，該游標本身卻無法再被使用。

<a id="id-1.9.3.169.9"></a>

## 範例

撤銷在建立 `my_savepoint`
之後所執行指令的效果：

```

ROLLBACK TO SAVEPOINT my_savepoint;
```

游標位置不會受到儲存點回復的影響：

```

BEGIN;

DECLARE foo CURSOR FOR SELECT 1 UNION SELECT 2;

SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        1

ROLLBACK TO SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        2

COMMIT;
```

<a id="id-1.9.3.169.10"></a>

## 相容性

SQL 標準規定
`SAVEPOINT` 關鍵字是必要的，但 PostgreSQL
與 Oracle 都允許將它省略。SQL 只允許在
`ROLLBACK` 之後使用 `WORK`，不允許使用
`TRANSACTION` 作為贅詞。此外，SQL 還有一個選用子句
`AND [ NO ] CHAIN`，PostgreSQL 目前並不支援。除此之外，此指令都符合
SQL 標準。

<a id="id-1.9.3.169.11"></a>

## 另請參閱

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [RELEASE SAVEPOINT](sql-release-savepoint.md), [ROLLBACK](sql-rollback.md), [SAVEPOINT](sql-savepoint.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-rollback-to.html)（原文版本：18.6；核對日期：2026-09-28）
