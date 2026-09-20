<a id="RULES-UPDATE"></a>
## 39.4. `INSERT`、`UPDATE` 與 `DELETE` 上的規則 [#](#RULES-UPDATE)

[39.4.1. 更新規則的運作方式](rules-update.md#RULES-UPDATE-HOW)

[39.4.2. 與檢視表的協同運作](rules-update.md#RULES-UPDATE-VIEWS)

<a id="id-1.8.6.9.2"></a><a id="id-1.8.6.9.3"></a><a id="id-1.8.6.9.4"></a>

定義在 `INSERT`、`UPDATE`
與 `DELETE` 上的規則，與前面幾節所描述的
檢視表規則有顯著的不同。首先，它們的 `CREATE
RULE` 指令允許更多做法：

* 允許沒有動作。
* 可以有多個動作。
* 可以是 `INSTEAD` 或 `ALSO`（預設）。
* 虛擬關係 `NEW` 與 `OLD` 會變得有用。
* 可以有規則限定條件。

其次，它們並不是就地修改查詢樹。而是
建立零個或多個新的查詢樹，並可以捨棄
原本的查詢樹。

### 小心

在許多情況下，原本可以透過
`INSERT`/`UPDATE`/`DELETE` 規則完成的工作，
用觸發程序來做會更好。觸發程序在記法上稍微複雜一些，
但其語意要容易理解得多。當原始查詢中包含
不穩定（volatile）函式時，規則往往會產生令人意外的
結果：在執行規則的過程中，不穩定函式可能會被執行
比預期更多次。

此外，這類規則完全不支援某些情況，尤其包括
在原始查詢中使用 `WITH` 子句，
以及在 `UPDATE` 查詢的 `SET` 清單中
使用多重指定的子 `SELECT`。這是因為將這些
結構複製到規則查詢中，會導致子查詢被多次求值，
違背了查詢撰寫者原本明確的意圖。

<a id="RULES-UPDATE-HOW"></a>

### 39.4.1. 更新規則的運作方式 [#](#RULES-UPDATE-HOW)

請記住這個語法：

```

CREATE [ OR REPLACE ] RULE name AS ON event
    TO table [ WHERE condition ]
    DO [ ALSO | INSTEAD ] { NOTHING | command | ( command ; command ... ) }
```

以下所稱的*更新規則（update rules）*，
指的是定義在 `INSERT`、`UPDATE` 或
`DELETE` 上的規則。

當某個查詢樹的結果關係與指令類型，
與 `CREATE RULE` 指令中給定的
物件與事件相符時，規則系統就會套用更新規則。
對於更新規則，規則系統會建立一份查詢樹清單。
一開始，這份查詢樹清單是空的。
動作的數量可以是零個（`NOTHING` 關鍵字）、一個，或多個。
為簡化說明，我們先來看只有一個動作的規則。這個規則
可以有限定條件，也可以沒有，而且可以是 `INSTEAD`
或 `ALSO`（預設）。

什麼是規則限定條件？它是一項限制，用來說明
規則的動作應該在什麼時候執行、什麼時候不執行。這個
限定條件只能參照虛擬關係 `NEW` 及／或 `OLD`，
它們基本上代表作為物件給定的那個關係（但帶有
特殊意義）。

因此，對於單一動作的規則，我們有三種情況，
會產生以下的查詢樹。

無限定條件，搭配 `ALSO` 或 `INSTEAD` 皆可
:   規則動作的查詢樹，並加上原始查詢樹
    的限定條件

有給定限定條件，且為 `ALSO`
:   規則動作的查詢樹，並加上規則
    限定條件與原始查詢樹的限定條件

有給定限定條件，且為 `INSTEAD`
:   規則動作的查詢樹，並加上規則
    限定條件與原始查詢樹的限定條件；以及
    原始查詢樹，並加上經過否定的規則限定條件

最後，若該規則是 `ALSO`，則會將未經修改的原始
查詢樹，加入清單中。由於只有帶限定條件的 `INSTEAD`
規則，才會另外加入原始查詢樹，因此，對於只有一個動作的
規則，我們最終會得到一個或兩個輸出查詢樹。

對於 `ON INSERT` 規則而言，原始查詢（若未被 `INSTEAD`
所抑制）會在規則所加入的任何動作之前執行。這讓
這些動作能夠看到已插入的資料列。但對於 `ON UPDATE` 與
`ON DELETE` 規則而言，原始查詢會在規則所加入的
動作之後執行。這確保了這些動作能夠看到即將被更新
或即將被刪除的資料列；否則，這些動作可能會因為找不到
符合其限定條件的資料列而什麼都不做。

由規則動作所產生的查詢樹，會再次被丟入
重寫系統，可能還會套用更多規則，導致
產生更多或更少的查詢樹。
因此，規則的動作，必須擁有與規則本身
不同的指令類型，或不同的結果關係，
否則這個遞迴過程將會陷入無窮迴圈。
（規則的遞迴展開會被偵測到，並回報為錯誤。）

`pg_rewrite` 系統目錄中，動作內所包含的
查詢樹，只是範本。由於它們可以參照
`NEW` 與 `OLD` 的範圍表項目，在它們能被使用之前，
必須先進行一些替換。對於任何 `NEW` 的參照，
系統會在原始查詢的目標清單中，搜尋
對應的項目。若找到，該項目的運算式就會取代該
參照。否則，`NEW` 的意義就等同於
`OLD`（對 `UPDATE` 而言），
或會被替換為 null 值（對 `INSERT` 而言）。任何對
`OLD` 的參照，都會被替換為對作為結果關係
的範圍表項目的參照。

系統完成套用更新規則後，會對所產生的查詢樹
套用檢視表規則。由於檢視表無法插入新的更新動作，
因此不需要對檢視表重寫的輸出結果，再套用一次更新規則。

<a id="RULES-UPDATE-HOW-FIRST"></a>

#### 39.4.1.1. 逐步說明第一條規則 [#](#RULES-UPDATE-HOW-FIRST)

假設我們想追蹤 `shoelace_data` 關係中
`sl_avail` 欄位的變更。因此，我們建立一個記錄
資料表，以及一條規則，在對
`shoelace_data` 執行 `UPDATE`
時，有條件地寫入一筆記錄項目。

```

CREATE TABLE shoelace_log (
    sl_name    text,          -- shoelace changed
    sl_avail   integer,       -- new available value
    log_who    text,          -- who did it
    log_when   timestamp      -- when
);

CREATE RULE log_shoelace AS ON UPDATE TO shoelace_data
    WHERE NEW.sl_avail <> OLD.sl_avail
    DO INSERT INTO shoelace_log VALUES (
                                    NEW.sl_name,
                                    NEW.sl_avail,
                                    current_user,
                                    current_timestamp
                                );
```

現在，有人執行了：

```

UPDATE shoelace_data SET sl_avail = 6 WHERE sl_name = 'sl7';
```

接著我們來看看記錄資料表：

```

SELECT * FROM shoelace_log;

 sl_name | sl_avail | log_who | log_when
---------+----------+---------+----------------------------------
 sl7     |        6 | Al      | Tue Oct 20 16:14:45 1998 MET DST
(1 row)
```

這正是我們所預期的。以下是幕後所發生的事情。
剖析器建立了以下查詢樹：

```

UPDATE shoelace_data SET sl_avail = 6
  FROM shoelace_data shoelace_data
 WHERE shoelace_data.sl_name = 'sl7';
```

有一條規則 `log_shoelace`，它是 `ON UPDATE`，
其規則限定條件運算式為：

```

NEW.sl_avail <> OLD.sl_avail
```

其動作為：

```

INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old;
```

（這看起來有點奇怪，因為您通常無法這樣寫
`INSERT ... VALUES ... FROM`。這裡的 `FROM`
子句，只是用來表示查詢樹中，
存在著 `new` 與 `old` 的範圍表項目。
之所以需要它們，是為了讓
`INSERT` 指令查詢樹中的變數能夠參照它們。）

這條規則是一條帶限定條件的 `ALSO` 規則，因此規則系統
必須傳回兩棵查詢樹：修改後的規則動作，以及原始的
查詢樹。在步驟 1 中，原始查詢的範圍表，會被
併入規則動作的查詢樹中。結果為：

```

INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data;
```

在步驟 2 中，規則限定條件會被加入其中，因此
結果集會被限制在 `sl_avail` 有變化的資料列：

```

INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE new.sl_avail <> old.sl_avail;
```

（這看起來更奇怪了，因為 `INSERT ... VALUES` 也
沒有 `WHERE` 子句，但規劃器與執行器
處理起來並不會有困難。因為它們無論如何都需要支援
`INSERT ... SELECT` 的相同功能。）

在步驟 3 中，原始查詢樹的限定條件會被加入，
將結果集進一步限制在原始查詢
本應觸及的資料列：

```

INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE new.sl_avail <> old.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

步驟 4 將 `NEW` 的參照，替換為原始查詢樹的
目標清單項目，或替換為結果關係中
相符的變數參照：

```

INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE 6 <> old.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

步驟 5 將 `OLD` 的參照，改為結果關係的參照：

```

INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE 6 <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

就是這樣。由於這條規則是 `ALSO`，我們也會
輸出原始查詢樹。簡而言之，規則系統
輸出的，是一份包含兩棵查詢樹的清單，對應到
以下的陳述式：

```

INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data
 WHERE 6 <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';

UPDATE shoelace_data SET sl_avail = 6
 WHERE sl_name = 'sl7';
```

它們會依照這個順序執行，這正是
該規則所要達成的目的。

這些替換動作與所加入的限定條件，
確保了若原始查詢改為：

```

UPDATE shoelace_data SET sl_color = 'green'
 WHERE sl_name = 'sl7';
```

就不會寫入任何記錄項目。在這種情況下，原始的
查詢樹中，不包含 `sl_avail` 的目標清單項目，
因此 `NEW.sl_avail` 會被替換為
`shoelace_data.sl_avail`。因此，這條規則所產生的
額外指令為：

```

INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, shoelace_data.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data
 WHERE shoelace_data.sl_avail <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

而這個限定條件永遠不會為真。

它同樣也能在原始查詢修改多筆資料列時正常運作。因此
若有人執行了以下指令：

```

UPDATE shoelace_data SET sl_avail = 0
 WHERE sl_color = 'black';
```

實際上有四筆資料列會被更新（`sl1`、`sl2`、`sl3` 與 `sl4`）。
但 `sl3` 原本就已經是 `sl_avail = 0`。在這種情況下，
原始查詢樹的限定條件不同，因此
產生的額外查詢樹為：

```

INSERT INTO shoelace_log
SELECT shoelace_data.sl_name, 0,
       current_user, current_timestamp
  FROM shoelace_data
 WHERE 0 <> shoelace_data.sl_avail
   AND shoelace_data.sl_color = 'black';
```

這是由該規則所產生的。這個查詢樹，必定會插入
三筆新的記錄項目。而這是完全正確的。

在這裡，我們可以看出為什麼原始查詢樹
最後才執行是重要的。若 `UPDATE` 先
執行，所有的資料列都已經被設為零，因此
負責記錄的 `INSERT`，就不會找到任何符合
`0 <> shoelace_data.sl_avail` 的資料列。

<a id="RULES-UPDATE-VIEWS"></a>

### 39.4.2. 與檢視表的協同運作 [#](#RULES-UPDATE-VIEWS)

<a id="id-1.8.6.9.8.2"></a>

要防範有人試圖對檢視表關係執行
`INSERT`、`UPDATE` 或 `DELETE`，
一種簡單的做法，是讓這些查詢樹被
丟棄。因此我們可以建立以下規則：

```

CREATE RULE shoe_ins_protect AS ON INSERT TO shoe
    DO INSTEAD NOTHING;
CREATE RULE shoe_upd_protect AS ON UPDATE TO shoe
    DO INSTEAD NOTHING;
CREATE RULE shoe_del_protect AS ON DELETE TO shoe
    DO INSTEAD NOTHING;
```

若現在有人試圖對檢視表關係 `shoe`
執行上述任一種操作，規則系統就會
套用這些規則。由於這些規則
沒有動作，且是 `INSTEAD`，最終產生的
查詢樹清單會是空的，整個查詢也會
變成什麼都沒有，因為在規則系統處理完它之後，
已經沒有東西需要規劃或執行了。

使用規則系統更精巧的做法，是
建立規則，將查詢樹重寫成
對真正資料表執行正確操作的查詢樹。要在
`shoelace` 檢視表上做到這一點，我們
建立以下規則：

```

CREATE RULE shoelace_ins AS ON INSERT TO shoelace
    DO INSTEAD
    INSERT INTO shoelace_data VALUES (
           NEW.sl_name,
           NEW.sl_avail,
           NEW.sl_color,
           NEW.sl_len,
           NEW.sl_unit
    );

CREATE RULE shoelace_upd AS ON UPDATE TO shoelace
    DO INSTEAD
    UPDATE shoelace_data
       SET sl_name = NEW.sl_name,
           sl_avail = NEW.sl_avail,
           sl_color = NEW.sl_color,
           sl_len = NEW.sl_len,
           sl_unit = NEW.sl_unit
     WHERE sl_name = OLD.sl_name;

CREATE RULE shoelace_del AS ON DELETE TO shoelace
    DO INSTEAD
    DELETE FROM shoelace_data
     WHERE sl_name = OLD.sl_name;
```

若您想要在該檢視表上支援 `RETURNING`
查詢，就需要讓規則包含能計算出檢視表資料列的
`RETURNING` 子句。對於單一資料表上的
檢視表而言，這通常相當直觀，但對於像
`shoelace` 這樣的聯結檢視表而言，就有點繁瑣了。
以下是插入案例的一個範例：

```

CREATE RULE shoelace_ins AS ON INSERT TO shoelace
    DO INSTEAD
    INSERT INTO shoelace_data VALUES (
           NEW.sl_name,
           NEW.sl_avail,
           NEW.sl_color,
           NEW.sl_len,
           NEW.sl_unit
    )
    RETURNING
           shoelace_data.*,
           (SELECT shoelace_data.sl_len * u.un_fact
            FROM unit u WHERE shoelace_data.sl_unit = u.un_name);
```

請注意，這一條規則同時支援了對該檢視表的
`INSERT` 與 `INSERT RETURNING` 查詢 —
對於 `INSERT`，`RETURNING` 子句
單純會被忽略。

請注意，在規則的 `RETURNING` 子句中，
`OLD` 與 `NEW`
指的是作為額外範圍表項目，加入重寫後查詢中的
虛擬關係，而不是結果關係中的新／舊資料列。因此，
舉例來說，在一條支援對該檢視表執行 `UPDATE`
查詢的規則中，若 `RETURNING` 子句中包含
`old.sl_name`，則永遠會傳回舊的名稱，
無論該檢視表查詢中的 `RETURNING` 子句
指定的是 `OLD` 還是 `NEW`，
這可能會造成混淆。為了避免這種混淆，並支援在
該檢視表的查詢中傳回新舊值，規則定義中的
`RETURNING` 子句，應該參照結果
關係中的項目，例如 `shoelace_data.sl_name`，
而不要指定 `OLD` 或 `NEW`。

現在假設，每隔一段時間，店裡就會送來一批鞋帶，
附帶一張很大的零件清單。但您不想每次都
手動更新 `shoelace` 檢視表。因此，
我們設定了兩個小資料表：一個用來讓您
插入零件清單中的項目，另一個則帶有一個特殊的
技巧。建立這些資料表的指令如下：

```

CREATE TABLE shoelace_arrive (
    arr_name    text,
    arr_quant   integer
);

CREATE TABLE shoelace_ok (
    ok_name     text,
    ok_quant    integer
);

CREATE RULE shoelace_ok_ins AS ON INSERT TO shoelace_ok
    DO INSTEAD
    UPDATE shoelace
       SET sl_avail = sl_avail + NEW.ok_quant
     WHERE sl_name = NEW.ok_name;
```

現在，您可以將零件清單的資料，
填入資料表 `shoelace_arrive` 中：

```

SELECT * FROM shoelace_arrive;

 arr_name | arr_quant
----------+-----------
 sl3      |        10
 sl6      |        20
 sl8      |        20
(3 rows)
```

先快速看一下目前的資料：

```

SELECT * FROM shoelace;

 sl_name  | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
----------+----------+----------+--------+---------+-----------
 sl1      |        5 | black    |     80 | cm      |        80
 sl2      |        6 | black    |    100 | cm      |       100
 sl7      |        6 | brown    |     60 | cm      |        60
 sl3      |        0 | black    |     35 | inch    |      88.9
 sl4      |        8 | black    |     40 | inch    |     101.6
 sl8      |        1 | brown    |     40 | inch    |     101.6
 sl5      |        4 | brown    |      1 | m       |       100
 sl6      |        0 | brown    |    0.9 | m       |        90
(8 rows)
```

現在，將送到的鞋帶移入：

```

INSERT INTO shoelace_ok SELECT * FROM shoelace_arrive;
```

並檢查結果：

```

SELECT * FROM shoelace ORDER BY sl_name;

 sl_name  | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
----------+----------+----------+--------+---------+-----------
 sl1      |        5 | black    |     80 | cm      |        80
 sl2      |        6 | black    |    100 | cm      |       100
 sl7      |        6 | brown    |     60 | cm      |        60
 sl4      |        8 | black    |     40 | inch    |     101.6
 sl3      |       10 | black    |     35 | inch    |      88.9
 sl8      |       21 | brown    |     40 | inch    |     101.6
 sl5      |        4 | brown    |      1 | m       |       100
 sl6      |       20 | brown    |    0.9 | m       |        90
(8 rows)

SELECT * FROM shoelace_log;

 sl_name | sl_avail | log_who| log_when
---------+----------+--------+----------------------------------
 sl7     |        6 | Al     | Tue Oct 20 19:14:45 1998 MET DST
 sl3     |       10 | Al     | Tue Oct 20 19:25:16 1998 MET DST
 sl6     |       20 | Al     | Tue Oct 20 19:25:16 1998 MET DST
 sl8     |       21 | Al     | Tue Oct 20 19:25:16 1998 MET DST
(4 rows)
```

從一則 `INSERT ... SELECT` 到得出這些結果，
中間經歷了很長的一段路。而對這個查詢樹
轉換過程的說明，也將是本章的最後一段。首先，
是剖析器的輸出：

```

INSERT INTO shoelace_ok
SELECT shoelace_arrive.arr_name, shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok;
```

現在，第一條規則 `shoelace_ok_ins` 被套用，
將它轉變為：

```

UPDATE shoelace
   SET sl_avail = shoelace.sl_avail + shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace
 WHERE shoelace.sl_name = shoelace_arrive.arr_name;
```

並捨棄了原本對 `shoelace_ok` 的
`INSERT`。這個重寫後的查詢，會再次被交給
規則系統，接著套用的第二條規則
`shoelace_upd` 產生了：

```

UPDATE shoelace_data
   SET sl_name = shoelace.sl_name,
       sl_avail = shoelace.sl_avail + shoelace_arrive.arr_quant,
       sl_color = shoelace.sl_color,
       sl_len = shoelace.sl_len,
       sl_unit = shoelace.sl_unit
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data
 WHERE shoelace.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = shoelace.sl_name;
```

這同樣是一條 `INSTEAD` 規則，先前的查詢樹會被捨棄。
請注意，這個查詢仍然使用了 `shoelace` 檢視表。
但規則系統在這一步還沒有結束，因此會繼續
對它套用 `_RETURN` 規則，於是我們得到：

```

UPDATE shoelace_data
   SET sl_name = s.sl_name,
       sl_avail = s.sl_avail + shoelace_arrive.arr_quant,
       sl_color = s.sl_color,
       sl_len = s.sl_len,
       sl_unit = s.sl_unit
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data,
       shoelace old, shoelace new,
       shoelace_data s, unit u
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name;
```

最後，規則 `log_shoelace` 被套用，
產生了額外的查詢樹：

```

INSERT INTO shoelace_log
SELECT s.sl_name,
       s.sl_avail + shoelace_arrive.arr_quant,
       current_user,
       current_timestamp
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data,
       shoelace old, shoelace new,
       shoelace_data s, unit u,
       shoelace_data old, shoelace_data new
       shoelace_log shoelace_log
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name
   AND (s.sl_avail + shoelace_arrive.arr_quant) <> s.sl_avail;
```

在那之後，規則系統已經沒有規則可以套用了，
於是傳回所產生的查詢樹。

因此，我們最終得到兩棵最終查詢樹，
等同於以下的 SQL 陳述式：

```

INSERT INTO shoelace_log
SELECT s.sl_name,
       s.sl_avail + shoelace_arrive.arr_quant,
       current_user,
       current_timestamp
  FROM shoelace_arrive shoelace_arrive, shoelace_data shoelace_data,
       shoelace_data s
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name
   AND s.sl_avail + shoelace_arrive.arr_quant <> s.sl_avail;

UPDATE shoelace_data
   SET sl_avail = shoelace_data.sl_avail + shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive,
       shoelace_data shoelace_data,
       shoelace_data s
 WHERE s.sl_name = shoelace_arrive.sl_name
   AND shoelace_data.sl_name = s.sl_name;
```

其結果是，資料從一個關係插入另一個關係，
接著被轉換成對第三個關係的更新，
再轉換成對第四個關係的更新，
外加把這次最終更新記錄到第五個關係，
最終被歸納成兩則查詢。

這裡有一個有點不美觀的小細節。觀察這兩則
查詢，可以發現，範圍表中出現了兩次
`shoelace_data` 關係，而它原本
應該可以精簡成一次。規劃器並不會處理這一點，
因此規則系統對 `INSERT` 所輸出結果的執行計畫，
會是：

```

Nested Loop
  ->  Merge Join
        ->  Seq Scan
              ->  Sort
                    ->  Seq Scan on s
        ->  Seq Scan
              ->  Sort
                    ->  Seq Scan on shoelace_arrive
  ->  Seq Scan on shoelace_data
```

而若省略那個多餘的範圍表項目，
則會得到：

```

Merge Join
  ->  Seq Scan
        ->  Sort
              ->  Seq Scan on s
  ->  Seq Scan
        ->  Sort
              ->  Seq Scan on shoelace_arrive
```

這會在記錄資料表中，產生完全相同的項目。因此，
規則系統在資料表 `shoelace_data` 上，
額外進行了一次完全不必要的掃描。而在
`UPDATE` 中，同樣的多餘掃描，又發生了一次。
但要讓這一切都能夠實現，實在是一件相當困難的工作。

現在，讓我們對
PostgreSQL 規則系統及其威力，做最後一次展示。
假設您在資料庫中，加入了一些顏色很特別的鞋帶：

```

INSERT INTO shoelace VALUES ('sl9', 0, 'pink', 35.0, 'inch', 0.0);
INSERT INTO shoelace VALUES ('sl10', 1000, 'magenta', 40.0, 'inch', 0.0);
```

我們想要建立一個檢視表，來檢查哪些
`shoelace` 項目，在顏色上沒有任何鞋子相符。
這個檢視表如下：

```

CREATE VIEW shoelace_mismatch AS
    SELECT * FROM shoelace WHERE NOT EXISTS
        (SELECT shoename FROM shoe WHERE slcolor = sl_color);
```

其輸出為：

```

SELECT * FROM shoelace_mismatch;

 sl_name | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
---------+----------+----------+--------+---------+-----------
 sl9     |        0 | pink     |     35 | inch    |      88.9
 sl10    |     1000 | magenta  |     40 | inch    |     101.6
```

現在，我們想要設定成，將那些沒有現貨、
且顏色不相符的鞋帶，從資料庫中刪除。
為了讓事情對 PostgreSQL 來說更難一點，
我們不直接刪除它。而是再建立一個檢視表：

```

CREATE VIEW shoelace_can_delete AS
    SELECT * FROM shoelace_mismatch WHERE sl_avail = 0;
```

並像這樣執行：

```

DELETE FROM shoelace WHERE EXISTS
    (SELECT * FROM shoelace_can_delete
             WHERE sl_name = shoelace.sl_name);
```

結果如下：

```

SELECT * FROM shoelace;

 sl_name | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
---------+----------+----------+--------+---------+-----------
 sl1     |        5 | black    |     80 | cm      |        80
 sl2     |        6 | black    |    100 | cm      |       100
 sl7     |        6 | brown    |     60 | cm      |        60
 sl4     |        8 | black    |     40 | inch    |     101.6
 sl3     |       10 | black    |     35 | inch    |      88.9
 sl8     |       21 | brown    |     40 | inch    |     101.6
 sl10    |     1000 | magenta  |     40 | inch    |     101.6
 sl5     |        4 | brown    |      1 | m       |       100
 sl6     |       20 | brown    |    0.9 | m       |        90
(9 rows)
```

一個對檢視表執行的 `DELETE`，其子查詢限定條件
總共用到了 4 個巢狀／聯結的檢視表，其中一個
本身又帶有包含某個檢視表的子查詢限定條件，
而且還使用了計算出來的檢視表欄位，
最終被重寫成
單獨一棵查詢樹，直接從一個真正的資料表中，
刪除所要求的資料。

在現實世界中，大概只有少數情況
真的需要這樣的結構。但這樣的結果，
確實能讓人對它的可靠運作感到放心。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules-update.html)（原文版本：18.6；核對日期：2026-09-16）
