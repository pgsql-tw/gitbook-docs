<a id="RULES-VIEWS"></a>
## 39.2. 檢視表與規則系統 [#](#RULES-VIEWS)

[39.2.1. `SELECT` 規則的運作方式](rules-views.md#RULES-SELECT)

[39.2.2. 非 `SELECT` 陳述式中的檢視表規則](rules-views.md#RULES-VIEWS-NON-SELECT)

[39.2.3. PostgreSQL 中檢視表的強大之處](rules-views.md#RULES-VIEWS-POWER)

[39.2.4. 更新檢視表](rules-views.md#RULES-VIEWS-UPDATE)

<a id="id-1.8.6.7.2"></a><a id="id-1.8.6.7.3"></a>

PostgreSQL 中的檢視表是使用
規則系統來實作的。檢視表基本上是一個空的資料表
（沒有實際的儲存空間），並附有一條
`ON SELECT DO INSTEAD` 規則。依照慣例，
該規則會被命名為 `_RETURN`。
因此，像這樣的檢視表

```

CREATE VIEW myview AS SELECT * FROM mytab;
```

幾乎等同於

```

CREATE TABLE myview (same column list as mytab);
CREATE RULE "_RETURN" AS ON SELECT TO myview DO INSTEAD
    SELECT * FROM mytab;
```

不過你實際上無法這樣寫，因為資料表
不允許擁有 `ON SELECT` 規則。

檢視表也可以擁有其他種類的 `DO INSTEAD`
規則，讓你得以對檢視表執行 `INSERT`、
`UPDATE` 或 `DELETE` 指令，
儘管它並沒有底層的儲存空間。
這一點將在下文的
[39.2.4 節](rules-views.md#RULES-VIEWS-UPDATE)中進一步討論。

<a id="RULES-SELECT"></a>

### 39.2.1. `SELECT` 規則的運作方式 [#](#RULES-SELECT)

<a id="id-1.8.6.7.6.2"></a>

`ON SELECT` 規則會在最後一步被套用到所有查詢，即使
給定的指令是 `INSERT`、
`UPDATE` 或 `DELETE` 也一樣。而且
它們的語意與其他指令類型的規則不同，因為它們是就地修改
查詢樹，而不是建立一棵新的查詢樹。因此
我們先說明 `SELECT` 規則。

目前，`ON SELECT` 規則中只能有一個動作，且該動作必須
是一個無條件、`INSTEAD` 的 `SELECT` 動作。之所以有這項限制，
是為了讓規則有足夠的安全性，能開放給一般使用者使用，
而這也讓 `ON SELECT` 規則的行為被限制得像是檢視表。

本章的範例是兩個進行某些計算的聯結檢視表，以及
另外一些依次使用它們的檢視表。這兩個最初的
檢視表之一，稍後會透過加入
`INSERT`、`UPDATE` 與
`DELETE` 操作的規則來加以客製化，讓最終的結果
成為一個行為就像真正資料表、但帶有一些魔法功能的檢視表。這不是一個
可以簡單入門的範例，這也讓事情變得比較難以理解。
但比起使用許多可能會讓人搞混的不同範例，
使用一個能循序涵蓋所有討論重點的範例，會是比較好的做法。

在前兩個規則系統的說明中，我們需要用到以下真正的資料表：

```

CREATE TABLE shoe_data (
    shoename   text,          -- primary key
    sh_avail   integer,       -- available number of pairs
    slcolor    text,          -- preferred shoelace color
    slminlen   real,          -- minimum shoelace length
    slmaxlen   real,          -- maximum shoelace length
    slunit     text           -- length unit
);

CREATE TABLE shoelace_data (
    sl_name    text,          -- primary key
    sl_avail   integer,       -- available number of pairs
    sl_color   text,          -- shoelace color
    sl_len     real,          -- shoelace length
    sl_unit    text           -- length unit
);

CREATE TABLE unit (
    un_name    text,          -- primary key
    un_fact    real           -- factor to transform to cm
);
```

如你所見，它們代表的是鞋店的資料。

這些檢視表是這樣建立的：

```

CREATE VIEW shoe AS
    SELECT sh.shoename,
           sh.sh_avail,
           sh.slcolor,
           sh.slminlen,
           sh.slminlen * un.un_fact AS slminlen_cm,
           sh.slmaxlen,
           sh.slmaxlen * un.un_fact AS slmaxlen_cm,
           sh.slunit
      FROM shoe_data sh, unit un
     WHERE sh.slunit = un.un_name;

CREATE VIEW shoelace AS
    SELECT s.sl_name,
           s.sl_avail,
           s.sl_color,
           s.sl_len,
           s.sl_unit,
           s.sl_len * u.un_fact AS sl_len_cm
      FROM shoelace_data s, unit u
     WHERE s.sl_unit = u.un_name;

CREATE VIEW shoe_ready AS
    SELECT rsh.shoename,
           rsh.sh_avail,
           rsl.sl_name,
           rsl.sl_avail,
           least(rsh.sh_avail, rsl.sl_avail) AS total_avail
      FROM shoe rsh, shoelace rsl
     WHERE rsl.sl_color = rsh.slcolor
       AND rsl.sl_len_cm >= rsh.slminlen_cm
       AND rsl.sl_len_cm <= rsh.slmaxlen_cm;
```

`shoelace` 檢視表（這是我們這裡最簡單的一個）的
`CREATE VIEW` 指令，會建立一個關係
`shoelace`，並在 `pg_rewrite` 中
建立一筆項目，表示只要查詢的範圍表中
參照到關係 `shoelace`，就有一條重寫規則必須被套用。
這條規則沒有規則限定條件（rule qualification，稍後會與非
`SELECT` 規則一起討論，因為目前 `SELECT`
規則不能有規則限定條件），且它是 `INSTEAD` 的。請注意，
規則限定條件與查詢限定條件並不相同。
我們這條規則的動作，有一個查詢限定條件。
該規則的動作，是一棵查詢樹，
是檢視表建立指令中 `SELECT` 陳述式的副本。

### 注意

你可以在
`pg_rewrite` 項目中看到的兩筆額外範圍表項目，
`NEW` 與 `OLD`，
對 `SELECT` 規則而言並不重要。

現在，我們對 `unit`、`shoe_data`
與 `shoelace_data` 填入資料，並對某個檢視表執行一個簡單的查詢：

```

INSERT INTO unit VALUES ('cm', 1.0);
INSERT INTO unit VALUES ('m', 100.0);
INSERT INTO unit VALUES ('inch', 2.54);

INSERT INTO shoe_data VALUES ('sh1', 2, 'black', 70.0, 90.0, 'cm');
INSERT INTO shoe_data VALUES ('sh2', 0, 'black', 30.0, 40.0, 'inch');
INSERT INTO shoe_data VALUES ('sh3', 4, 'brown', 50.0, 65.0, 'cm');
INSERT INTO shoe_data VALUES ('sh4', 3, 'brown', 40.0, 50.0, 'inch');

INSERT INTO shoelace_data VALUES ('sl1', 5, 'black', 80.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl2', 6, 'black', 100.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl3', 0, 'black', 35.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl4', 8, 'black', 40.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl5', 4, 'brown', 1.0 , 'm');
INSERT INTO shoelace_data VALUES ('sl6', 0, 'brown', 0.9 , 'm');
INSERT INTO shoelace_data VALUES ('sl7', 7, 'brown', 60 , 'cm');
INSERT INTO shoelace_data VALUES ('sl8', 1, 'brown', 40 , 'inch');

SELECT * FROM shoelace;

 sl_name   | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
-----------+----------+----------+--------+---------+-----------
 sl1       |        5 | black    |     80 | cm      |        80
 sl2       |        6 | black    |    100 | cm      |       100
 sl7       |        7 | brown    |     60 | cm      |        60
 sl3       |        0 | black    |     35 | inch    |      88.9
 sl4       |        8 | black    |     40 | inch    |     101.6
 sl8       |        1 | brown    |     40 | inch    |     101.6
 sl5       |        4 | brown    |      1 | m       |       100
 sl6       |        0 | brown    |    0.9 | m       |        90
(8 rows)
```

這是我們可以對檢視表執行的最簡單的
`SELECT`，因此我們藉此機會來說明檢視表
規則的基本原理。`SELECT * FROM shoelace` 會
被剖析器解讀，並產生以下查詢樹：

```

SELECT shoelace.sl_name, shoelace.sl_avail,
       shoelace.sl_color, shoelace.sl_len,
       shoelace.sl_unit, shoelace.sl_len_cm
  FROM shoelace shoelace;
```

接著這棵查詢樹會交給規則系統。規則系統會走訪
範圍表，檢查是否有任何關係附有規則。
在處理 `shoelace` 的範圍表項目時
（目前為止唯一的一個），它會找到
`_RETURN` 規則，其查詢樹為：

```

SELECT s.sl_name, s.sl_avail,
       s.sl_color, s.sl_len, s.sl_unit,
       s.sl_len * u.un_fact AS sl_len_cm
  FROM shoelace old, shoelace new,
       shoelace_data s, unit u
 WHERE s.sl_unit = u.un_name;
```

為了展開這個檢視表，重寫器只是單純建立一個包含
該規則動作查詢樹的子查詢範圍表項目，並以這個
範圍表項目取代原本參照該檢視表的項目。
結果重寫後的查詢樹，幾乎與你手動輸入以下內容時所得到的結果相同：

```

SELECT shoelace.sl_name, shoelace.sl_avail,
       shoelace.sl_color, shoelace.sl_len,
       shoelace.sl_unit, shoelace.sl_len_cm
  FROM (SELECT s.sl_name,
               s.sl_avail,
               s.sl_color,
               s.sl_len,
               s.sl_unit,
               s.sl_len * u.un_fact AS sl_len_cm
          FROM shoelace_data s, unit u
         WHERE s.sl_unit = u.un_name) shoelace;
```

不過，有一個地方不同：子查詢的範圍表中，多了兩筆
額外的項目 `shoelace old` 與 `shoelace new`。這些項目
不會直接參與查詢，因為它們並不會被
子查詢的聯結樹或目標清單所參照。重寫器使用它們
來儲存原本存在於參照該檢視表的範圍表項目中的
存取權限檢查資訊。如此一來，即使重寫後的查詢
中並未直接使用該檢視表，
執行器仍然會檢查使用者是否具備存取該檢視表的適當權限。

這就是所套用的第一條規則。規則系統接著會繼續
檢查上層查詢中剩餘的範圍表項目（在這個範例中
已經沒有其他項目了），並且會遞迴地檢查新加入的子查詢中
的範圍表項目，看看其中是否有任何一個參照到檢視表。（但它
不會展開 `old` 或 `new` — 否則我們就會遇到無窮遞迴！）
在這個範例中，`shoelace_data` 或 `unit`
都沒有重寫規則，因此重寫工作已經完成，
上述結果就是交給規劃器的最終結果。

現在，我們想寫一個查詢，找出目前店裡有哪些鞋子，
存在著顏色與長度都相符的鞋帶，且
完全相符配對的總數大於等於二。

```

SELECT * FROM shoe_ready WHERE total_avail >= 2;

 shoename | sh_avail | sl_name | sl_avail | total_avail
----------+----------+---------+----------+-------------
 sh1      |        2 | sl1     |        5 |           2
 sh3      |        4 | sl7     |        7 |           4
(2 rows)
```

這次剖析器的輸出是以下查詢樹：

```

SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM shoe_ready shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

所套用的第一條規則，會是
`shoe_ready` 檢視表的規則，其結果為
以下查詢樹：

```

SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM (SELECT rsh.shoename,
               rsh.sh_avail,
               rsl.sl_name,
               rsl.sl_avail,
               least(rsh.sh_avail, rsl.sl_avail) AS total_avail
          FROM shoe rsh, shoelace rsl
         WHERE rsl.sl_color = rsh.slcolor
           AND rsl.sl_len_cm >= rsh.slminlen_cm
           AND rsl.sl_len_cm <= rsh.slmaxlen_cm) shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

同樣地，`shoe` 與
`shoelace` 的規則，也會被代入子查詢
的範圍表中，最終形成一棵三層的查詢樹：

```

SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM (SELECT rsh.shoename,
               rsh.sh_avail,
               rsl.sl_name,
               rsl.sl_avail,
               least(rsh.sh_avail, rsl.sl_avail) AS total_avail
          FROM (SELECT sh.shoename,
                       sh.sh_avail,
                       sh.slcolor,
                       sh.slminlen,
                       sh.slminlen * un.un_fact AS slminlen_cm,
                       sh.slmaxlen,
                       sh.slmaxlen * un.un_fact AS slmaxlen_cm,
                       sh.slunit
                  FROM shoe_data sh, unit un
                 WHERE sh.slunit = un.un_name) rsh,
               (SELECT s.sl_name,
                       s.sl_avail,
                       s.sl_color,
                       s.sl_len,
                       s.sl_unit,
                       s.sl_len * u.un_fact AS sl_len_cm
                  FROM shoelace_data s, unit u
                 WHERE s.sl_unit = u.un_name) rsl
         WHERE rsl.sl_color = rsh.slcolor
           AND rsl.sl_len_cm >= rsh.slminlen_cm
           AND rsl.sl_len_cm <= rsh.slmaxlen_cm) shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

這樣看起來可能沒有效率，但規劃器會透過將子查詢
「向上提升（pulling up）」，把它壓平成一棵單層的查詢樹，
接著就會像我們手動寫出所有聯結一樣，
規劃這些聯結。因此，壓平查詢樹是一種最佳化，
重寫系統本身並不需要為此操心。

<a id="RULES-VIEWS-NON-SELECT"></a>

### 39.2.2. 非 `SELECT` 陳述式中的檢視表規則 [#](#RULES-VIEWS-NON-SELECT)

上面對檢視表規則的說明中，並未觸及查詢樹的
兩個細節：指令類型與結果關係。
事實上，檢視表規則並不需要指令類型，但結果
關係可能會影響查詢重寫器的運作方式，因為當結果關係
是檢視表時，需要特別小心處理。

`SELECT` 的查詢樹與其他任何
指令的查詢樹之間，只有少數幾個差異。顯而易見地，
它們的指令類型不同，而對於非 `SELECT`
的指令而言，結果關係會指向結果應該
寫入的範圍表項目。其他一切都完全相同。因此，假設有兩個資料表
`t1` 與 `t2`，各有欄位 `a` 與
`b`，以下這兩個陳述式的查詢樹：

```

SELECT t2.b FROM t1, t2 WHERE t1.a = t2.a;

UPDATE t1 SET b = t2.b FROM t2 WHERE t1.a = t2.a;
```

幾乎完全一樣。具體來說：

* 範圍表都包含資料表 `t1` 與 `t2` 的項目。
* 目標清單都包含一個變數，指向資料表 `t2`
  範圍表項目的欄位 `b`。
* 限定條件運算式都比較兩個
  範圍表項目的欄位 `a` 是否相等。
* 聯結樹都顯示 `t1` 與 `t2` 之間的簡單聯結。

其結果就是，這兩棵查詢樹都會產生類似的
執行計畫：它們都是這兩個資料表之間的聯結。對於
`UPDATE` 而言，規劃器會將 `t1` 中缺少的欄位
加入目標清單，最終的查詢樹會變成：

```

UPDATE t1 SET a = t1.a, b = t2.b FROM t2 WHERE t1.a = t2.a;
```

因此，執行器對該聯結執行的結果，會產生
與以下查詢完全相同的結果集：

```

SELECT t1.a, t2.b FROM t1, t2 WHERE t1.a = t2.a;
```

但 `UPDATE` 中存在一個小問題：執行器計畫中
負責執行聯結的部分，並不在意聯結的結果
究竟是要拿來做什麼用。它只是產生一個資料列的結果集。
一個是 `SELECT` 指令、另一個是
`UPDATE` 指令，這件事是在執行器的更上層處理的，
在那裡，系統知道這是一個 `UPDATE`，也知道
這個結果應該寫入資料表 `t1`。但究竟結果集中
哪一列，應該被新的資料列取代呢？

為了解決這個問題，`UPDATE`（以及
`DELETE`）陳述式的目標清單中，會加入
另一項：目前的元組 ID（current tuple ID，
CTID）<a id="id-1.8.6.7.7.5.4"></a>。
這是一個系統欄位，內含
該資料列所在的檔案區塊編號，以及在該區塊中的位置。
在知道資料表的情況下，就可以使用 CTID 來取回
要更新的 `t1` 原始資料列。將
CTID 加入目標清單後，該查詢實際上看起來會像是：

```

SELECT t1.a, t2.b, t1.ctid FROM t1, t2 WHERE t1.a = t2.a;
```

現在，PostgreSQL 的另一項細節
登場了。舊的資料表列並不會被覆寫，這也是
`ROLLBACK` 之所以快速的原因。在
`UPDATE` 中，新的結果列會被插入該資料表中（在
去除 CTID 之後），而在 CTID 所指向的
舊列的列標頭中，`cmax` 與
`xmax` 這兩個項目，會被設定為目前的指令計數器
與目前的交易 ID。因此，舊的列會被隱藏起來，
在交易提交之後，資料清理程式（vacuum）最終就能移除
這個已死的列。

了解了以上這一切之後，我們就可以將檢視表規則以完全
相同的方式，套用到任何指令上。這之間並沒有差別。

<a id="RULES-VIEWS-POWER"></a>

### 39.2.3. PostgreSQL 中檢視表的強大之處 [#](#RULES-VIEWS-POWER)

上面說明了規則系統如何將檢視表
定義，併入原本的查詢樹中。在第二個範例中，一個
針對某個檢視表的簡單 `SELECT`，
最終產生了一棵四個資料表聯結的查詢樹
（`unit` 以不同的名稱被使用了兩次）。

以規則系統來實作檢視表的好處在於，
規劃器可以在單一棵查詢樹中，同時取得
哪些資料表需要被掃描、這些資料表之間的關係、
來自檢視表的限制性限定條件，
以及來自原始查詢的限定條件等所有資訊。
即使原始查詢本身已經是對多個檢視表的聯結，
情況也依然如此。
規劃器必須決定執行該查詢
最佳的路徑為何，而規劃器所掌握的資訊
越多，這項決策就能做得越好。而
PostgreSQL 中所實作的規則系統，
確保了在那個時間點，所有關於該查詢的資訊
都是可取得的。

<a id="RULES-VIEWS-UPDATE"></a>

### 39.2.4. 更新檢視表 [#](#RULES-VIEWS-UPDATE)

若某個檢視表被指定為
`INSERT`、`UPDATE`、
`DELETE` 或 `MERGE` 的目標關係，
會發生什麼事呢？若照上述方式進行替換，就會得到一棵
結果關係指向子查詢範圍表項目的查詢樹，這是行不通的。
不過，PostgreSQL 有幾種方式，
可以支援「看起來像是」在更新檢視表的操作。
依使用者所感受到的複雜度排序，分別是：自動代換為
檢視表底層的資料表、執行使用者自訂的觸發程序，
或依照使用者自訂的規則重寫查詢。
以下將分別討論這些選項。

若子查詢是從單一基礎關係中選取，且夠簡單，
重寫器就可以自動以底層的基礎關係
取代該子查詢，讓 `INSERT`、
`UPDATE`、`DELETE` 或
`MERGE` 能以適當的方式套用到基礎關係上。
「夠簡單」而能適用這種做法的檢視表，稱為
*可自動更新（automatically updatable）*的檢視表。
關於哪些種類的檢視表可以自動更新的詳細資訊，請參閱
[CREATE VIEW](../../reference/sql-commands/sql-createview.md)。

另一種做法，是由使用者為檢視表提供
`INSTEAD OF` 觸發程序來處理該操作
（請參閱[CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md)）。
在這種情況下，重寫的運作方式略有不同。
對於 `INSERT`，重寫器完全不會對檢視表
做任何處理，讓它保持為該查詢的結果
關係。對於 `UPDATE`、`DELETE`
與 `MERGE`，仍然需要展開
檢視表查詢，以產生該指令將嘗試更新、刪除或合併的
「舊」列。因此該檢視表會照常被展開，
但查詢中還會加入另一個未展開的範圍表項目，
以其身為結果關係的身分，來代表該檢視表。

現在產生的問題是，該如何辨識檢視表中
要更新的列。回想一下，當結果關係
是資料表時，會在目標清單中加入一個特殊的
CTID 項目，用來辨識要更新的資料列的實體位置。
若結果關係是檢視表，這個做法就行不通了，因為檢視表
沒有任何 CTID，因為它的資料列
並沒有實際的實體位置。取而代之，對於 `UPDATE`、
`DELETE` 或 `MERGE` 操作，
會在目標清單中加入一個特殊的 `wholerow` 項目，
它會展開成包含該檢視表的所有欄位。執行器會使用這個
值，將「舊」的列提供給
`INSTEAD OF` 觸發程序。至於該根據新舊列的值
判斷該更新什麼，則由觸發程序自行決定。

另一種可能的做法，是由使用者定義
`INSTEAD` 規則，為檢視表上的 `INSERT`、
`UPDATE` 與 `DELETE`
指令指定替代動作。這些規則會重寫該指令，通常會重寫成
一個更新一或多個資料表（而非檢視表）的指令。這是
[39.4 節](rules-update.md)的主題。請注意，這種做法對
`MERGE` 並不適用，因為它目前
在目標關係上，除了 `SELECT` 規則之外，並不支援其他規則。

請注意，規則會先被求值，在原始查詢被規劃與
執行之前，先將其重寫。因此，若某個檢視表
同時具有 `INSTEAD OF` 觸發程序，以及針對 `INSERT`、
`UPDATE` 或 `DELETE` 的規則，則規則會
先被求值，而視結果而定，觸發程序有可能
完全不會被使用。

對簡單檢視表上的 `INSERT`、
`UPDATE`、`DELETE` 或
`MERGE` 查詢進行自動重寫，
永遠是最後才會嘗試的做法。因此，若某個檢視表有規則或
觸發程序，它們會覆蓋掉可自動更新檢視表的
預設行為。

若該檢視表沒有 `INSTEAD` 規則或 `INSTEAD OF`
觸發程序，且重寫器無法將該查詢自動重寫為
對底層基礎關係的更新，就會擲回錯誤，
因為執行器本身無法就這樣更新一個檢視表。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules-views.html)（原文版本：18.6；核對日期：2026-09-22）
