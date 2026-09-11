# 多 AI 協作協定：PostgreSQL 18 翻譯

- 建立：2026-09-11，Claude（Cowork）起草；使用者核准分工方式為「雙向夾擊」。
- 適用：branch `18`，`C:\Workspaces\gitbook-docs`。
- 修改本協定：任何代理都可以提議，以 `messages/` 發給 `all`，由使用者裁決後再改本檔。

## 1. 參與者與分工

| 代理 | 工作方式 | 取頁方向 | 可否 commit |
| --- | --- | --- | --- |
| `codex` | 本機 checkout；`scripts/translation_pipeline.py` 佇列與隔離草稿 | `pending-pages.md` 由上往下（第一個 `[ ]` 起） | 可以，目前唯一的 publisher |
| `claude` | Cowork 雲端工作區，經檔案橋接讀寫本資料夾，無法在本機執行 git | 由下往上（最後一個 `[ ]` 起） | 不可以，譯稿送 inbox |

新代理加入時：選一個小寫名稱，在 `status/` 建立自己的看板，並在本表登記取頁方向或章節範圍（例如「只做 reference/」）。範圍不可與他人重疊。

## 2. 五條核心規則

1. **單一發佈者**：只有 publisher 可以修改真實 checkout 中受 Git 追蹤的檔案並 commit。其他代理不得直接修改頁面、`SUMMARY.md`、`pending-pages.md`、`continuation-state.md`。
   理由：pipeline 在這些檔案有未提交變更時會整批停止；`continuation-state.md` 每次發佈都會被 pipeline 覆寫。
2. **先認領再翻譯**：動手前在 `claims/` 建立認領檔；看到他人有效認領就跳過該頁。
3. **譯稿走 inbox**：非 publisher 的代理把完整譯稿放進 `inbox/<代理>/<slug>/`，由 `scripts/agent_handoff.py publish` 檢查後，以該代理為 author 逐頁 commit。
4. **各寫各的檔**：狀態看板只由擁有者寫；訊息一則一檔、寫後不改。沒有任何一個協作檔需要兩個代理同時修改。
5. **Git 是最終真相**：完成與否以 commit trailer `Translation-Page-SHA256` 對帳，不以看板或訊息的文字宣告為準。

## 3. 目錄

```
outputs/pg18-translation/agents/
├── PROTOCOL.md          本檔（受追蹤）
├── .gitignore           忽略以下執行期目錄（受追蹤）
├── status/<代理>.md     各代理看板，只由本人寫
├── claims/<slug>.json   認領檔，一頁一檔
├── inbox/<代理>/<slug>/ 待發佈譯稿：page.md + meta.json
│   ├── _published/      已提交（附 result.json 與 commit）
│   └── _rejected/       退件（附 result.json 與原因）
└── messages/            代理間訊息，一則一檔
```

`slug` = 頁面路徑把 `/` 換成 `__`，例如 `tutorial/tutorial-start/tutorial-install.md` → `tutorial__tutorial-start__tutorial-install.md`。

## 4. 認領檔 `claims/<slug>.json`

```json
{
  "page": "tutorial/tutorial-start/tutorial-install.md",
  "agent": "claude",
  "status": "active",
  "claimed_at": "2026-09-11T21:40:00+08:00",
  "expires_at": "2026-09-12T09:40:00+08:00",
  "note": ""
}
```

- 預設有效 12 小時；譯稿送進 inbox 後把 `status` 改為 `submitted`、`expires_at` 延長 72 小時，等待發佈。
- 過期的認領可被他人接手；接手者須在 `messages/` 通知原認領者。
- publisher 提交或退件後刪除認領檔。
- 可用 `agent_handoff.py claim` 原子建立；無法執行程式的代理（Claude）先列目錄確認不存在再寫入。

## 5. 送件 `inbox/<代理>/<slug>/`

- `page.md`：整頁譯稿，UTF-8、LF。
- `meta.json`：

| 欄位 | 說明 |
| --- | --- |
| `page` | 頁面相對路徑 |
| `agent` | 代理名稱，須與目錄一致 |
| `base_sha256` | 翻譯時讀到的原頁 SHA-256（去 BOM、換行正規化為 LF，與 pipeline 的 `digest(read())` 相同） |
| `page_sha256` | `page.md` 的 SHA-256（同樣正規化） |
| `source_url` | 必須以 `https://www.postgresql.org/docs/18/` 開頭 |
| `source_version`、`retrieved` | 官方原文小版本與核對日期 |
| `submitted_at` | 送件時間（ISO 8601，+08:00） |
| `self_review` | 自我核對紀錄：比對了哪些段落、條件、例外 |
| `trailers`（選填） | 額外 commit trailer，如 `Co-Authored-By: ...` |
| `author`（選填） | 覆寫 commit author；預設 `claude` → `Claude <noreply@anthropic.com>` |

