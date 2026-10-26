<a id="NLS-TRANSLATOR"></a>

## 56.1. 給翻譯者 [#](#nls-translator) <a href="#nls-translator" id="nls-translator"></a>

[56.1.1. 需求](nls-translator.md#nls-translator-requirements)

[56.1.2. 基本概念](nls-translator.md#nls-translator-concepts)

[56.1.3. 建立與維護訊息目錄](nls-translator.md#nls-translator-message-catalogs)

[56.1.4. 編輯 PO 檔案](nls-translator.md#nls-translator-editing-po)

PostgreSQL
程式（伺服器與用戶端）可以用
你偏好的語言發出訊息——前提是這些訊息已經翻譯過。
建立與維護已翻譯的訊息集，需要
精通自己語言、並且願意為
PostgreSQL 貢獻心力的人協助。你完全不必是
程式設計師
也能做這件事。本節說明如何協助。

<a id="NLS-TRANSLATOR-REQUIREMENTS"></a>

### 56.1.1. 需求 [#](#nls-translator-requirements) <a href="#nls-translator-requirements" id="nls-translator-requirements"></a>

我們不會評斷你的語言能力——本節談的是
軟體工具。理論上，你只需要一個文字編輯器。但
這只適用於你不想實際試用自己翻譯的訊息這種
不太可能發生的情況。設定原始碼樹時，請
務必使用 `--enable-nls` 選項。這也會
檢查 libintl 函式庫與
`msgfmt` 程式，這些無論如何都是所有終端使用者
需要的。若要試用你的成果，請依照
安裝說明中適用的部分進行。

如果你想展開新的翻譯工作，或想進行
訊息目錄合併（稍後說明），你將分別需要
`xgettext` 與
`msgmerge` 這兩個程式，而且必須是與 GNU 相容的
實作。之後我們會設法安排，讓你在
使用打包好的原始碼發行版時，不需要
`xgettext`。（若是從 Git 工作，你仍然需要
它。）目前建議使用 GNU Gettext 0.10.36 或更新版本。

你本機的 gettext 實作應該會附帶自己的
文件。其中一些內容可能與以下
說明重複，但若需要更多細節，應該去那裡查閱。

<a id="NLS-TRANSLATOR-CONCEPTS"></a>

### 56.1.2. 基本概念 [#](#nls-translator-concepts) <a href="#nls-translator-concepts" id="nls-translator-concepts"></a>

原始（英文）訊息與其（可能已）
翻譯之對應訊息所組成的配對，保存在*訊息
目錄*（message catalog）中，每個程式（雖然相關的
程式可以共用一個訊息目錄）與每個目標
語言各有一個。訊息目錄有兩種檔案格式：
第一種是「PO」檔案（Portable Object，可攜式物件），
它是具有特殊語法、供翻譯者編輯的純文字檔案。
第二種是「MO」檔案（Machine Object，機器物件），
它是由對應的 PO 檔案產生的二進位檔案，
在執行國際化程式時使用。翻譯者
不會接觸 MO 檔案；事實上幾乎沒有人會接觸。

訊息目錄檔案的副檔名，不出所料，是
`.po` 或 `.mo`。主檔名
則依情況而定，可能是它所搭配之程式的名稱，也可能是
該檔案所屬的語言。這有點
令人困惑。例如 `psql.po`（psql 的
PO 檔案）或 `fr.mo`（法文的 MO 檔案）。

PO 檔案的檔案格式如下所示：

```

# comment

msgid "original string"
msgstr "translated string"

msgid "more original"
msgstr "another translated"
"string can be broken up like this"

...
```

msgid 行是從程式原始碼中擷取出來的。（不一定
要這樣做，但這是最常見的方式。）msgstr 行
一開始是空的，由翻譯者填入有用的字串。
這些字串可以包含 C 風格的跳脫字元，並且
可以如上所示跨行接續。（下一行必須
從該行的開頭開始。）

字元 # 用來開始一段註解。如果 # 字元後面
緊接著空白，這就是由
翻譯者維護的註解。也可能有自動註解，其 # 後面
緊接著的是非空白字元。這些註解
由處理 PO 檔案的各種工具維護，
目的是協助翻譯者。

```

#. automatic comment
#: filename.c:1023
#, flags, flags
```

形式為 #. 的註解，是從使用該訊息的原始檔中
擷取出來的。程式設計師可能在其中加入了給
翻譯者的資訊，例如預期的對齊方式。#:
註解指出該訊息在原始碼中被使用的
確切位置。翻譯者不必查看程式
原始碼，但在對正確的翻譯
有疑問時可以查看。#, 註解包含以某種方式
描述該訊息的旗標。目前有兩個旗標：
如果訊息可能因為程式原始碼的變更而
過時，就會設定 `fuzzy`。翻譯者
接著可以確認這一點，並視情況移除 fuzzy 旗標。請注意，
fuzzy 訊息不會提供給終端使用者。另一個
旗標是 `c-format`，它表示
該訊息是 `printf` 風格的格式
範本。這表示翻譯也應該是一個格式
字串，具有相同數量與型別的預留位置。有一些
工具可以依據 c-format 旗標來驗證這一點。

<a id="NLS-TRANSLATOR-MESSAGE-CATALOGS"></a>

### 56.1.3. 建立與維護訊息目錄 [#](#nls-translator-message-catalogs) <a href="#nls-translator-message-catalogs" id="nls-translator-message-catalogs"></a>

那麼，要如何建立一個「空白」的訊息
目錄呢？首先，進入包含你想翻譯其訊息之程式的
目錄。如果其中有
`nls.mk` 檔案，表示這個程式已經做好
翻譯的準備。

如果已經有一些 `.po` 檔案，表示
已經有人做過一些翻譯工作。這些檔案
命名為 `language.po`，
其中 *`language`* 是
[ISO 639-1 雙字母語言代碼（小寫）](https://www.loc.gov/standards/iso639-2/php/English_list.php)，例如
法文為 `fr.po`。如果每種語言確實需要
超過一項翻譯工作，那麼檔案
也可以命名為
`language_region.po`，
其中 *`region`* 是
[ISO 3166-1 雙字母國家代碼（大寫）](https://www.iso.org/iso-3166-country-codes.html)，
例如巴西葡萄牙文為
`pt_BR.po`。如果你
找到了想要的語言，就可以直接開始處理那個
檔案。

如果你需要展開新的翻譯工作，請先執行
下列命令：

```

make init-po
```

這會建立一個
`progname.pot` 檔案。
（`.pot` 是為了與「正在使用中」的 PO 檔案
區分。`T` 代表
「template」（範本）。）
將這個檔案複製為
`language.po` 並
加以編輯。為了讓大家知道有新的語言可用，
也請編輯 `po/LINGUAS` 檔案，在已列出的語言旁
加入該語言代碼（或語言與國家代碼），
例如：

```

de fr
```

（當然也可能出現其他語言。）

當底層的程式或函式庫變更時，程式設計師可能會
修改或新增訊息。在這種情況下，你不需要
從頭開始。改為執行下列命令：

```

make update-po
```

它會建立一個新的空白訊息目錄檔案（也就是你
一開始使用的 pot 檔案），並將它與現有的 PO 檔案合併。
如果合併演算法無法確定某則訊息，就會
如上所述將它標記為「fuzzy」。新的 PO 檔案
會以 `.po.new` 副檔名儲存。

<a id="NLS-TRANSLATOR-EDITING-PO"></a>

### 56.1.4. 編輯 PO 檔案 [#](#nls-translator-editing-po) <a href="#nls-translator-editing-po" id="nls-translator-editing-po"></a>

PO 檔案可以用一般的文字編輯器編輯。另外也有
數種專門用於 PO 檔案的編輯器，可以透過
翻譯專用的功能協助這項工作。
（不出所料）Emacs 也有 PO 模式，相當
好用。

翻譯者只應該修改 msgstr 指令後面
引號之間的區域、加入註解，以及變更 fuzzy 旗標。

PO 檔案不必完全填滿。如果沒有翻譯
（或翻譯為空），軟體會
自動改用原始字串。將
不完整的翻譯提交並納入原始碼樹，
完全沒有問題；這樣其他人才有機會接手你的工作。不過，
我們鼓勵你在完成合併之後，優先移除 fuzzy 項目。
請記住，fuzzy 項目不會被
安裝；它們只用來作為可能正確之
翻譯的參考。

編輯翻譯時，有幾件事需要
記住：

* 請確認如果原文以換行字元結尾，
  譯文也要以換行字元結尾。定位字元（tab）等也是如此。
* 如果原文是 `printf` 格式字串，譯文
  也必須是。譯文也需要以相同的順序
  具有相同的格式指定符。有時候語言本身的
  規則會讓這件事無法做到，或至少很彆扭。
  這時你可以像這樣修改格式指定符：

  ```

  msgstr "Die Datei %2$s hat %1$u Zeichen."
  ```

  如此一來，第一個預留位置實際上會使用清單中的第二個
  引數。
  `digits$` 必須
  緊接在 % 後面，位於任何其他格式修飾符之前。
  （這項功能確實存在於 `printf`
  系列函式中。你以前可能沒聽說過它，因為
  除了訊息國際化之外，它幾乎沒有什麼
  用途。）
* 如果原始字串含有語言上的錯誤，請回報
  （或自行在程式原始碼中修正），並照常
  翻譯。修正後的字串可以在
  程式原始碼更新後合併進來。如果原始字串
  含有事實上的錯誤，請回報（或自行修正），
  而且不要翻譯它。你可以改在 PO 檔案中
  以註解標記該字串。
* 保持原始字串的風格與語氣。
  具體來說，不是完整句子的訊息（`cannot
  open file %s`）可能不應該以
  大寫字母開頭（如果你的語言有大小寫之分），或
  以句號結尾（如果你的語言使用標點符號）。
  閱讀[第 55.3 節](../source/error-style-guide.md)可能會有幫助。
* 如果你不知道某則訊息的意思，或它有歧義，
  請到開發人員郵件清單詢問。說英語的
  終端使用者很可能也看不懂它，或覺得它
  有歧義，因此最好改善這則訊息。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/nls-translator.html)（原文版本：18.6；核對日期：2026-10-12）
