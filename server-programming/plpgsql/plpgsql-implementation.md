<a id="PLPGSQL-IMPLEMENTATION"></a>
## 41.11. PL/pgSQL 內部運作原理 [#](#PLPGSQL-IMPLEMENTATION)

[41.11.1. 變數代換](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)

[41.11.2. 計畫快取](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)

本節討論一些對 PL/pgSQL 使用者而言，經常十分重要的實作細節。

<a id="PLPGSQL-VAR-SUBST"></a>

### 41.11.1. 變數代換 [#](#PLPGSQL-VAR-SUBST)

PL/pgSQL 函式中的 SQL 陳述式與運算式，
可以參照該函式的變數與參數。在幕後，
PL/pgSQL 會以查詢參數取代這類參照。
查詢參數只會在語法上允許的位置被取代。作為一個極端的例子，
請考慮以下這種不良的程式撰寫風格範例：

```

INSERT INTO foo (foo) VALUES (foo(foo));
```

第一次出現的 `foo`，在語法上必須是一個資料表
名稱，因此不會被取代，即使該函式有一個名為
`foo` 的變數也一樣。第二次出現的，必須是該資料表
某個欄位的名稱，因此同樣不會被取代。同理，
第三次出現的必須是函式名稱，因此也不會被
取代。只有最後一次出現的，才有可能是對 PL/pgSQL
函式某個變數的參照。

換個方式理解，變數代換只能將資料值插入 SQL
命令中；它無法動態變更該命令所參照的資料庫物件。（若您想要
這麼做，就必須如[41.5.4 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)所述，
動態建構命令字串。）

由於變數名稱在語法上與資料表欄位名稱並無不同，因此在同時
參照資料表的陳述式中，可能會出現歧義：某個給定的名稱，究竟是指
資料表欄位，還是變數？讓我們將先前的範例改成

```

INSERT INTO dest (col) SELECT foo + bar FROM src;
```

在此範例中，`dest` 與 `src` 必須是資料表名稱，
`col` 必須是 `dest` 的某個欄位，但 `foo`
與 `bar` 則有可能合理地是該函式的變數，
或是 `src` 的欄位。

在預設情況下，若 SQL 陳述式中的某個名稱，既可能指變數，
也可能指資料表欄位，PL/pgSQL 就會回報錯誤。
您可以透過重新命名該變數或欄位、限定該有歧義的參照，
或是告知 PL/pgSQL 應優先採用哪種解讀方式，
來解決這類問題。

最簡單的解決方式，就是重新命名該變數或欄位。
常見的程式撰寫規則，是為 PL/pgSQL
變數採用與欄位名稱不同的命名慣例。舉例來說，
若您一律將函式變數命名為
`v_something`，而您的
欄位名稱都不以 `v_` 開頭，就不會發生衝突。

或者，您也可以限定有歧義的參照，使其意義明確。
在上述範例中，`src.foo` 便是對該資料表欄位明確無歧義的參照。
若要建立對變數明確無歧義的參照，請在一個帶標籤的區塊中宣告該變數，
並使用該區塊的標籤（見[41.2 節](plpgsql-structure.md)）。舉例來說，

```

<<block>>
DECLARE
    foo int;
BEGIN
    foo := ...;
    INSERT INTO dest (col) SELECT block.foo + bar FROM src;
```

此處 `block.foo` 指的是該變數，即使 `src` 中
存在欄位 `foo` 也一樣。函式的參數，以及像
`FOUND` 這樣的特殊變數，都可以用函式名稱來限定，
因為它們是隱含地在一個以函式名稱為標籤的外層區塊中宣告的。

有時候，在一大段 PL/pgSQL 程式碼中，修正所有有歧義的
參照並不切實際。在這種情況下，您可以指定
PL/pgSQL 應將有歧義的參照解析為變數
（此行為與 PostgreSQL 9.0 之前
PL/pgSQL 的行為相容），或解析為
資料表欄位（此行為與 Oracle 等其他系統相容）。

<a id="id-1.8.8.13.3.9"></a>

