<a id="DOCGUIDE-STYLE"></a>

## J.6. 風格指南 [#](#DOCGUIDE-STYLE)

[J.6.1. 參考頁面](docguide-style.md#DOCGUIDE-STYLE-REF-PAGES)

<a id="DOCGUIDE-STYLE-REF-PAGES"></a>

### J.6.1. 參考頁面 [#](#DOCGUIDE-STYLE-REF-PAGES)

參考頁面應該遵循標準的版面配置。這可以讓
使用者更快找到所需的資訊，也能
鼓勵撰寫者記載命令所有相關的面向。
一致性不僅是
PostgreSQL 參考頁面之間所追求的，也希望
與作業系統及其他
套件所提供的參考頁面保持一致。因此制定了下列準則。
這些準則大致上與
各種作業系統所制定的類似準則一致。

描述可執行命令的參考頁面應該包含
下列各節，並依此順序排列。不適用的節
可以省略。額外的頂層節只應在
特殊情況下使用；這類資訊通常應該放在
「用法」（Usage）一節中。

<a id="DOCGUIDE-STYLE-REF-PAGES-NAME"></a>

名稱（Name） [#](#DOCGUIDE-STYLE-REF-PAGES-NAME)
:   此節會自動產生。它包含
    命令名稱，以及半句話的功能摘要。
<a id="DOCGUIDE-STYLE-REF-PAGES-SYNOPSIS"></a>

語法（Synopsis） [#](#DOCGUIDE-STYLE-REF-PAGES-SYNOPSIS)
:   此節包含命令的語法圖。語法
    通常不應列出每一個命令列選項；
    那會在後面說明。取而代之的是，列出
    命令列的主要組成部分，例如輸入與輸出檔案的位置。
<a id="DOCGUIDE-STYLE-REF-PAGES-DESCRIPTION"></a>

說明（Description） [#](#DOCGUIDE-STYLE-REF-PAGES-DESCRIPTION)
:   以數個段落說明此命令的作用。
<a id="DOCGUIDE-STYLE-REF-PAGES-OPTIONS"></a>

選項（Options） [#](#DOCGUIDE-STYLE-REF-PAGES-OPTIONS)
:   說明每一個命令列選項的清單。若
    選項很多，可以使用子節。
<a id="DOCGUIDE-STYLE-REF-PAGES-EXIT-STATUS"></a>

結束狀態（Exit Status） [#](#DOCGUIDE-STYLE-REF-PAGES-EXIT-STATUS)
:   若程式以 0 表示成功、以非零值表示失敗，
    則不需要記載。若不同的非零結束碼
    各有其意義，請在此列出。
<a id="DOCGUIDE-STYLE-REF-PAGES-USAGE"></a>

用法（Usage） [#](#DOCGUIDE-STYLE-REF-PAGES-USAGE)
:   描述程式的任何子語言或執行期介面。
    若程式不是互動式的，通常可以省略此節。
    否則，此節用來
    統括描述各種執行期功能。適當時可使用子節。
<a id="DOCGUIDE-STYLE-REF-PAGES-ENVIRONMENT"></a>

環境（Environment） [#](#DOCGUIDE-STYLE-REF-PAGES-ENVIRONMENT)
:   列出程式可能使用的所有環境變數。
    請盡量列完整；即使是看似微不足道的變數，例如
    `SHELL`，也可能是使用者關心的。
<a id="DOCGUIDE-STYLE-REF-PAGES-FILES"></a>

檔案（Files） [#](#DOCGUIDE-STYLE-REF-PAGES-FILES)
:   列出程式可能隱含存取的任何檔案。也就是說，
    不要列出在命令列上指定的輸入與輸出檔案，
    而是列出設定檔等。
<a id="DOCGUIDE-STYLE-REF-PAGES-DIAGNOSTICS"></a>

診斷（Diagnostics） [#](#DOCGUIDE-STYLE-REF-PAGES-DIAGNOSTICS)
:   解釋程式可能產生的任何不尋常輸出。
    不要列出每一個可能的錯誤訊息。那樣
    工作量很大，在實務上用處也不大。但如果，例如，
    錯誤訊息具有使用者可以剖析的標準格式，
    這裡就是說明它的地方。
<a id="DOCGUIDE-STYLE-REF-PAGES-NOTES"></a>

注意事項（Notes） [#](#DOCGUIDE-STYLE-REF-PAGES-NOTES)
:   任何不適合放在其他地方的內容，特別是程式錯誤、
    實作缺陷、安全性考量、相容性
    問題。
<a id="DOCGUIDE-STYLE-REF-PAGES-EXAMPLES"></a>

範例（Examples） [#](#DOCGUIDE-STYLE-REF-PAGES-EXAMPLES)
:   範例
<a id="DOCGUIDE-STYLE-REF-PAGES-HISTORY"></a>

歷史（History） [#](#DOCGUIDE-STYLE-REF-PAGES-HISTORY)
:   若程式的歷史中有一些重大的里程碑，
    可以在此列出。通常可以省略
    此節。
<a id="DOCGUIDE-STYLE-REF-PAGES-AUTHOR"></a>

作者（Author） [#](#DOCGUIDE-STYLE-REF-PAGES-AUTHOR)
:   作者（只用於 contrib 部分）
<a id="DOCGUIDE-STYLE-REF-PAGES-SEE-ALSO"></a>

另請參閱（See Also） [#](#DOCGUIDE-STYLE-REF-PAGES-SEE-ALSO)
:   交互參照，依下列順序列出：其他
    PostgreSQL 命令參考頁面、
    PostgreSQL SQL 命令參考
    頁面、引用 PostgreSQL
    手冊、其他參考頁面（例如作業系統、其他
    套件）、其他文件。同一組中的項目
    依字母順序排列。

描述 SQL 命令的參考頁面應該包含
下列各節：名稱（Name）、語法（Synopsis）、說明（Description）、參數（Parameters）、
輸出（Outputs）、注意事項（Notes）、範例（Examples）、相容性（Compatibility）、歷史（History）、另請參閱（See
Also）。參數一節類似選項一節，但
對於可以列出命令的哪些子句有更大的自由度。
只有當命令傳回預設命令完成標籤以外的
內容時，才需要輸出一節。相容性
一節應說明
此命令符合 SQL 標準的程度，或與哪些其他
資料庫系統相容。SQL 命令的另請參閱一節
應先列出 SQL 命令，再列出對
程式的交互參照。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-style.html)（原文版本：18.6；核對日期：2026-10-22）
