# TRUNCATE

TRUNCATE — 清空一個資料表或一堆資料表

### 語法

```text
TRUNCATE [ TABLE ] [ ONLY ] name [ * ] [, ... ]
    [ RESTART IDENTITY | CONTINUE IDENTITY ] [ CASCADE | RESTRICT ]
```

### 說明

TRUNCATE 快速移除一堆資料表中的所有資料列。它與每個資料表上的無差別 DELETE 具有相同的效果，但由於它實際上不掃描資料表，因此速度更快。此外，它會立即回收磁碟空間，而不是需要後續的 VACUUM 操作。這對大型資料表非常有用。

### 參數

_`name`_

要清空的資料表名稱（可選用綱要名稱）。如果在資料表名稱之前指定了 ONLY，則僅清空此資料表。如果未指定 ONLY，則會清空此表及其所有後代資料表（如果有的話）。也可以在資料表名稱後指定 \* 以明確指示包含後代資料表。

`RESTART IDENTITY`

自動重置清空資料表的欄位所擁有的序列。

`CONTINUE IDENTITY`

不要變更序列的值。這是預設值。

`CASCADE`

自動清空所有對任何對此資料表具有外部鍵引用的資料表，或者由於 CASCADE 而加入群組的資料表。

`RESTRICT`

如果任何資料表具有未在命令中列出的資料表外部鍵引用，則拒絕清空。這是預設值。

### 注意

您必須對資料具有 TRUNCATE 權限才能以 TRUNCATE 清空它。

TRUNCATE 會在其執行的每個資料表上取得一個 ACCESS EXCLUSIVE 鎖定，它阻止資料表上的所有其他同時間的操作。指定 RESTART IDENTITY 時，任何要重置的序列同樣都是獨占鎖定的。如果需要對資料表進行同時間的存取，則應使用 DELETE 指令。

TRUNCATE 不能用於具有其他資料表外部鍵引用的資料表，除非所有這些資料表也在同一指令中被清空。在這種情況下檢查其有效性將需要資料表掃描，掃描點不一定只有一個。CASCADE 選項可用於自動包含所有相關資料表 - 但在使用此選項時要非常小心，否則您可能會失去您不想要失去的資料！

TRUNCATE 不會觸發資料表可能存在的任何 ON DELETE 觸發器。但它將觸發 TRUNCATE 觸發器。如果為任何資料表定義了 ON TRUNCATE 觸發器，則在發生任何清空之前觸發所有 BEFORE TRUNCATE 觸發器，並在執行最後一次清空且重置任何序列之後觸發所有 AFTER TRUNCATE 觸發器。觸發器將按照要處理的資料表順序觸發（首先是指令中列出的那些，然後是由於串聯處理而添加的資料表）。

TRUNCATE 並不是 MVCC 安全的。清空後，如果資料表使用在清空發生之前所産生的快照，則資料表對於平行執行的事務將顯示為空。更多詳細訊息，請參閱[第 13.5 節](../../the-sql-language/concurrency-control/13.5.-te-bie-zhu-yi.md)。

TRUNCATE 對於資料表中的資料是事務安全的：如果其他的事務沒有提交，則 TRUNCATE 將能安全地回溯。

指定 RESTART IDENTITY 時，隱含的 ALTER SEQUENCE RESTART 操作也會以事務方式完成；也就是說，如果其他的事務沒有提交，它們將被回溯。這與 ALTER SEQUENCE RESTART 的正常行為不同。請注意，如果在事務回溯之前對重置的序列執行任何其他序列操作，則會回溯這些操作對序列的影響，但不會影響它們對 currval\(\) 的影響。也就是說，事務 currval\(\) 將繼續反映失敗事務中獲得的最後一個序列值，即使序列本身可能不再與之一致。 這類似於事務失敗後 currval\(\) 的通常行為。

外部資料表目前不支援 TRUNCATE。這意味著如果指定的資料表具有任何外部的後代資料表，則此指令將會失敗。

### 範例

清空資料表 bigtable 和 fattable：

```text
TRUNCATE bigtable, fattable;
```

同樣，再加上重置任何相關的序列産生器：

```text
TRUNCATE bigtable, fattable RESTART IDENTITY;
```

清空資料表 othertable，串聯清空任何透過外部鍵引用的其他資料表：

```text
TRUNCATE othertable CASCADE;
```

### 相容性

SQL:2008 標準有一個 TRUNCATE 指令，其語法為 TRUNCATE TABLE tablename。子句 CONTINUE IDENTITY / RESTART IDENTITY 也出現在該標準中，但具有略微不同但類似的意義。此指令的某些平行作業行為是由實作定義的，因此應考慮上述註釋，並在必要時與其他實作進行比較。

### 參閱

[DELETE](delete.md)