若要在系統層級變更此行為，請將組態
參數 `plpgsql.variable_conflict` 設為
`error`、`use_variable` 或
`use_column` 其中之一（`error` 是出廠預設值）。
此參數會影響後續在
PL/pgSQL 函式中編譯的陳述式，但不會影響目前工作階段中
已經編譯過的陳述式。
由於變更此設定
可能導致 PL/pgSQL 函式的行為出現非預期的變化，
因此只有超級使用者才能變更此設定。

您也可以逐一函式各別設定此行為，方式是在
函式文字的開頭，插入以下其中一個特殊命令：

```

#variable_conflict error
#variable_conflict use_variable
#variable_conflict use_column
```

這些命令只會影響其所在的那個函式，並會覆寫
`plpgsql.variable_conflict` 的設定。範例如下：

```

CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    #variable_conflict use_variable
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = curtime, comment = comment
          WHERE users.id = id;
    END;
$$ LANGUAGE plpgsql;
```

在此 `UPDATE` 命令中，無論 `users` 是否具有這些名稱的
欄位，`curtime`、`comment` 與
`id` 都會指該函式的變數與參數。請注意，
我們必須在 `WHERE` 子句中，限定對 `users.id` 的參照，
才能使其指向該資料表欄位。
但我們不需要限定 `UPDATE` 清單中，作為
目標的 `comment` 參照，因為在語法上，
它必然是 `users` 的欄位。我們也可以改用以下方式，
撰寫出相同的函式，而不需依賴 `variable_conflict` 設定：

```

CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    <<fn>>
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = fn.curtime, comment = stamp_user.comment
          WHERE users.id = stamp_user.id;
    END;
$$ LANGUAGE plpgsql;
```

在提供給 `EXECUTE` 或其變體的命令字串中，不會發生變數代換。
若您需要將某個變動的值插入此類命令中，
請將其作為建構字串值的一部分來處理，或使用 `USING`，
如[41.5.4 節](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)中所示範。

目前變數代換只在 `SELECT`、
`INSERT`、`UPDATE`、
`DELETE`、`MERGE` 以及包含這類命令的
命令（例如 `EXPLAIN` 與
`CREATE TABLE ... AS SELECT`）中運作，因為主要的 SQL
引擎只允許在這些命令中使用查詢參數。若要在其他陳述式類型
（一般統稱為公用程式陳述式）中使用非常數的名稱或值，
您必須將該公用程式陳述式建構為字串，並以
`EXECUTE` 執行。

<a id="PLPGSQL-PLAN-CACHING"></a>

### 41.11.2. 計畫快取 [#](#PLPGSQL-PLAN-CACHING)

PL/pgSQL 直譯器會在該函式（於各工作階段中）首次被呼叫時，
剖析其原始碼文字，並產生一個內部的二進位指令樹。
該指令樹會完整轉譯
PL/pgSQL 的陳述式結構，但函式中所使用的
個別 SQL 運算式與 SQL 命令，
則不會立即被轉譯。

<a id="id-1.8.8.13.4.3.1"></a>
當函式中每個運算式與 SQL 命令首次
被執行時，PL/pgSQL 直譯器會
剖析並分析該命令，以建立一個預備陳述式，
方式是使用 SPI 管理員的
`SPI_prepare` 函式。
之後再次執行同一運算式或命令時，
會重複使用該預備陳述式。因此，若函式中含有極少被執行到的
條件式程式碼路徑，就永遠不會在目前工作階段中，
承擔分析那些從未被執行之命令的額外負擔。這樣做的一項缺點，
是特定運算式或命令中的錯誤，要等到執行時抵達函式的
那一部分才能被偵測到。（單純的語法
錯誤會在初次剖析階段就被偵測到，但更深層的問題
要等到執行時才會被偵測到。）

