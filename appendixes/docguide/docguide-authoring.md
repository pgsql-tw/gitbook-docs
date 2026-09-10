## J.5. 文件撰寫 [#](#DOCGUIDE-AUTHORING)

[J.5.1. Emacs](docguide-authoring.md#DOCGUIDE-AUTHORING-EMACS)

使用具備 XML 編輯模式的編輯器最便於修改文件原始碼；若編輯器也瞭解 XML schema 語言，
能特別辨識 DocBook 語法，則更為方便。

請注意，基於歷史因素，文件原始碼檔案雖然現在是 XML 檔案，副檔名仍為 `.sgml`。
因此，你可能需要調整編輯器設定以選用正確的模式。

<a id="DOCGUIDE-AUTHORING-EMACS"></a>

### J.5.1. Emacs [#](#DOCGUIDE-AUTHORING-EMACS)

nXML Mode 隨 Emacs 一同提供，是使用 Emacs 編輯 XML 文件最常見的模式。
它可讓你使用 Emacs 插入標籤並檢查標記的一致性，且原生支援 DocBook。詳細資訊請參閱 [nXML 手冊](https://www.gnu.org/software/emacs/manual/html_mono/nxml-mode.html)。

`src/tools/editors/emacs.samples` 包含此模式的建議設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-authoring.html)（原文版本：18.6；核對日期：2026-09-10）
