## N.2. 設定色彩 [#](#COLOR-WHICH)

實際要使用的色彩由環境變數 `PG_COLORS`<a id="id-1.11.15.5.2.2"></a>（注意是複數）設定。其值為以冒號分隔的 `key=value` 配對清單。鍵指定色彩的用途；值則是由終端機解譯的 SGR（Select Graphic Rendition）規格。

目前使用下列鍵：

`error`
:   用於醒目顯示錯誤訊息中的「error」文字

`warning`
:   用於醒目顯示警告訊息中的「warning」文字

`note`
:   用於醒目顯示此類訊息中的「detail」與「hint」文字

`locus`
:   用於醒目顯示訊息中的位置資訊（例如程式名稱與檔案名稱）

預設值為 `error=01;31:warning=01;35:note=01;36:locus=01`（`01;31` 代表粗體紅色，`01;35` 代表粗體洋紅色，`01;36` 代表粗體青色，`01` 代表粗體的預設色彩）。

### 提示

GCC、GNU coreutils 與 GNU grep 等其他軟體套件也使用此色彩規格格式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/color-which.html)（原文版本：18.6；核對日期：2026-09-06）
