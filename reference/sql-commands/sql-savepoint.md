<a id="id-1.9.3.170.1"></a><a id="id-1.9.3.170.2"></a>

## SAVEPOINT

SAVEPOINT — 在目前交易中定義一個新的儲存點

## 語法

```

SAVEPOINT savepoint_name
```

<a id="id-1.9.3.170.6"></a>

## 說明

`SAVEPOINT` 會在目前交易中建立一個新的儲存點。

儲存點是交易內的一個特殊標記，讓在建立之後執行的所有命令
都能被回復，將交易狀態還原成建立該儲存點時的狀態。

<a id="id-1.9.3.170.7"></a>

## 參數

*`savepoint_name`*
:   要賦予新儲存點的名稱。若已存在同名的儲存點，
    在較新的同名儲存點被釋放之前，這些同名儲存點都將無法存取。

<a id="id-1.9.3.170.8"></a>

## 注意事項

使用 [`ROLLBACK TO`](sql-rollback-to.md) 可回復到某個儲存點。使用
[`RELEASE SAVEPOINT`](sql-release-savepoint.md)
可銷毀某個儲存點，同時保留該儲存點建立之後所執行命令的效果。

儲存點只能在交易區塊內建立。一個交易內可以定義多個儲存點。

<a id="id-1.9.3.170.9"></a>

## 範例

建立一個儲存點，之後再復原自其建立以來所有命令的效果：

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    ROLLBACK TO SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);
COMMIT;
```

上述交易會插入 1 與 3，但不會插入 2。

建立一個儲存點，之後再將其銷毀：

```

BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

上述交易會插入 3 與 4 兩者。

使用單一儲存點名稱：

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);

    -- rollback to the second savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows rows 1 and 2

    -- release the second savepoint
    RELEASE SAVEPOINT my_savepoint;

    -- rollback to the first savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows only row 1
COMMIT;
```

上述交易顯示值為 3 的資料列先被回復，接著值為 2 的資料列也被回復。

<a id="id-1.9.3.170.10"></a>

## 相容性

SQL 標準要求當另一個同名的儲存點被建立時，原本的儲存點必須自動銷毀。
在 PostgreSQL 中，舊的儲存點會被保留，只是在回復或釋放時只會用到
較新的那一個。（以 `RELEASE SAVEPOINT` 釋放較新的儲存點後，
較舊的儲存點就會再次可供 `ROLLBACK TO SAVEPOINT` 與
`RELEASE SAVEPOINT` 使用。）除此之外，`SAVEPOINT`
完全符合 SQL 標準。

<a id="id-1.9.3.170.11"></a>

## 另請參閱

[BEGIN](sql-begin.md)、[COMMIT](sql-commit.md)、[RELEASE SAVEPOINT](sql-release-savepoint.md)、[ROLLBACK](sql-rollback.md)、[ROLLBACK TO SAVEPOINT](sql-rollback-to.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-savepoint.html)（原文版本：18.6；核對日期：2026-09-28）
