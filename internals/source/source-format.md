<a id="SOURCE-FORMAT"></a>

## 55.1. 格式 [#](#source-format) <a href="#source-format" id="source-format"></a>

原始碼格式採用 4 欄寬的定位字元（tab）間距，並保留定位字元（也就是說，定位字元不會展開成空格）。每多一層邏輯縮排，就多一個定位停駐點。

版面規則（大括號位置等）遵循 BSD 慣例。特別是，`if`、`while`、`switch` 等所控制區塊的大括號，要各自獨立成一行。

請限制每行長度，讓程式碼在 80 欄寬的視窗中仍然易讀。（這不表示你絕對不能超過 80 欄。例如，只為了讓程式碼保持在 80 欄以內，就在任意位置拆開一個很長的錯誤訊息字串，對可讀性來說大概得不償失。）

為了維持一致的程式碼風格，請不要使用 C++ 風格的註解（`//` 註解）。pgindent 會把它們替換成 `/* ... */`。

多行註解區塊的建議風格是

```

/*
 * comment text begins here
 * and continues here
 */
```

請注意，從第 1 欄開始的註解區塊會被 pgindent 原樣保留，但縮排的註解區塊則會被當成純文字重新排列換行。如果你想保留縮排區塊中的換行，請像這樣加上破折號：

```

    /*----------
     * comment text begins here
     * and continues here
     *----------
     */
```

雖然送出的修補程式並非絕對必須遵循這些格式規則，但遵循它們是個好主意。你的程式碼在下一個版本發布前會被 pgindent 處理過，所以讓它在其他格式慣例下看起來漂亮並沒有意義。對修補程式而言，一個不錯的經驗法則是「讓新程式碼看起來像它周圍的既有程式碼」。

`src/tools/editors` 目錄中包含範例設定檔，可用於 Emacs、xemacs 或 vim 編輯器，協助確保它們依照這些慣例來排版程式碼。

如果你想在本機執行 pgindent，讓你的程式碼符合專案風格，請參閱 `src/tools/pgindent` 目錄。

文字瀏覽工具 more 與 less 可以這樣呼叫：

```

more -x4
less -x4
```

讓它們正確顯示定位字元。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/source-format.html)（原文版本：18.6；核對日期：2026-10-12）
