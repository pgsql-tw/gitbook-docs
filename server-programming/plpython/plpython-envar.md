## 44.11. 環境變數 [#](#PLPYTHON-ENVAR)

Python 直譯器接受的部分環境變數，也能用來影響 PL/Python 的行為。這些變數必須設於 PostgreSQL 主伺服器程序的環境中，例如在啟動指令碼內設定。可用的環境變數取決於 Python 版本；詳情請參閱 Python 文件。在撰寫本文時，若 Python 版本適當，下列環境變數會影響 PL/Python：

* `PYTHONHOME`
* `PYTHONPATH`
* `PYTHONY2K`
* `PYTHONOPTIMIZE`
* `PYTHONDEBUG`
* `PYTHONVERBOSE`
* `PYTHONCASEOK`
* `PYTHONDONTWRITEBYTECODE`
* `PYTHONIOENCODING`
* `PYTHONUSERBASE`
* `PYTHONHASHSEED`

（`python` 手冊頁列出的部分環境變數，只對命令列直譯器有效，對嵌入式 Python 直譯器無效；這似乎是 Python 的實作細節，超出 PL/Python 的控制範圍。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-envar.html)（原文版本：18.6；核對日期：2026-09-07）
