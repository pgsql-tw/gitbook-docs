<a id="TUTORIAL-INSTALL"></a>

## 1.1. 安裝 [#](#TUTORIAL-INSTALL)

使用 PostgreSQL 之前，當然必須先安裝它。PostgreSQL 可能已經安裝在你的環境中，原因可能是你的作業系統發行版本已內含 PostgreSQL，或是系統管理員已經安裝過。若是如此，請參閱作業系統文件或詢問系統管理員，以瞭解如何存取 PostgreSQL。

如果你不確定 PostgreSQL 是否已經可用，或不確定能否用它來做實驗，可以自行安裝。自行安裝並不困難，也是很好的練習。任何不具特殊權限的一般使用者都可以安裝 PostgreSQL，不需要超級使用者（root）權限。

如果你要自行安裝 PostgreSQL，請參閱[第 17 章](../../server-administration/installation/README.md)的安裝說明，安裝完成後再回到本指南。請務必確實依照其中設定適當環境變數的小節操作。

如果你所在環境的管理員沒有以預設方式設定，你可能還需要做一些額外的工作。舉例來說，如果資料庫伺服器是一台遠端主機，你需要將環境變數 `PGHOST` 設為資料庫伺服器主機的名稱，也可能需要設定環境變數 `PGPORT`。總而言之：如果你嘗試啟動應用程式時，它回報無法連線到資料庫，請洽詢你的環境管理員；如果管理員就是你自己，請查閱文件，確認你的環境已正確設定。如果你看不懂上一段的內容，請閱讀下一節。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-install.html)（原文版本：18.6；核對日期：2026-09-11）