此外，PL/pgSQL（或更精確地說，是 SPI 管理員）
可以嘗試快取與任一特定預備陳述式相關聯的執行計畫。若沒有
使用快取的計畫，則每次執行到該陳述式時，都會產生一個
全新的執行計畫，並可利用目前的參數值（也就是 PL/pgSQL
的變數值）來最佳化所選出的計畫。若該
陳述式沒有參數，或是被執行了許多次，SPI 管理員便會
考慮建立一個不依賴特定參數值的*通用*計畫，
並將其快取以供重複使用。通常，只有在該執行計畫對其中所參照
PL/pgSQL 變數值的敏感度不高時，才會發生這種情況。
若敏感度較高，則每次都重新產生計畫反而較為划算。關於預備陳述式行為的
更多資訊，請參閱 [PREPARE](../../reference/sql-commands/sql-prepare.md)。

由於 PL/pgSQL 會以此方式儲存預備陳述式，
有時也會儲存執行計畫，因此直接出現在
PL/pgSQL 函式中的 SQL 命令，在每次執行時
都必須參照相同的資料表與欄位；也就是說，您不能在 SQL 命令中，
使用參數作為資料表或欄位的名稱。若要規避此限制，您可以使用
PL/pgSQL 的 `EXECUTE`
陳述式建構動態命令——代價是每次執行時，都必須執行新的剖析分析，
並建構新的執行計畫。

紀錄變數（record variable）可變的特性，在這方面又帶來另一個問題。
當紀錄變數的欄位被用於
運算式或陳述式中時，這些欄位的資料型別，在函式的每次呼叫之間都不得
改變，因為每個運算式都會使用其首次被抵達時所存在的
資料型別來分析。必要時，可以使用 `EXECUTE`
來規避這個問題。

若同一個函式被用作一個以上資料表的觸發程序，
PL/pgSQL 會為每個這樣的資料表，各自獨立準備並快取
陳述式——也就是說，快取是依每個觸發程序函式與資料表的
組合建立的，而不只是依每個函式建立。這在一定程度上緩解了
資料型別變動所帶來的問題；舉例來說，一個觸發程序函式，
即使名為 `key` 的欄位在不同資料表中，剛好具有不同的
型別，仍然能夠成功運作。

同樣地，具有多型引數型別的函式，會為其被呼叫時使用過的
每一種實際引數型別組合，各自維護一個獨立的陳述式快取，
如此一來，資料型別的差異就不會導致非預期的失敗。

陳述式快取有時會對時間敏感值的解讀，產生令人意外的
效果。舉例來說，以下這兩個函式的行為便有所不同：

```

CREATE FUNCTION logfunc1(logtxt text) RETURNS void AS $$
    BEGIN
        INSERT INTO logtable VALUES (logtxt, 'now');
    END;
$$ LANGUAGE plpgsql;
```

以及：

```

CREATE FUNCTION logfunc2(logtxt text) RETURNS void AS $$
    DECLARE
        curtime timestamp;
    BEGIN
        curtime := 'now';
        INSERT INTO logtable VALUES (logtxt, curtime);
    END;
$$ LANGUAGE plpgsql;
```

就 `logfunc1` 而言，PostgreSQL
的主剖析器在分析該 `INSERT` 時，
便已知道字串
`'now'` 應解讀為
`timestamp`，因為
`logtable` 的目標欄位屬於該型別。因此，
`'now'` 會在分析該
`INSERT` 時，被轉換為一個 `timestamp`
常數，之後在該工作階段存續期間，
`logfunc1` 的每一次呼叫都會使用這個常數。不用說，
這並不是程式設計者原本想要的結果。較好的做法，是使用 `now()` 或
`current_timestamp` 函式。

就 `logfunc2` 而言，PostgreSQL
的主剖析器並不知道
`'now'` 應成為什麼型別，因此
它會傳回一個型別為 `text`、內容為字串
`now` 的資料值。在隨後將其指派給
區域變數 `curtime` 的過程中，
PL/pgSQL 直譯器會透過呼叫
`textout` 與 `timestamp_in`
函式，將這個字串轉型為 `timestamp` 型別。
因此，計算出的時間戳記，會如程式設計者所預期的，在每次執行時更新。
儘管這確實如預期般運作，但效率並不算太好，因此
使用 `now()` 函式，仍然是較好的做法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-implementation.html)（原文版本：18.6；核對日期：2026-09-16）
