<a id="id-1.9.3.181.1"></a>

## TRUNCATE

TRUNCATE — 清空一個資料表或一組資料表

## 語法

```

TRUNCATE [ TABLE ] [ ONLY ] name [ * ] [, ... ]
    [ RESTART IDENTITY | CONTINUE IDENTITY ] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.181.5"></a>

## 說明

`TRUNCATE` 會快速移除一組資料表中的所有資料列。
其效果與對每個資料表執行未加條件的
`DELETE` 相同，但因為它實際上不會掃描資料表，
所以速度更快。此外，它會立即回收磁碟空間，
而不需要之後再執行一次 `VACUUM` 操作。
這在大型資料表上最為實用。

<a id="id-1.9.3.181.6"></a>

## 參數

*`name`*
:   要清空的資料表名稱（可加上結構描述限定）。
    若在資料表名稱前指定了 `ONLY`，則只會清空該資料表。
    若未指定 `ONLY`，則該資料表及其所有子系資料表（若有）
    都會被清空。也可以選擇在資料表名稱後指定 `*`，
    以明確表示包含子系資料表。

`RESTART IDENTITY`
:   自動重新啟動由被清空資料表的欄位所擁有的序列。

`CONTINUE IDENTITY`
:   不變更序列的值。這是預設行為。

`CASCADE`
:   自動清空所有對指定資料表具有外鍵參照的資料表，
    或因 `CASCADE` 而加入群組中的任何資料表。

`RESTRICT`
:   若任何資料表被未列於本指令中的資料表以外鍵參照，
    則拒絕清空。這是預設行為。

<a id="id-1.9.3.181.7"></a>

## 注意事項

必須擁有資料表的 `TRUNCATE` 權限才能清空該資料表。

`TRUNCATE` 會在其操作的每個資料表上取得
`ACCESS EXCLUSIVE` 鎖，這會阻擋該資料表上所有其他
並行操作。當指定 `RESTART IDENTITY` 時，
任何要重新啟動的序列同樣會被獨佔鎖定。
若需要對資料表進行並行存取，則應改用 `DELETE` 指令。

`TRUNCATE` 無法用於被其他資料表以外鍵參照的資料表，
除非那些資料表也在同一個指令中一併清空。在這類情況下檢查
有效性需要掃描資料表，而整個重點正是要避免這樣做。
`CASCADE` 選項可用來自動納入所有相依的資料表——
但使用這個選項時務必非常小心，否則你可能會遺失非預期要
刪除的資料！特別要注意的是，當要清空的資料表是一個分割區時，
其同層分割區不會受到影響，但串接效果會套用到所有參照的資料表
及其所有分割區，不加區分。

`TRUNCATE` 不會觸發資料表上可能存在的任何
`ON DELETE` 觸發程序，但會觸發
`ON TRUNCATE` 觸發程序。若任何資料表定義了
`ON TRUNCATE` 觸發程序，則所有
`BEFORE TRUNCATE` 觸發程序都會在清空動作發生前
全部觸發，而所有 `AFTER TRUNCATE` 觸發程序則會在
最後一次清空完成、且任何序列都已重設之後才觸發。
這些觸發程序會依照資料表被處理的順序觸發
（先是指令中列出的資料表，接著是因串接而加入的資料表）。

`TRUNCATE` 不具備 MVCC 安全性。清空之後，若並行交易使用的
是清空動作發生前所取得的快照，該資料表對這些並行交易而言
會顯示為空的。
詳情請參閱 [Section 13.6](../../the-sql-language/mvcc/mvcc-caveats.md)。

就資料表中的資料而言，`TRUNCATE` 具備交易安全性：
若周圍的交易未提交，清空動作會被安全地回復。

當指定 `RESTART IDENTITY` 時，其隱含的
`ALTER SEQUENCE RESTART` 操作同樣會以交易方式進行；
也就是說，若周圍的交易未提交，這些操作也會被回復。
請注意，若在交易回復之前，對重新啟動的序列又執行了其他
序列操作，這些操作對序列本身的效果會被回復，
但對 `currval()` 的效果不會被回復；也就是說，
交易結束後，`currval()` 仍會反映在失敗交易中
最後一次取得的序列值，即使該序列本身可能已經與此
不一致。這與失敗交易後 `currval()` 一貫的行為相似。

若外部資料包裝器支援，`TRUNCATE` 也可用於外部資料表，
例如可參閱 [postgres_fdw](../../appendixes/contrib/postgres-fdw.md)。

<a id="id-1.9.3.181.8"></a>

## 範例

清空 `bigtable` 與 `fattable` 這兩個資料表：

```

TRUNCATE bigtable, fattable;
```

同樣的操作，並同時重設任何相關聯的序列產生器：

```

TRUNCATE bigtable, fattable RESTART IDENTITY;
```

清空 `othertable` 資料表，並串接清空所有透過
外鍵限制條件參照 `othertable` 的資料表：

```

TRUNCATE othertable CASCADE;
```

<a id="id-1.9.3.181.9"></a>

## 相容性

SQL:2008 標準包含一個 `TRUNCATE` 指令，
其語法為 `TRUNCATE TABLE tablename`。
`CONTINUE IDENTITY`／`RESTART IDENTITY`
子句也出現在該標準中，但意義略有不同，且彼此相關。
本指令的部分並行行為由標準交由實作自行定義，
因此上述注意事項在必要時應與其他實作進行比對與考量。

<a id="id-1.9.3.181.10"></a>

## 參見

[DELETE](sql-delete.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-truncate.html)（原文版本：18.6；核對日期：2026-09-28）
