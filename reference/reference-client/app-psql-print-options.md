# psql：\pset 列印選項

[返回 psql 主頁](app-psql.md)。

<a id="APP-PSQL-META-COMMAND-PSET-BORDER"></a>

## `border` [#](#app-psql-meta-command-pset-border) <a href="#app-psql-meta-command-pset-border" id="app-psql-meta-command-pset-border"></a>

*`value`* 必須是一個數字。一般而言，數字越大，表格的框線與分隔線就越多，但細節取決於特定的格式。在 HTML 格式中，此值會直接轉換為 `border=...` 屬性。在其他大多數格式中，只有 0（無框線）、1（內部分隔線）與 2（表格外框）這幾個值有意義，大於 2 的值會被視同 `border = 2`。`latex` 與 `latex-longtable` 格式另外允許值 3，以在資料列之間加上分隔線。
<a id="APP-PSQL-META-COMMAND-PSET-COLUMNS"></a>

## `columns` [#](#app-psql-meta-command-pset-columns) <a href="#app-psql-meta-command-pset-columns" id="app-psql-meta-command-pset-columns"></a>

設定 `wrapped` 格式的目標寬度，同時也是判斷輸出是否寬到需要使用分頁程式，或在自動展開模式下切換為垂直顯示的寬度上限。零（預設值）表示目標寬度由環境變數 `COLUMNS` 控制；若未設定 `COLUMNS`，則由偵測到的螢幕寬度控制。此外，若 `columns` 為零，則 `wrapped` 格式只影響螢幕輸出。若 `columns` 不為零，則檔案與管線輸出也會換行到該寬度。
<a id="APP-PSQL-META-COMMAND-PSET-CSV-FIELDSEP"></a>

## `csv_fieldsep` [#](#app-psql-meta-command-pset-csv-fieldsep) <a href="#app-psql-meta-command-pset-csv-fieldsep" id="app-psql-meta-command-pset-csv-fieldsep"></a>

指定 CSV 輸出格式所使用的欄位分隔字元。若分隔字元出現在某個欄位的值中，該欄位會依標準 CSV 規則以雙引號括住輸出。預設為逗號。
<a id="APP-PSQL-META-COMMAND-PSET-EXPANDED"></a>

## `expanded`（或 `x`） [#](#app-psql-meta-command-pset-expanded) <a href="#app-psql-meta-command-pset-expanded" id="app-psql-meta-command-pset-expanded"></a>

若指定了 *`value`*，它必須是 `on` 或 `off`（分別啟用或停用展開模式），或是 `auto`。若省略 *`value`*，此命令會在 on 與 off 設定之間切換。啟用展開模式時，查詢結果會以兩個欄位顯示，左邊是欄位名稱，右邊是資料。若資料在一般的「水平」模式下無法放進螢幕，此模式就很有用。在 auto 設定下，只要查詢輸出有超過一個欄位且寬度超過螢幕，就會使用展開模式；否則使用一般模式。auto 設定只在對齊（aligned）與換行（wrapped）格式中有效。在其他格式中，它的行為一律如同展開模式為關閉。
<a id="APP-PSQL-META-COMMAND-PSET-FIELDSEP"></a>

## `fieldsep` [#](#app-psql-meta-command-pset-fieldsep) <a href="#app-psql-meta-command-pset-fieldsep" id="app-psql-meta-command-pset-fieldsep"></a>

指定非對齊輸出格式所使用的欄位分隔字元。如此一來，就可以建立例如其他程式可能偏好的定位字元（tab）分隔輸出。若要將定位字元設為欄位分隔字元，請輸入 `\pset fieldsep
'\t'`。預設的欄位分隔字元是 `'|'`（垂直線）。
<a id="APP-PSQL-META-COMMAND-PSET-FIELDSEP-ZERO"></a>

## `fieldsep_zero` [#](#app-psql-meta-command-pset-fieldsep-zero) <a href="#app-psql-meta-command-pset-fieldsep-zero" id="app-psql-meta-command-pset-fieldsep-zero"></a>

將非對齊輸出格式所使用的欄位分隔字元設為值為 0 的位元組（NUL）。
<a id="APP-PSQL-META-COMMAND-PSET-FOOTER"></a>

