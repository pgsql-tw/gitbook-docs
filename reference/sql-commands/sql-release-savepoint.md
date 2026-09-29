<a id="id-1.9.3.164.1"></a><a id="id-1.9.3.164.2"></a>

## RELEASE SAVEPOINT

RELEASE SAVEPOINT — 釋放先前定義的一個儲存點

## 語法

```

RELEASE [ SAVEPOINT ] savepoint_name
```

<a id="id-1.9.3.164.6"></a>

## 說明

`RELEASE SAVEPOINT` 會釋放指定名稱的儲存點，以及在此儲存點之後建立的所有有效儲存點，並釋放它們所佔用的資源。自建立該儲存點以來所做的所有變更，只要尚未被回復，都會併入建立該儲存點當時有效的交易或儲存點中。在
`RELEASE SAVEPOINT` 之後所做的變更，也同樣會屬於這個有效的交易或儲存點。

<a id="id-1.9.3.164.7"></a>

## 參數

*`savepoint_name`*
:   要釋放的儲存點名稱。

<a id="id-1.9.3.164.8"></a>

## 注意

指定一個先前未定義過的儲存點名稱會導致錯誤。

當交易處於中止狀態時，無法釋放儲存點；若要進行這種操作，請使用 [ROLLBACK TO SAVEPOINT](sql-rollback-to.md)。

如果有多個儲存點使用相同名稱，只有最近定義、尚未被釋放的那一個會被釋放。重複執行此指令，會依序釋放較舊的儲存點。

<a id="id-1.9.3.164.9"></a>

## 範例

建立並在稍後釋放一個儲存點：

```

BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

上述交易會插入 3 與 4 這兩個值。

以下是一個包含多層巢狀子交易的較複雜範例：

```

BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT sp1;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT sp2;
    INSERT INTO table1 VALUES (3);
    RELEASE SAVEPOINT sp2;
    INSERT INTO table1 VALUES (4))); -- generates an error
```

在這個範例中，應用程式要求釋放插入了 3 的儲存點
`sp2`。這會將該次插入的交易上下文變更為
`sp1`。當嘗試插入值 4 的陳述式產生錯誤時，2 與
4 的插入都會遺失，因為它們同屬於這個現已被回復的儲存點，而值 3 則已併入同一個（sp1）交易上下文。此時應用程式只能從以下兩個指令中選擇一個，因為其他所有指令都會被忽略：

```

ROLLBACK;
ROLLBACK TO SAVEPOINT sp1;
```

選擇 `ROLLBACK` 會中止所有內容，包括值
1；而 `ROLLBACK TO SAVEPOINT sp1` 則會保留
值 1，並讓交易得以繼續。

<a id="id-1.9.3.164.10"></a>

## 相容性

此指令符合 SQL 標準。標準規定
`SAVEPOINT` 關鍵字是必要的，但 PostgreSQL 允許
將它省略。

<a id="id-1.9.3.164.11"></a>

## 另請參閱

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md), [ROLLBACK TO SAVEPOINT](sql-rollback-to.md), [SAVEPOINT](sql-savepoint.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-release-savepoint.html)（原文版本：18.6；核對日期：2026-09-28）
