# SET TRANSACTION

SET TRANSACTION — 設定目前交易事務的模式

## 語法

```text
SET TRANSACTION transaction_mode [, ...]
SET TRANSACTION SNAPSHOT snapshot_id
SET SESSION CHARACTERISTICS AS TRANSACTION transaction_mode [, ...]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

## 說明

SET TRANSACTION 指令設定目前交易事務的模式。它對任何後續的交易都沒有影響。SET SESSION CHARACTERISTICS 設定連線後續交易事務的預設的交易模式。 對於單個交易，這些預設值可以由 SET TRANSACTION 所覆寫。

可用的事務模式是事務隔離級別、事務存取模式（讀/寫或唯讀）以及可延遲模式。另外，可以選擇一個快照，但僅限於目前事務，而不是連線預設值。

事務的隔離級別確定了其他事務同時運行時事務可以看到的資料：

`READ COMMITTED`

一個查詢語句只能看到在它開始之前已確認提交的資料。這是預設的模式。

`REPEATABLE READ`

目前事務中的所有語句只能看到在此事務中執行第一個查詢或資料修改語句之前已提交的資料。

`SERIALIZABLE`

目前事務中的所有語句只能看到在此事務中執行第一個查詢或資料修改語句之前已提交的資料。如果在平行可序列化事務之間的讀寫模式會產生對於這些事務的任何串接（一次一個）執行都不可能發生的情況，則其中一個將被退回並帶有 serialization\_failure 錯誤。

SQL 標準定義了另一個等級 READ UNCOMMITTED。在 PostgreSQL 中，READ UNCOMMITTED 被視為 READ COMMITTED。

事務的第一個查詢或資料修改語句（SELECT、INSERT、DELETE、UPDATE、FETCH 或 COPY）已執行後，事務隔離等級就不能再更改。有關事務隔離和同時一致性控制的更多訊息，請參閱[第 13 章](../../ii.-sql-cha-xun-yu-yan/13.-yi-zhi-xing-guan-li-mvcc/)。

事務存取模式會決定該事務是讀/寫還是唯讀。讀/寫是預設值。如果事務處於唯讀狀態，則不允許執行以下的 SQL 命令：INSERT、UPDATE、DELETE 和 COPY FROM，除非它們要寫入的資料表是臨時資料表；還有所有的 CREATE、ALTER 和 DROP命令；COMMENT、GRANT、REVOKE、TRUNCATE；以及 EXPLAIN ANALYZE 和 EXECUTE，如果它們執行的命令在以上列出的命令之中的。這是一個高等級的唯讀概念，它不會阻止所有寫入磁碟的行為。

除非事務是 SERIALIZABLE 和 READ ONLY，否則 DEFERRABLE 事務屬性不會起作用。當為事務選擇這三個屬性時，事務可能會在第一次取得其快照時阻隔，之後它就可以在沒有 SERIALIZABLE 事務的正常開銷的情況下執行，並且沒有任何串接化作用或被取消的失敗風險。此模式非常適合長時間執行的報告或備份。

SET TRANSACTION SNAPSHOT 指令允許使用與現有事務相同的快照執行新的事務。預先存在的事務必須使用 pg\_export\_snapshot 函數匯出其快照（請參閱[第 9.26.5節](../../ii.-sql-cha-xun-yu-yan/9.-han-shi-ji-yun-suan-zi/9.26.-xi-tong-guan-li-han-shi.md)）。該函數回傳一個快照識別指標，該識別指標必須賦予 SET TRANSACTION SNAPSHOT 以指定要導入哪個快照。該命令中的識別指標必須寫為字串文字，例如 '000003A1-1'。 SET TRANSACTION SNAPSHOT 只能在事務開始時，在事務的第一個查詢或資料修改語句（SELECT、INSERT、DELETE、UPDATE、FETCH 或 COPY）之前執行。此外，事務必須已設定為 SERIALIZABLE 或 REPEATABLE READ 的隔離等級（否則，由於 READ COMMITTED 模式會為每個指令建立一個新快照，因此快照會立即丟棄）。如果導入事務使用 SERIALIZABLE 隔離等級，則導出快照的事務也必須使用該隔離等級。此外，非唯讀序列化事務不能從唯讀事務導入快照。

## 注意

如果在沒有 START TRANSACTION 或 BEGIN 指令的情況下執行 SET TRANSACTION，它會發出警告，並且沒有效果。

透過在 BEGIN 或 START TRANSACTION 指令中指定所需的交易模式，就可以不用 SET TRANSACTION。但該選項並不適用於 SET TRANSACTION SNAPSHOT。

連線預設的交易事務模式也可以透過設定配置參數 [default\_transaction\_isolation](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#default_transaction_isolation-enum)、[default\_transaction\_read\_only](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#default_transaction_read_only-boolean) 和 [default\_transaction\_deferrable](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#default_transaction_deferrable-boolean) 來設置。（事實上，SET SESSION CHARACTERISTICS 也是利用 SET 設定這些變數。）這意味著可以透過 ALTER DATABASE 等在配置檔案中設定預設值。有關更多訊息，請參閱[第 19 章](../../iii.-xi-tong-guan-li/19.-fu-wu-zu-tai-she-ding/)。

## 範例

要使用與現有事務相同的快照開始新的事務，請首先從現有事務中匯出快照。 這將回匯快照識別指標，例如：

```text
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

然後在新的事務開始時於 SET TRANSACTION SNAPSHOT 指令中給予快照識別指標：

```text
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```

## 相容性

這些指令是在 SQL 標準中定義的，除了 DEFERRABLE 事務模式和 SET TRANSACTION SNAPSHOT 形式（它們是 PostgreSQL 延伸指令）之外。

SERIALIZABLE 是標準中的預設的事務隔離等級。在 PostgreSQL 中，預設情況下通常是 READ COMMITTED，但你可以像上面提到的那樣更改它。

在 SQL 標準中，還有一個事務模式可以使用這些指令設定：診斷區域大小（the size of the diagnostics area）。這個概念特別用於嵌入式 SQL，因此 PostgreSQL 並沒有實作。

SQL 標準要求在連續的 transaction\_modes 之間使用逗號，但由於歷史原因，PostgreSQL 允許省略逗號。