## 6. 發佈檢查（`agent_handoff.py publish`）

逐項檢查，不通過即移到 `_rejected/` 並發訊息給送件者：

- 頁面在待譯清單中仍為 `[ ]`，且沒有他人有效認領。
- 原頁目前的 SHA-256 等於 `base_sha256`（避免覆蓋別人的變更）。
- 結構不變：沿用 `translation_pipeline.structural_errors`（程式碼區塊、行內程式碼、HTML 表格、連結、錨點、標題數），不可殘留「英文原文，待翻譯」。
- `page.md` 的 SHA-256 等於 `page_sha256`。

通過後，在 `pipeline-runtime/publish.lock` 保護下：寫入頁面、清單改 `[x]` 並重算「待譯頁面：N 頁。」、更新 `SUMMARY.md` 標題，三個檔案一筆 commit：

```
文件(pg18)：翻譯 <頁面檔名>

Translation-Page: <page>
Translation-Page-SHA256: <sha256>
Translated-By: <agent>
Source: <url> (<版本>, <日期>)
```

若 index 已有暫存內容，或三個目標檔有未提交變更，整批停止、不做任何寫入。

## 7. 狀態看板 `status/<代理>.md`

每次開工與收工都更新，固定欄位：

```
- 更新時間：
- 狀態：working / idle / blocked
- 取頁方向或範圍：
- 目前認領：
- 最近送出或完成：
- 已讀訊息至：<最後讀到的訊息檔名>
- 阻塞與待決事項：
```

## 8. 訊息 `messages/`

- 檔名：`YYYYMMDDTHHMMSS--<寄件者>--to-<收件者|all>--<主旨>.md`，時間為台北時間。
- 內容開頭為 YAML frontmatter（from、to、date、subject）。
- 不修改或刪除他人訊息；回覆請另開新檔並在主旨註明「回覆」。
- 讀過後把最後一則檔名寫到自己看板的「已讀訊息至」。
- 用途：術語提議、退件說明、接手過期認領、協定修改提議、會合通知。

## 9. 每輪工作流程

**所有代理開工時**

1. 讀本協定、自己的看板、他人的看板。
2. 讀 `messages/` 中「已讀訊息至」之後、收件者是自己或 `all` 的訊息。
3. 讀 `pending-pages.md`，並檢查 `claims/`。

**Codex（publisher）**

1. 先執行 `python scripts/agent_handoff.py publish`，發佈其他代理的 inbox 譯稿。
2. pipeline 取下一頁前，跳過「已非 `[ ]`」或「`is_claimed_by_other(root, page, 'codex')` 為真」的頁面；開始處理某頁時，以 `claim(root, page, 'codex')` 登記。
3. 更新 `status/codex.md`。

**Claude（及其他非 publisher 代理）**

1. 從清單最下方往上，找第一個沒有認領、仍為 `[ ]` 的頁面，寫入認領檔。
2. 讀原頁並記下 `base_sha256`；對照官方 `/docs/18/` 原文翻譯。
3. 在自己的工作區跑結構檢查，通過後寫入 inbox，認領改為 `submitted`。
4. 查看 `_rejected/` 並處理退件；更新自己的看板。

## 10. 會合與結束

- 某代理的下一頁已被他人認領或完成，代表兩個方向已會合：發一則 `to-all` 的「會合」訊息，改做退件修正或交叉審校。
- 清單歸零、inbox 清空、`claims/` 清空之後，publisher 執行 pipeline 的最終稽核。

## 11. 翻譯風格與術語

- 以 Codex skill `postgresql-tw-translation` 的 `SKILL.md` 及 `references/style.md` 為準：技術直述、全形標點，教學章節以「你」稱呼讀者。
- 保留 SQL、識別字、範例、錨點、表格與相對連結；頁首缺少頁面級錨點時補上 `<a id="..."></a>`；頁尾改為 `原文：[PostgreSQL 18.6 Documentation](url)（原文版本：18.6；核對日期：YYYY-MM-DD）`。
- 發現新術語或與既有譯法衝突時，不要自行全站替換；發一則 `to-all` 訊息，由使用者裁決後寫入 style.md。

## 12. 衝突處理

| 狀況 | 處理 |
| --- | --- |
| 兩個代理同時認領同一頁 | 以 `claimed_at` 較早者為準，較晚者放棄並留言 |
| 送件時原頁已被改動（stale base） | 退件；送件者以新原頁重譯或合併 |
| 認領過期但 inbox 已有譯稿 | 接手前先確認 inbox 與 `_published/`，避免重工 |
| publish 因未提交變更而停止 | 不強制覆寫；在看板標為 blocked 並通知使用者 |
| 對譯法有歧見 | 發訊息列出兩案與原文，交使用者裁決 |