## `footer` [#](#app-psql-meta-command-pset-footer) <a href="#app-psql-meta-command-pset-footer" id="app-psql-meta-command-pset-footer"></a>

若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用表格頁尾（`(n rows)` 計數）的顯示。若省略 *`value`*，此命令會切換頁尾顯示的開關。
<a id="APP-PSQL-META-COMMAND-PSET-FORMAT"></a>

## `format` [#](#app-psql-meta-command-pset-format) <a href="#app-psql-meta-command-pset-format" id="app-psql-meta-command-pset-format"></a>

將輸出格式設為 `aligned`、`asciidoc`、`csv`、`html`、`latex`、`latex-longtable`、`troff-ms`、`unaligned` 或 `wrapped` 其中之一。允許使用不產生歧義的縮寫。

`aligned` 格式是標準、人類可讀、排版整齊的文字輸出；這是預設格式。

`unaligned` 格式會將一筆資料列的所有欄位寫在同一行，並以目前生效的欄位分隔字元分隔。這對於建立可能要給其他程式讀取的輸出很有用，例如定位字元分隔或逗號分隔的格式。不過，若欄位分隔字元出現在某個欄位的值中，並不會受到特別處理；因此 CSV 格式可能更適合這類用途。

`csv` 格式
<a id="id-1.9.4.21.8.4.11.1.81.2.3.1.8.2.4.2"></a>
會寫出以逗號分隔的欄位值，並套用 [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180) 所描述的引號規則。此輸出與伺服器 `COPY` 命令的 CSV 格式相容。除非 `tuples_only` 參數為 `on`，否則會產生含有欄位名稱的標頭行。標題與頁尾不會印出。每筆資料列以系統相關的行尾字元結束；在類 Unix 系統上通常是單一換行字元（`\n`），在 Microsoft Windows 上則是歸位與換行字元序列（`\r\n`）。可以用 `\pset csv_fieldsep` 選擇逗號以外的欄位分隔字元。

`wrapped` 格式與 `aligned` 類似，但會將較寬的資料值換行到多行，使輸出符合目標欄寬。目標寬度依 `columns` 選項所述方式決定。請注意，psql 不會嘗試對欄位標頭標題換行；因此，若欄位標頭所需的總寬度超過目標寬度，`wrapped` 格式的行為會與 `aligned` 相同。

`asciidoc`、`html`、`latex`、`latex-longtable` 與 `troff-ms` 格式輸出的表格，是要分別放入使用對應標記語言的文件中。它們並不是完整的文件！在 HTML 中這可能不是必要的，但在 LaTeX 中你必須有完整的文件包裝。`latex` 格式使用 LaTeX 的 `tabular` 環境。`latex-longtable` 格式需要 LaTeX 的 `longtable` 與 `booktabs` 套件。
<a id="APP-PSQL-META-COMMAND-PSET-LINESTYLE"></a>

## `linestyle` [#](#app-psql-meta-command-pset-linestyle) <a href="#app-psql-meta-command-pset-linestyle" id="app-psql-meta-command-pset-linestyle"></a>

將框線的繪製樣式設為 `ascii`、`old-ascii` 或 `unicode` 其中之一。允許使用不產生歧義的縮寫。（這表示一個字母就夠了。）預設設定為 `ascii`。此選項只影響 `aligned` 與 `wrapped` 輸出格式。

`ascii` 樣式使用純 ASCII 字元。資料中的換行會以右側邊界的 `+` 符號表示。當 `wrapped` 格式在沒有換行字元的情況下將資料從一行折到下一行時，會在第一行的右側邊界顯示一個點（`.`），並在下一行的左側邊界再顯示一次。

`old-ascii` 樣式使用純 ASCII 字元，採用 PostgreSQL 8.4 及更早版本所使用的格式樣式。資料中的換行會以 `:` 符號取代左側的欄位分隔符號來表示。當資料在沒有換行字元的情況下從一行折到下一行時，會以 `;` 符號取代左側的欄位分隔符號。

`unicode` 樣式使用 Unicode 框線繪製字元。資料中的換行會以右側邊界的歸位符號表示。當資料在沒有換行字元的情況下從一行折到下一行時，會在第一行的右側邊界顯示一個省略符號，並在下一行的左側邊界再顯示一次。

