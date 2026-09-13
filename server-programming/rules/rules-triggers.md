<a id="RULES-TRIGGERS"></a>

## 39.7. 規則與觸發程序的比較 [#](#RULES-TRIGGERS)

<a id="id-1.8.6.12.2"></a><a id="id-1.8.6.12.3"></a>

許多可以用觸發程序完成的事情，也可以用 PostgreSQL 規則系統來實作。規則無法實作的其中一件事是某些種類的限制條件，特別是外鍵。你確實可以放置一條帶有限定條件的規則，在某個欄位的值沒有出現在另一個資料表中時，把指令重寫成 `NOTHING`。但這麼一來資料就被默默地丟棄了，而那不是個好主意。如果需要檢查值是否有效，並且在值無效時必須產生錯誤訊息，那就必須用觸發程序來完成。

在本章中，我們把重點放在使用規則來更新檢視表。本章所有的更新規則範例，也都可以用檢視表上的 `INSTEAD OF` 觸發程序來實作。撰寫這類觸發程序往往比撰寫規則容易，尤其是在需要複雜邏輯才能完成更新的時候。

對於兩種方式都能實作的情況，哪一種比較好取決於資料庫的使用方式。觸發程序會針對每一筆受影響的資料列各觸發一次。規則則是修改查詢或產生一個額外的查詢。所以如果一個陳述式影響了許多資料列，那麼發出一個額外指令的規則，很可能會比針對每一筆資料列都被呼叫一次、而且必須反覆判斷該做什麼的觸發程序來得快。不過，觸發程序的作法在概念上遠比規則的作法單純，新手也比較容易做對。

這裡我們舉一個例子，說明在某種情境下規則與觸發程序的選擇會有什麼樣的結果。這裡有兩個資料表：

```

CREATE TABLE computer (
    hostname        text,    -- indexed
    manufacturer    text     -- indexed
);

CREATE TABLE software (
    software        text,    -- indexed
    hostname        text     -- indexed
);
```

兩個資料表都有好幾千筆資料列，而且 `hostname` 上的索引都是唯一的。這個規則或觸發程序要實作的限制是：當某台電腦被刪除時，就從 `software` 中刪除參照到它的資料列。觸發程序會使用這個指令：

```

DELETE FROM software WHERE hostname = $1;
```

由於觸發程序會針對從 `computer` 刪除的每一筆個別資料列被呼叫，因此它可以為這個指令準備並保存執行計畫，然後以參數的方式傳入 `hostname` 的值。而規則則會寫成：

```

CREATE RULE computer_del AS ON DELETE TO computer
    DO DELETE FROM software WHERE hostname = OLD.hostname;
```

現在我們來看看不同類型的刪除。以這個為例：

```

DELETE FROM computer WHERE hostname = 'mypc.local.net';
```

資料表 `computer` 會以索引掃描（很快），而觸發程序所發出的指令也會使用索引掃描（同樣很快）。來自規則的額外指令會是：

```

DELETE FROM software WHERE computer.hostname = 'mypc.local.net'
                       AND software.hostname = computer.hostname;
```

由於已經設定了適當的索引，規劃器會建立這樣的執行計畫

```

Nestloop
  ->  Index Scan using comp_hostidx on computer
  ->  Index Scan using soft_hostidx on software
```

所以觸發程序與規則這兩種實作方式在速度上不會有太大的差異。

在下一個刪除中，我們想要清掉所有 2000 台 `hostname` 以 `old` 開頭的電腦。有兩種可能的指令可以做到這件事。其中之一是：

```

DELETE FROM computer WHERE hostname >= 'old'
                       AND hostname <  'ole'
```

由規則加入的指令會是：

```

DELETE FROM software WHERE computer.hostname >= 'old' AND computer.hostname < 'ole'
                       AND software.hostname = computer.hostname;
```

其執行計畫為

```

Hash Join
  ->  Seq Scan on software
  ->  Hash
    ->  Index Scan using comp_hostidx on computer
```

另一個可能的指令是：

```

DELETE FROM computer WHERE hostname ~ '^old';
```

它會使得由規則所加入的指令產生下列的執行計畫：

```

Nestloop
  ->  Index Scan using comp_hostidx on computer
  ->  Index Scan using soft_hostidx on software
```

這顯示出：當有多個限定條件運算式以 `AND` 結合在一起時（也就是這個指令的正規表示式版本所做的事），規劃器並沒有意識到 `computer` 中針對 `hostname` 的限定條件，其實也可以用來對 `software` 進行索引掃描。觸發程序會針對那 2000 台必須被刪除的舊電腦各被呼叫一次，結果就是對 `computer` 做一次索引掃描，以及對 `software` 做 2000 次索引掃描。規則的實作方式則會用兩個使用索引的指令來完成。而在循序掃描的情況下規則是否仍然比較快，就要看資料表 `software` 的整體大小而定了。從觸發程序透過 SPI 管理器執行 2000 次指令會花掉一些時間，即使所有的索引區塊很快就會進到快取裡也一樣。

我們要看的最後一個指令是：

```

DELETE FROM computer WHERE manufacturer = 'bim';
```

這同樣可能導致從 `computer` 刪除許多資料列。所以觸發程序又會透過執行器執行許多指令。由規則產生的指令會是：

```

DELETE FROM software WHERE computer.manufacturer = 'bim'
                       AND software.hostname = computer.hostname;
```

這個指令的執行計畫同樣會是對兩個索引掃描所做的巢狀迴圈，只是在 `computer` 上使用了不同的索引：

```

Nestloop
  ->  Index Scan using comp_manufidx on computer
  ->  Index Scan using soft_hostidx on software
```

在上述任何一種情況下，來自規則系統的額外指令多多少少都與指令中受影響的資料列數量無關。

總結來說，只有當規則的動作導致大量且限定條件很差的聯結，也就是規劃器失靈的情況下，規則才會明顯比觸發程序來得慢。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules-triggers.html)（原文版本：18.6；核對日期：2026-09-12）
