<a id="SYSTEM-CATALOG-INITIAL-DATA"></a>

## 68.2. 系統目錄初始資料 [#](#system-catalog-initial-data) <a href="#system-catalog-initial-data" id="system-catalog-initial-data"></a>

[68.2.1. 資料檔格式](system-catalog-initial-data.md#SYSTEM-CATALOG-INITIAL-DATA-FORMAT)

[68.2.2. OID 指派](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-ASSIGNMENT)

[68.2.3. OID 參照查找](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-REFERENCES)

[68.2.4. 自動建立陣列型別](system-catalog-initial-data.md#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)

[68.2.5. 編輯資料檔的訣竅](system-catalog-initial-data.md#SYSTEM-CATALOG-RECIPES)

每個具有手動建立之初始資料的目錄（有些目錄沒有），
都有一個對應的 `.dat` 檔案，以可編輯的格式存放其初始資料。

<a id="SYSTEM-CATALOG-INITIAL-DATA-FORMAT"></a>

### 68.2.1. 資料檔格式 [#](#SYSTEM-CATALOG-INITIAL-DATA-FORMAT)

每個 `.dat` 檔案都包含 Perl 資料結構字面值，
這些字面值只會直接以 Perl 的 eval 求值，產生記憶體中的資料結構；
該資料結構是由雜湊參照（hash reference）組成的陣列，每筆目錄資料列對應一個雜湊參照。
以下是取自 `pg_database.dat` 並稍加修改的摘錄，
可展示其主要特性：

```

[

# A comment could appear here.
{ oid => '1', oid_symbol => 'Template1DbOid',
  descr => 'database\'s default template',
  datname => 'template1', encoding => 'ENCODING',
  datlocprovider => 'LOCALE_PROVIDER', datistemplate => 't',
  datallowconn => 't', dathasloginevt => 'f', datconnlimit => '-1', datfrozenxid => '0',
  datminmxid => '1', dattablespace => 'pg_default', datcollate => 'LC_COLLATE',
  datctype => 'LC_CTYPE', datlocale => 'DATLOCALE', datacl => '_null_' },

]
```

需要注意的要點：

* 整體檔案配置為：左方括號、一組或多組大括號（每組代表一筆目錄資料列）、
  右方括號。在每個右大括號之後寫一個逗號。
* 在每筆目錄資料列中，寫入以逗號分隔的
  *`key`* `=>`
  *`value`* 配對。
  允許的 *`key`* 為目錄的欄位名稱，
  再加上中繼資料鍵 `oid`、
  `oid_symbol`、
  `array_type_oid` 與 `descr`。
  （`oid` 與 `oid_symbol`
  的用法說明於下方的[第 68.2.2 節](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-ASSIGNMENT)，
  而 `array_type_oid` 則說明於
  [第 68.2.4 節](system-catalog-initial-data.md#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)。
  `descr` 為物件提供描述字串，
  該字串會視情況插入 `pg_description`
  或 `pg_shdescription` 中。）
  雖然中繼資料鍵是選擇性的，但目錄所定義的欄位都必須提供，
  除非目錄的 `.h` 檔案為該欄位指定了預設值。
  （在上面的範例中，`datdba` 欄位被省略了，
  因為 `pg_database.h` 為它提供了適當的預設值。）
* 所有值都必須以單引號括住。值中使用的單引號要以反斜線跳脫。
  作為資料的反斜線可以（但不一定需要）重複寫兩次；這遵循 Perl 對簡單引號字面值的規則。
  請注意，作為資料出現的反斜線會被初始建置（bootstrap）掃描器視為跳脫字元，
  所依循的規則與跳脫字串常數相同
  （請參閱[第 4.1.2.2 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE)）；
  例如 `\t` 會轉換為定位字元。如果你確實想在最終的值中放入一個反斜線，
  就需要寫四個：Perl 會去掉兩個，留下 `\\` 給
  初始建置掃描器處理。
* null 值以 `_null_` 表示。
  （請注意，沒有辦法建立恰好就是該字串的值。）
* 註解以 `#` 開頭，且必須獨立成行。
* 值為其他目錄項目 OID 的欄位，應該以符號名稱表示，
  而不是實際的數值 OID。
  （在上面的範例中，`dattablespace`
  就含有這樣的參照。）
  這會在下方的[第 68.2.3 節](system-catalog-initial-data.md#SYSTEM-CATALOG-OID-REFERENCES)中說明。
* 由於雜湊是無序的資料結構，欄位順序與行的配置在語意上並不重要。
  不過，為了維持一致的外觀，我們訂定了幾條規則，
  由格式化腳本 `reformat_dat_file.pl` 套用：

  * 在每對大括號中，中繼資料欄位
    `oid`、`oid_symbol`、
    `array_type_oid` 與 `descr`
    （若有的話）依此順序排在最前面，接著目錄本身的欄位依其定義順序出現。
  * 會視需要在欄位之間插入換行，以盡可能將行長限制在 80 個字元以內。
    中繼資料欄位與一般欄位之間也會插入換行。
  * 若目錄的 `.h` 檔案為某個欄位指定了預設值，
    而某筆資料項目具有相同的值，
    `reformat_dat_file.pl` 會將它從資料檔中省略。
    這能讓資料的表示保持精簡。
  * `reformat_dat_file.pl` 會原樣保留空白行與註解行。

  建議在送出目錄資料的修補程式（patch）之前，先執行 `reformat_dat_file.pl`。
  為了方便起見，你只需切換到 `src/include/catalog/` 並
  執行 `make reformat-dat-files` 即可。
* 如果你想新增一種讓資料表示更精簡的方法，就必須在
  `reformat_dat_file.pl` 中實作它，同時也要讓
  `Catalog::ParseData()` 知道如何將資料展開回完整的表示形式。

<a id="SYSTEM-CATALOG-OID-ASSIGNMENT"></a>

### 68.2.2. OID 指派 [#](#SYSTEM-CATALOG-OID-ASSIGNMENT)

初始資料中出現的目錄資料列，可以藉由寫入 `oid
=> nnnn` 中繼資料欄位，給予手動指派的 OID。
此外，若已指派 OID，可以藉由寫入 `oid_symbol
=> name` 中繼資料欄位，為該 OID 建立 C 巨集。

若其他預先載入的資料列中有對某些預先載入資料列的 OID 參照，
這些被參照的資料列就必須有預先指派的 OID。若資料列的 OID 必須從 C 程式碼中參照，
也需要預先指派 OID。
若兩種情況都不適用，則可以省略 `oid` 中繼資料欄位，
此時初始建置程式碼會自動指派 OID。
實務上，對於某個目錄中的預先載入資料列，我們通常會為全部資料列預先指派 OID，
或全部都不指派，即使實際上只有其中一部分被交叉參照也是如此。

在 C 程式碼中寫入任何 OID 的實際數值被認為是非常不好的寫法；
請一律改用巨集。直接參照 `pg_proc` OID 的情況相當常見，
因此有一套特殊機制可以自動建立所需的巨集；
請參閱 `src/backend/utils/Gen_fmgrtab.pl`。同樣地——
不過基於歷史因素，作法並不相同——
也有一種自動建立 `pg_type`
OID 巨集的方法。因此，這兩個目錄中不需要 `oid_symbol` 項目。
同樣地，系統目錄與索引的 `pg_class` OID 巨集也會自動設定。
對於其他所有系統目錄，你都必須透過 `oid_symbol` 項目，
手動指定你所需要的任何巨集。

要為新的預先載入資料列找到可用的 OID，請執行腳本
`src/include/catalog/unused_oids`。
它會列出未使用 OID 的範圍（包含兩端點；例如，輸出行
`45-900` 表示 OID 45 到 900 尚未被配置）。
目前 OID 1–9999 保留給手動指派使用；
`unused_oids` 腳本只是查看目錄標頭檔與 `.dat` 檔案，
看看哪些 OID 沒有出現。你也可以使用
`duplicate_oids` 腳本來檢查錯誤。
（`genbki.pl` 會為任何未手動指派 OID 的資料列指派 OID，
而且也會在編譯時期偵測重複的 OID。）

為預期不會立即被提交的修補程式選擇 OID 時，最佳做法是使用一組
大致連續的 OID，並以 8000—9999 範圍內隨機選擇的某個值作為起點。
這可以將與其他同時開發中的修補程式發生 OID 衝突的風險降到最低。
為了讓 8000—9999 範圍保持可供開發使用，在修補程式被提交到
主要（master）git 儲存庫之後，應該將它的 OID 重新編號到該範圍以下的可用空間。
這通常會在每個開發週期接近尾聲時進行，
一次移動該週期中所有已提交修補程式所使用的 OID。
腳本 `renumber_oids.pl` 可用於此目的。
如果發現某個尚未提交的修補程式與某個最近提交的修補程式有 OID 衝突，
`renumber_oids.pl` 也可能有助於從這種情況中恢復。

由於有這種可能會對修補程式所指派的 OID 重新編號的慣例，
在修補程式被納入正式發行版之前，不應將它所指派的 OID 視為穩定的。
不過，一旦發行之後，我們就不會變更手動指派的物件 OID，
因為那會造成各種相容性問題。

若 `genbki.pl` 需要為沒有手動指派 OID 的目錄項目指派 OID，
它會使用 10000—11999 範圍內的值。
伺服器的 OID 計數器在初始建置執行開始時會被設為 10000，
因此在初始建置處理期間即時建立的任何物件，也會取得此範圍內的 OID。
（一般的 OID 指派機制會負責防止任何衝突。）

OID 低於 `FirstUnpinnedObjectId`（12000）的物件
被視為「固定的」（pinned），以防止它們被刪除。
（有少數例外，這些例外直接寫死在 `IsPinnedObject()` 中。）
initdb 一旦準備好建立非固定物件，就會將 OID 計數器推進到
`FirstUnpinnedObjectId`。因此，在 initdb 後期階段建立的物件，
例如執行 `information_schema.sql` 腳本時建立的物件，
不會是固定的，而 `genbki.pl` 所知道的所有物件
則都會是固定的。

在一般資料庫運作期間指派的 OID 會被限制為
16384 以上。這確保了 10000—16383 的範圍
可以保留給由 `genbki.pl` 或在 initdb 期間自動指派的 OID 使用。
這些自動指派的 OID 不被視為穩定的，
而且可能在不同的安裝之間有所不同。

<a id="SYSTEM-CATALOG-OID-REFERENCES"></a>

### 68.2.3. OID 參照查找 [#](#SYSTEM-CATALOG-OID-REFERENCES)

原則上，從一筆初始目錄資料列到另一筆的交叉參照，
只要在參照欄位中寫入被參照資料列的預先指派 OID 即可。
然而，這違反專案政策，因為這種做法容易出錯、難以閱讀，
而且若新指派的 OID 被重新編號就可能失效。因此，
`genbki.pl` 提供了改以符號參照撰寫的機制。
規則如下：

* 在特定的目錄欄位上啟用符號參照的方式，是在該欄位的定義附加
  `BKI_LOOKUP(lookuprule)`，其中 *`lookuprule`*
  是被參照目錄的名稱，例如 `pg_proc`。
  `BKI_LOOKUP` 可以附加到型別為
  `Oid`、`regproc`、`oidvector`
  或 `Oid[]` 的欄位；在後兩種情況下，它表示會對陣列的每個元素進行查找。
* 也允許將 `BKI_LOOKUP(encoding)`
  附加到整數欄位，以參照字元集編碼；這些編碼目前並未以目錄 OID 表示，
  但具有一組 `genbki.pl` 已知的值。
* 在某些目錄欄位中，允許項目為零而不是有效的參照。
  若允許這樣做，請寫
  `BKI_LOOKUP_OPT` 而不是
  `BKI_LOOKUP`。這樣你就可以為項目寫入
  `0`。（若該欄位宣告為
  `regproc`，你可以選擇改寫
  `-` 而不是 `0`。）
  除了這種特殊情況之外，
  `BKI_LOOKUP` 欄位中的所有項目都必須是符號參照。
  `genbki.pl` 會對無法辨識的名稱發出警告。
* 大多數種類的目錄物件只需以其名稱來參照。
  請注意，型別名稱必須與被參照之
  `pg_type`
  項目的 `typname` 完全相符；你不能使用
  任何別名，例如以 `integer`
  代替 `int4`。
* 函式可以用它的 `proname` 來表示，前提是該名稱在
  `pg_proc.dat` 的項目中是唯一的（這與 regproc
  輸入的運作方式相同）。否則，請將它寫成
  *`proname(argtypename,argtypename,...)`*，
  如同 regprocedure。引數型別名稱的拼寫必須與
  `pg_proc.dat` 項目之
  `proargtypes` 欄位中的完全相同。不要插入任何
  空白。
* 運算子以
  *`oprname(lefttype,righttype)`* 表示，
  型別名稱的寫法須與
  `pg_operator.dat`
  項目之 `oprleft`
  與 `oprright` 欄位中的完全相同。
  （對於一元運算子省略的運算元，請寫 `0`。）
* 運算子類別與運算子家族的名稱只在同一個存取方法內是唯一的，
  因此它們以 *`access_method_name`*`/`*`object_name`* 表示。
* 以上這些情況都沒有提供任何綱要限定的機制；
  初始建置期間建立的所有物件都預期位於
  `pg_catalog` 綱要中。

`genbki.pl` 會在執行時解析所有符號參照，
並將單純的數值 OID 放入輸出的 BKI 檔案中。因此，
初始建置用後端不需要處理符號參照。

即使目錄沒有需要查找的初始資料，最好仍以
`BKI_LOOKUP` 或 `BKI_LOOKUP_OPT`
標記 OID 參照欄位。這讓 `genbki.pl` 能夠記錄
系統目錄中存在的外鍵關係。這些資訊會在迴歸測試中
用來檢查不正確的項目。另請參閱巨集
`DECLARE_FOREIGN_KEY`、
`DECLARE_FOREIGN_KEY_OPT`、
`DECLARE_ARRAY_FOREIGN_KEY`
與 `DECLARE_ARRAY_FOREIGN_KEY_OPT`，它們用於宣告
對 `BKI_LOOKUP` 而言過於複雜的外鍵關係
（通常是多欄位外鍵）。

<a id="SYSTEM-CATALOG-AUTO-ARRAY-TYPES"></a>

### 68.2.4. 自動建立陣列型別 [#](#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)

大多數純量資料型別都應該有對應的陣列型別（也就是一個標準的 varlena
陣列型別，其元素型別為該純量型別，並且由該純量型別之 `pg_type`
項目中的 `typarray` 欄位所參照）。
在大多數情況下，`genbki.pl` 都能自動為該陣列型別
產生 `pg_type` 項目。

要使用此功能，只需在該純量型別的 `pg_type` 項目中寫入 `array_type_oid
=> nnnn` 中繼資料欄位，
指定陣列型別要使用的 OID。接著你就可以省略
`typarray` 欄位，因為它會自動以該 OID 填入。

產生的陣列型別名稱，是在純量型別名稱前面加上一個底線。
陣列項目的其他欄位，會從 `pg_type.h` 中的
`BKI_ARRAY_DEFAULT(value)`
標註填入；若沒有該標註，則從純量型別複製。
（`typalign` 另有一個特殊情況。）接著，
這兩個項目的 `typelem`
與 `typarray` 欄位會被設定為互相參照。

<a id="SYSTEM-CATALOG-RECIPES"></a>

### 68.2.5. 編輯資料檔的訣竅 [#](#SYSTEM-CATALOG-RECIPES)

以下是一些建議，說明在更新目錄資料檔時，執行常見工作最簡單的方式。

**為目錄新增具有預設值的欄位：**
在標頭檔中加入該欄位，並附上
`BKI_DEFAULT(value)`
標註。資料檔只需在需要非預設值的現有資料列中
加入該欄位即可。

**為沒有預設值的現有欄位加入預設值：**
在標頭檔中加入 `BKI_DEFAULT` 標註，
然後執行 `make reformat-dat-files`，以移除
現在已多餘的欄位項目。

**移除欄位（無論它是否有預設值）：**
從標頭檔中移除該欄位，然後執行 `make
reformat-dat-files`，以移除現在已無用的欄位項目。

**變更或移除現有的預設值：**
你不能只變更標頭檔，因為那會導致目前的資料被錯誤地解讀。
請先執行 `make
expand-dat-files`，以明確插入所有預設值的方式改寫資料檔，
然後變更或移除 `BKI_DEFAULT` 標註，接著執行 `make
reformat-dat-files`，再次移除多餘的欄位。

**臨時性的大量編輯：**
`reformat_dat_file.pl` 可以加以修改，用來執行
許多種大量變更。請找出它的區塊註解，這些註解標示了可以插入
一次性程式碼的位置。在以下範例中，我們要將 `pg_proc`
中的兩個布林欄位合併為一個 char 欄位：

1. 將具有預設值的新欄位加入
   `pg_proc.h`：

   ```

   +    /* see PROKIND_ categories below */
   +    char        prokind BKI_DEFAULT(f);
   ```
2. 以 `reformat_dat_file.pl` 為基礎建立新的腳本，
   以即時插入適當的值：

   ```

   -           # At this point we have the full row in memory as a hash
   -           # and can do any operations we want. As written, it only
   -           # removes default values, but this script can be adapted to
   -           # do one-off bulk-editing.
   +           # One-off change to migrate to prokind
   +           # Default has already been filled in by now, so change to other
   +           # values as appropriate
   +           if ($values{proisagg} eq 't')
   +           {
   +               $values{prokind} = 'a';
   +           }
   +           elsif ($values{proiswindow} eq 't')
   +           {
   +               $values{prokind} = 'w';
   +           }
   ```
3. 執行新的腳本：

   ```

   $ cd src/include/catalog
   $ perl  rewrite_dat_with_prokind.pl  pg_proc.dat
   ```

   此時 `pg_proc.dat` 已具有全部三個
   欄位：`prokind`、
   `proisagg`
   與 `proiswindow`，不過它們只會出現在
   具有非預設值的資料列中。
4. 從 `pg_proc.h` 中移除舊的欄位：

   ```

   -    /* is it an aggregate? */
   -    bool        proisagg BKI_DEFAULT(f);
   -
   -    /* is it a window function? */
   -    bool        proiswindow BKI_DEFAULT(f);
   ```
5. 最後，執行 `make reformat-dat-files`，
   從 `pg_proc.dat` 中移除無用的舊項目。

若要參考更多用於大量編輯之腳本的範例，請參閱附加在此郵件中的
`convert_oid2name.pl`
與 `remove_pg_type_oid_symbols.pl`：
<https://www.postgresql.org/message-id/CAJVSVGVX8gXnPm+Xa=DxR7kFYprcQ1tNcCT5D0O3ShfnM6jehA@mail.gmail.com>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/system-catalog-initial-data.html)（原文版本：18.6；核對日期：2026-10-17）
