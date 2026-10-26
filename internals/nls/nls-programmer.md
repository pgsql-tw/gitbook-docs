<a id="NLS-PROGRAMMER"></a>

## 56.2. 給程式設計者 [#](#nls-programmer) <a href="#nls-programmer" id="nls-programmer"></a>

[56.2.1. 運作機制](nls-programmer.md#nls-mechanics)

[56.2.2. 訊息撰寫指南](nls-programmer.md#nls-guidelines)

<a id="NLS-MECHANICS"></a>

### 56.2.1. 運作機制 [#](#nls-mechanics) <a href="#nls-mechanics" id="nls-mechanics"></a>

本節說明如何在屬於 PostgreSQL 發行版本一部分的程式或函式庫中實作母語支援。目前它只適用於 C 程式。

<a id="id-1.10.8.3.2.3"></a>

**為程式加入 NLS 支援**

1. 將下列程式碼插入程式的啟動流程中：

   ```

   #ifdef ENABLE_NLS
   #include <locale.h>
   #endif

   ...

   #ifdef ENABLE_NLS
   setlocale(LC_ALL, "");
   bindtextdomain("progname", LOCALEDIR);
   textdomain("progname");
   #endif
   ```

   （*`progname`* 實際上可以自由選擇。）
2. 凡是找到可能需要翻譯的訊息，都需要插入對 `gettext()` 的呼叫。例如：

   ```

   fprintf(stderr, "panic level %d\n", lvl);
   ```

   應改為：

   ```

   fprintf(stderr, gettext("panic level %d\n"), lvl);
   ```

   （若未設定 NLS 支援，`gettext` 會被定義為不做任何事的空操作。）

   這往往會增加許多雜亂的程式碼。一種常見的簡寫方式是使用：

   ```

   #define _(x) gettext(x)
   ```

   若程式的大部分溝通都透過一個或少數幾個函式進行（例如後端中的 `ereport()`），就可以採用另一種解法：讓這個函式在內部對所有輸入字串呼叫 `gettext`。
3. 在程式原始碼所在的目錄中加入檔案 `nls.mk`。這個檔案會被當作 makefile 讀取。需要在這裡進行下列變數指派：

   `CATALOG_NAME`
   :   程式名稱，與 `textdomain()` 呼叫中所提供的相同。

   `GETTEXT_FILES`
   :   包含可翻譯字串的檔案清單，也就是以 `gettext` 或替代方案標記了字串的那些檔案。最終，這會包含程式幾乎所有的原始檔。若這份清單變得太長，可以讓第一個「檔案」為 `+`，第二個字則是一個每行包含一個檔名的檔案。

   `GETTEXT_TRIGGERS`
   :   為翻譯者產生訊息目錄的工具，需要知道哪些函式呼叫包含可翻譯的字串。預設只認得 `gettext()` 呼叫。若你使用了 `_` 或其他識別字，就需要在這裡列出它們。若可翻譯的字串不是第一個引數，該項目需要寫成 `func:2` 的形式（表示第二個引數）。若你有支援複數形式訊息的函式，該項目應該寫成像 `func:1,2` 這樣（分別指出單數與複數訊息的引數）。
4. 加入檔案 `po/LINGUAS`，其中將包含所提供的翻譯清單——最初為空。

建置系統會自動負責建置與安裝訊息目錄。

<a id="NLS-GUIDELINES"></a>

### 56.2.2. 訊息撰寫指南 [#](#nls-guidelines) <a href="#nls-guidelines" id="nls-guidelines"></a>

以下是撰寫容易翻譯之訊息的一些指南。

* 不要在執行期間組合句子，例如：

  ```

  printf("Files were %s.\n", flag ? "copied" : "removed");
  ```

  在其他語言中，句子內的詞序可能不同。此外，即使你記得對每個片段呼叫 `gettext()`，這些片段分開翻譯的效果也可能不好。最好多重複一點程式碼，讓每一則要翻譯的訊息都是一個連貫的整體。只有數字、檔名以及類似的執行期變數，才應該在執行期間插入訊息文字中。
* 基於類似的理由，下面的寫法行不通：

  ```

  printf("copied %d file%s", n, n!=1 ? "s" : "");
  ```

  因為它假設了複數形式的構成方式。如果你以為可以這樣解決：

  ```

  if (n==1)
      printf("copied 1 file");
  else
      printf("copied %d files", n):
  ```

  譯註：上方範例最後一行的冒號（:）是官方原文的誤植，正確的 C 陳述式應以分號（;）結尾。本譯文保留原始程式碼，僅在此說明勘誤。

  那你會失望的。有些語言有超過兩種形式，而且有一些特殊的規則。通常最好的做法是設計訊息時就完全避開這個問題，例如像這樣：

  ```

  printf("number of copied files: %d", n);
  ```

  如果你真的想組合出正確使用複數形式的訊息，系統也有支援，只是有點不方便。在 `ereport()` 中產生主要或詳細錯誤訊息時，你可以寫成像這樣：

  ```

  errmsg_plural("copied %d file",
                "copied %d files",
                n,
                n)
  ```

  第一個引數是適用於英文單數形式的格式字串，第二個是適用於英文複數形式的格式字串，第三個則是決定要使用哪一種複數形式的整數控制值。後續的引數照常依格式字串進行格式化。（通常複數控制值也會是要格式化的值之一，因此必須寫兩次。）在英文中，只有 *`n`* 是 1 或不是 1 有差別，但在其他語言中可能有許多不同的複數形式。翻譯者會將兩種英文形式視為一組，並有機會提供多個替代字串，再根據 *`n`* 的執行期值選出適當的那一個。

  若你需要將不是直接送往 `errmsg` 或 `errdetail` 報告的訊息改成複數形式，就必須使用底層函式 `ngettext`。請參閱 gettext 的文件。
* 若你想向翻譯者傳達某些事情，例如某則訊息打算如何與其他輸出對齊，請在該字串出現之前加上一則以 `translator` 開頭的註解，例如：

  ```

  /* translator: This message is not what it seems to be. */
  ```

  這些註解會被複製到訊息目錄檔案中，讓翻譯者能夠看到。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/nls-programmer.html)（原文版本：18.6；核對日期：2026-10-17）