當 `border` 設定大於零時，`linestyle` 選項也會決定繪製框線所用的字元。純 ASCII 字元在任何地方都能運作，但在能辨識 Unicode 字元的顯示器上，Unicode 字元看起來比較美觀。
<a id="APP-PSQL-META-COMMAND-PSET-NULL"></a>

## `null` [#](#app-psql-meta-command-pset-null) <a href="#app-psql-meta-command-pset-null" id="app-psql-meta-command-pset-null"></a>

設定在空值（null）的位置要印出的字串。預設是什麼都不印，這很容易被誤認為空字串。例如，你可能會偏好使用 `\pset null
'(null)'`。
<a id="APP-PSQL-META-COMMAND-PSET-NUMERICLOCALE"></a>

## `numericlocale` [#](#app-psql-meta-command-pset-numericlocale) <a href="#app-psql-meta-command-pset-numericlocale" id="app-psql-meta-command-pset-numericlocale"></a>

若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用以特定語言環境（locale）的字元來分隔小數點左側數字群組的顯示。若省略 *`value`*，此命令會在一般數字輸出與特定語言環境的數字輸出之間切換。
<a id="APP-PSQL-META-COMMAND-PSET-PAGER"></a>

## `pager` [#](#app-psql-meta-command-pset-pager) <a href="#app-psql-meta-command-pset-pager" id="app-psql-meta-command-pset-pager"></a>

控制查詢輸出與 psql 說明輸出是否使用分頁程式。當 `pager` 選項為 `off` 時，不使用分頁程式。當 `pager` 選項為 `on` 時，會在適當的時候使用分頁程式，亦即輸出到終端機且無法在一個畫面中容納時。`pager` 選項也可以設為 `always`，這會使所有終端機輸出都使用分頁程式，不論是否能在一個畫面中容納。不帶 *`value`* 的 `\pset pager` 會切換分頁程式的使用開關。

若設定了環境變數 `PSQL_PAGER` 或 `PAGER`，要分頁的輸出會以管線傳給指定的程式。否則會使用與平台相關的預設程式（例如 `more`）。

在 Unix 系統上，使用 `\watch` 命令重複執行查詢時，會改用環境變數 `PSQL_WATCH_PAGER` 來尋找分頁程式。之所以另外設定，是因為這可能會讓傳統的分頁程式混淆，但可用來將輸出傳送給能理解 psql 輸出格式的工具（例如 `pspg --stream`）。
<a id="APP-PSQL-META-COMMAND-PSET-PAGER-MIN-LINES"></a>

## `pager_min_lines` [#](#app-psql-meta-command-pset-pager-min-lines) <a href="#app-psql-meta-command-pset-pager-min-lines" id="app-psql-meta-command-pset-pager-min-lines"></a>

若 `pager_min_lines` 設為大於頁面高度的數字，則除非至少有這麼多行輸出要顯示，否則不會呼叫分頁程式。預設設定為 0。
<a id="APP-PSQL-META-COMMAND-PSET-RECORDSEP"></a>

## `recordsep` [#](#app-psql-meta-command-pset-recordsep) <a href="#app-psql-meta-command-pset-recordsep" id="app-psql-meta-command-pset-recordsep"></a>

指定非對齊輸出格式所使用的記錄（行）分隔字元。預設為換行字元。
<a id="APP-PSQL-META-COMMAND-PSET-RECORDSEP-ZERO"></a>

## `recordsep_zero` [#](#app-psql-meta-command-pset-recordsep-zero) <a href="#app-psql-meta-command-pset-recordsep-zero" id="app-psql-meta-command-pset-recordsep-zero"></a>

將非對齊輸出格式所使用的記錄分隔字元設為值為 0 的位元組（NUL）。
<a id="APP-PSQL-META-COMMAND-PSET-TABLEATTR"></a>

## `tableattr`（或 `T`） [#](#app-psql-meta-command-pset-tableattr) <a href="#app-psql-meta-command-pset-tableattr" id="app-psql-meta-command-pset-tableattr"></a>

