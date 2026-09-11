<a id="TUTORIAL-TRANSACTIONS"></a>

## 3.4. 交易 [#](#TUTORIAL-TRANSACTIONS)

<a id="id-1.4.5.5.2"></a>

*交易*（Transaction）是所有資料庫系統的基本概念。交易的重點在於，它把多個步驟組合成單一、全有或全無的操作。步驟之間的中間狀態對其他同時進行的交易是不可見的；如果發生某種故障使交易無法完成，那麼這些步驟都完全不會影響資料庫。

舉例來說，考慮一個銀行資料庫，其中包含各個客戶帳戶的餘額，以及各分行的存款總餘額。假設我們想記錄一筆從 Alice 的帳戶支付 $100.00 到 Bob 帳戶的款項。在極度簡化的情況下，對應的 SQL 指令可能像這樣：

```

UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
UPDATE branches SET balance = balance - 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Alice');
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
UPDATE branches SET balance = balance + 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Bob');
```

這些指令的細節在這裡並不重要；重點是，要完成這個相當簡單的操作，需要進行好幾個獨立的更新。銀行的主管會希望確保這些更新要嘛全部發生，要嘛全都不發生。如果系統故障導致 Bob 收到了 $100.00，而 Alice 的帳戶卻沒有被扣款，那絕對不行。同樣地，如果 Alice 被扣了款而 Bob 卻沒有入帳，Alice 也不會一直是滿意的客戶。我們需要一種保證：如果操作進行到一半出了問題，至今已執行的步驟都不會生效。把這些更新組合成一個*交易*，就能提供這種保證。我們說交易是*不可分割的*（atomic）：從其他交易的角度來看，它要嘛完整發生，要嘛完全沒有發生。

我們也需要一種保證：一旦交易完成並經資料庫系統確認，它就確實已被永久記錄，即使之後不久發生當機也不會遺失。例如，如果我們正在記錄 Bob 的一筆現金提領，我們不希望在他剛走出銀行大門時，因為一次當機而讓他帳戶的扣款記錄消失。支援交易的資料庫會保證，在回報交易完成之前，交易所做的所有更新都已記錄在永久儲存裝置中（也就是磁碟上）。

支援交易的資料庫還有另一個重要特性，與不可分割更新的概念密切相關：當多個交易同時執行時，每個交易都不應該看到其他交易尚未完成的變更。例如，如果某個交易正在加總所有分行的餘額，它就不能只計入 Alice 所屬分行的扣款，卻沒有計入 Bob 所屬分行的入帳，反之亦然。因此，交易不僅在對資料庫的永久影響上必須是全有或全無，在進行過程中的可見性上也必須如此。尚未結束的交易至今所做的更新，在該交易完成之前，對其他交易都是不可見的；交易完成時，所有更新會同時變成可見。

在 PostgreSQL 中，建立交易的方式是用 `BEGIN` 與 `COMMIT` 指令將交易中的 SQL 指令包起來。因此，我們的銀行交易實際上會像這樣：

```

BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
-- etc etc
COMMIT;
```

如果在交易進行到一半時，我們決定不要提交（也許是剛發現 Alice 的餘額變成負數），可以改為執行 `ROLLBACK` 指令，而不是 `COMMIT`，至今所做的所有更新都會被取消。

PostgreSQL 實際上會把每個 SQL 陳述式都視為在交易中執行。如果你沒有執行 `BEGIN` 指令，那麼每個陳述式都會隱含地被 `BEGIN` 與（成功時的）`COMMIT` 包起來。以 `BEGIN` 與 `COMMIT` 包起來的一組陳述式，有時稱為*交易區塊*（transaction block）。

### 注意

有些用戶端函式庫會自動發出 `BEGIN` 與 `COMMIT` 指令，因此你可能在沒有要求的情況下就得到交易區塊的效果。請查閱你所使用介面的文件。

你可以透過*交易儲存點*（savepoint），以更細的粒度控制交易中的陳述式。交易儲存點讓你可以選擇性地捨棄交易中的某些部分，同時提交其餘部分。以 `SAVEPOINT` 定義交易儲存點之後，必要時可以用 `ROLLBACK TO` 回復到該交易儲存點。從定義交易儲存點到回復至該點之間，交易對資料庫所做的所有變更都會被捨棄，但在交易儲存點之前的變更則會保留。

回復到某個交易儲存點之後，該交易儲存點仍然存在，因此你可以多次回復到它。反過來說，如果你確定不會再需要回復到某個交易儲存點，可以將它釋放，讓系統釋出一些資源。請記住，無論是釋放某個交易儲存點，還是回復到該點，都會自動釋放在它之後定義的所有交易儲存點。

這些操作全都在交易區塊內進行，因此其他資料庫工作階段都看不到。當你提交交易區塊時（如果你會提交的話），已提交的動作會以一個整體對其他工作階段變成可見，而已回復的動作則永遠不會變成可見。

回到銀行資料庫的例子，假設我們從 Alice 的帳戶扣款 $100.00，並存入 Bob 的帳戶，之後才發現應該存入 Wally 的帳戶才對。我們可以像這樣使用交易儲存點來處理：

```

BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
-- oops ... forget that and use Wally's account
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Wally';
COMMIT;
```

當然，這個例子過度簡化了，但透過交易儲存點，可以在交易區塊中進行許多控制。此外，當交易區塊因錯誤而被系統置於中止狀態時，除了將它完全回復並重新開始之外，`ROLLBACK TO` 是重新取得該交易區塊控制權的唯一方法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-transactions.html)（原文版本：18.6；核對日期：2026-09-11）
