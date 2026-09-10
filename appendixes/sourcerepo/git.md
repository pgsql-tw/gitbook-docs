## I.1. 透過 Git 取得原始碼 [#](#GIT)

使用 Git 時，你會在本機建立整個程式碼儲存庫的副本，因此可離線存取所有歷史紀錄與分支。這是開發或測試修補程式最快且最有彈性的方式。

<a id="id-1.11.10.4.3"></a>

**Git**

1. 你需要安裝 Git，可從 <https://git-scm.com> 取得。許多系統預設已安裝較新的 Git 版本，或可在其套件發行系統中取得。
2. 若要開始使用 Git 儲存庫，請複製官方鏡像：

   ```

   git clone https://git.postgresql.org/git/postgresql.git
   ```

   這會將完整儲存庫複製到本機，因此可能需要一些時間，尤其是在網際網路連線較慢時。檔案會放在目前目錄下的新子目錄 `postgresql` 中。
3. 每當你要取得系統的最新更新時，請 `cd` 至儲存庫並執行：

   ```

   git fetch
   ```

Git 能做的不只取得原始碼。詳細資訊請參閱 Git man page，或造訪 <https://git-scm.com>。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/git.html)（原文版本：18.6；核對日期：2026-09-10）