在 HTML 格式中，此選項指定要放在 `table` 標籤內的屬性。例如可以是 `cellpadding` 或 `bgcolor`。請注意，你大概不會想在這裡指定 `border`，因為那已經由 `\pset border` 處理了。若未給定 *`value`*，則會取消設定表格屬性。

在 `latex-longtable` 格式中，此選項控制每個包含靠左對齊資料型別之欄位的比例寬度。它以空白分隔的值清單指定，例如 `'0.2 0.2 0.6'`。未指定的輸出欄位會使用最後一個指定的值。
<a id="APP-PSQL-META-COMMAND-PSET-TITLE"></a>

## `title`（或 `C`） [#](#app-psql-meta-command-pset-title) <a href="#app-psql-meta-command-pset-title" id="app-psql-meta-command-pset-title"></a>

設定之後所印出之任何表格的表格標題。這可用來為你的輸出加上描述性的標籤。若未給定 *`value`*，則會取消設定標題。
<a id="APP-PSQL-META-COMMAND-PSET-TUPLES-ONLY"></a>

## `tuples_only`（或 `t`） [#](#app-psql-meta-command-pset-tuples-only) <a href="#app-psql-meta-command-pset-tuples-only" id="app-psql-meta-command-pset-tuples-only"></a>

若指定了 *`value`*，它必須是 `on` 或 `off`，分別啟用或停用僅資料列（tuples-only）模式。若省略 *`value`*，此命令會在一般輸出與僅資料列輸出之間切換。一般輸出包含額外資訊，例如欄位標頭、標題與各種頁尾。在僅資料列模式下，只會顯示實際的表格資料。
<a id="APP-PSQL-META-COMMAND-PSET-UNICODE-BORDER-LINESTYLE"></a>

## `unicode_border_linestyle` [#](#app-psql-meta-command-pset-unicode-border-linestyle) <a href="#app-psql-meta-command-pset-unicode-border-linestyle" id="app-psql-meta-command-pset-unicode-border-linestyle"></a>

將 `unicode` 線條樣式的框線繪製樣式設為 `single` 或 `double` 其中之一。
<a id="APP-PSQL-META-COMMAND-PSET-UNICODE-COLUMN-LINESTYLE"></a>

## `unicode_column_linestyle` [#](#app-psql-meta-command-pset-unicode-column-linestyle) <a href="#app-psql-meta-command-pset-unicode-column-linestyle" id="app-psql-meta-command-pset-unicode-column-linestyle"></a>

將 `unicode` 線條樣式的欄位繪製樣式設為 `single` 或 `double` 其中之一。
<a id="APP-PSQL-META-COMMAND-PSET-UNICODE-HEADER-LINESTYLE"></a>

## `unicode_header_linestyle` [#](#app-psql-meta-command-pset-unicode-header-linestyle) <a href="#app-psql-meta-command-pset-unicode-header-linestyle" id="app-psql-meta-command-pset-unicode-header-linestyle"></a>

將 `unicode` 線條樣式的標頭繪製樣式設為 `single` 或 `double` 其中之一。
<a id="APP-PSQL-META-COMMAND-PSET-XHEADER-WIDTH"></a>

## `xheader_width` [#](#app-psql-meta-command-pset-xheader-width) <a href="#app-psql-meta-command-pset-xheader-width" id="app-psql-meta-command-pset-xheader-width"></a>

將擴展輸出的標頭最大寬度設為 `full`（預設值）、`column`、`page` 或某個 *`integer value`* 其中之一。

`full`：擴展標頭不會被截斷，寬度會與最寬的輸出行相同。

`column`：將標頭行截斷為第一個欄位的寬度。

`page`：將標頭行截斷為終端機的寬度。

*`integer value`*：指定標頭行的確切最大寬度。

## 相關範例與提示

這些不同格式的外觀範例，請參閱下方的[範例](app-psql.md#fan-li)。

<a id="APP-PSQL-META-COMMAND-PSET-TIP"></a>

### 提示 [#](#app-psql-meta-command-pset-tip) <a href="#app-psql-meta-command-pset-tip" id="app-psql-meta-command-pset-tip"></a>

`\pset` 有多個簡寫命令。請參閱 `\a`、`\C`、`\f`、`\H`、`\t`、`\T` 與 `\x`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-psql.html)（原文版本：18.6；核對日期：2026-10-17）
