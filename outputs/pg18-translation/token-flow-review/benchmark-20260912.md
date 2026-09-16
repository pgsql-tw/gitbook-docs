# 實際 token A/B 測試：passwordcheck

2026-09-12，約 17:34–17:36（Asia/Taipei）。測試腳本：scripts/benchmark_translation_tokens.py。

## 方法

固定 passwordcheck 原文、譯稿、PostgreSQL 18.6 官方 source.html 快照（retrieved 2026-09-11T19:03:49.851448+00:00）、SKILL/style 快照；各複製到獨立資料夾。舊版直接載入 commit 9a2b72b5 的 Queue.review；新版使用目前 Queue.review。兩邊清空審查快取，使用相同 CLI 預設設定（本次 config：gpt-5.6-terra、medium）、read-only reviewer。沒有啟動翻譯者、發佈或修改正式頁面。

順序為舊版後新版，各一次；不是重複試驗或隨機交叉試驗。政策與原文/候選稿 hash、逐次 JSONL、提示詞、逐節核對證據均保存在 ab-1789205645391270900/。

## 結果

| 指標 | 舊版逐節 | 新版批次 | 減少 |
| --- | ---: | ---: | ---: |
| 審查呼叫 | 3 | 1 | 66.7% |
| 輸入 tokens（包含快取部分） | 250,308 | 22,858 | 90.9% |
| 快取輸入 tokens（輸入的子集） | 176,896 | 0 | 不作成本推算 |
| 未快取輸入 tokens | 73,412 | 22,858 | 68.9% |
| 輸出 tokens | 3,209 | 431 | 86.6% |
| reasoning_output_tokens（另列、不重複相加） | 1,046 | 213 | — |
| shell 指令完成事件 | 8 | 0 | — |
| 審查耗時 | 100.64 秒 | 14.24 秒 | 85.9% |

節省輸入 227,450 tokens、未快取輸入 50,554 tokens、輸出 2,778 tokens。沒有失敗呼叫或省略不利結果。

兩邊都回報 sections 0、1、2 通過，無 issues，且每節候選稿 hash 一致。新版證據涵蓋啟用條件、CrackLib 例外、未加密密碼風險、预先加密的限制、參數單位/預設值/超級使用者權限與保留範例。這證明本次覆蓋與檢查結果一致，不等同完整品質等效性研究。

## 解讀與限制

舊版在各呼叫中讀取文件，工具輸出及歷史上下文隨後再次進入模型；新版一次供應必要來源、完整政策與所有選中段落，無需 shell 讀取，並合併三次啟動。減量來自流程與重複上下文減少，不是取消獨立語意審查。

這是小頁單次的「審查階段」測試，不包含翻譯生成、修稿、父對話、排程監控，也不能推定大型頁面或全部剩餘頁面都節省 90.9%。快取命中、模型行為與呼叫順序可能影響結果。不能把 token 比例直接換算成 ChatGPT 帳戶額度、費用或金額。

數據取自每次 JSONL 的 turn.completed.usage，而非字元數估計或少呼叫次數推算。欄位參考：[OpenAI Docs 非互動模式](https://learn.chatgpt.com/docs/non-interactive-mode)。原始結果：[report.json](ab-1789205645391270900/report.json)。
