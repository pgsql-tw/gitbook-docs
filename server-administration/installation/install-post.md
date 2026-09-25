<a id="INSTALL-POST"></a>

## 17.5. 安裝後設定 [#](#INSTALL-POST)

[17.5.1. 共用函式庫](install-post.md#INSTALL-POST-SHLIBS)

[17.5.2. 環境變數](install-post.md#INSTALL-POST-ENV-VARS)

<a id="INSTALL-POST-SHLIBS"></a>

### 17.5.1. 共用函式庫 [#](#INSTALL-POST-SHLIBS)

<a id="id-1.6.4.8.2.2"></a>

在部分使用共用函式庫的系統上，你需要告訴系統如何找到剛安裝好的
共用函式庫。不需要這麼做的系統包括
FreeBSD、
Linux、
NetBSD、OpenBSD 與
Solaris。

設定共用函式庫搜尋路徑的方法因平台而異，但最普遍使用的方法，
是設定環境變數 `LD_LIBRARY_PATH`，作法如下：
在 Bourne shell（`sh`、`ksh`、`bash`、`zsh`）中：

```

LD_LIBRARY_PATH=/usr/local/pgsql/lib
export LD_LIBRARY_PATH
```

或在 `csh` 或 `tcsh` 中：

```

setenv LD_LIBRARY_PATH /usr/local/pgsql/lib
```

請將 `/usr/local/pgsql/lib` 替換成你在
[步驟 1](install-make.md#CONFIGURE) 中所設定的
`--libdir`。你應該將這些指令放進 shell 啟動檔中，
例如 `/etc/profile` 或 `~/.bash_profile`。
關於這個方法相關的注意事項，可以在
<http://xahlee.info/UnixResource_dir/_/ldpath.html>
找到一些不錯的資訊。

在部分系統上，可能比較適合在建置之前，先設定環境變數
`LD_RUN_PATH`。

在 Cygwin 上，請將函式庫目錄放進
`PATH`，或是將 `.dll`
檔案搬到 `bin` 目錄中。

如果有疑問，請參閱你系統的手冊頁面（可能是
`ld.so` 或 `rld`）。如果你之後
看到類似下面這樣的訊息：

```

psql: error in loading shared libraries
libpq.so.2.1: cannot open shared object file: No such file or directory
```

那就代表這個步驟是必要的。到時候處理即可。

<a id="id-1.6.4.8.2.8.1"></a>
如果你使用的是 Linux，且擁有 root
權限，可以在安裝完成後執行：

```

/sbin/ldconfig /usr/local/pgsql/lib
```

（或相對應的目錄），以讓執行期連結器能更快找到共用函式庫。
關於更多資訊，請參閱 `ldconfig` 的手冊頁面。
在 FreeBSD、NetBSD 與 OpenBSD 上，指令則是：

```

/sbin/ldconfig -m /usr/local/pgsql/lib
```

其他系統則不確定是否有相對應的指令。

<a id="INSTALL-POST-ENV-VARS"></a>

### 17.5.2. 環境變數 [#](#INSTALL-POST-ENV-VARS)

<a id="id-1.6.4.8.3.2"></a>

如果你安裝到 `/usr/local/pgsql`，或其他預設不會
搜尋程式的位置，你應該將 `/usr/local/pgsql/bin`
（或你在[步驟 1](install-make.md#CONFIGURE)中設定的
`--bindir`）加進你的 `PATH` 中。
嚴格來說，這並非必要，但這樣會讓使用
PostgreSQL 更加方便。

若要這麼做，請將下列內容加進你的 shell 啟動檔中，例如
`~/.bash_profile`（或 `/etc/profile`，
如果你想讓所有使用者都受影響的話）：

```

PATH=/usr/local/pgsql/bin:$PATH
export PATH
```

如果你使用的是 `csh` 或 `tcsh`，請使用這個指令：

```

set path = ( /usr/local/pgsql/bin $path )
```

<a id="id-1.6.4.8.3.5.1"></a>
若要讓你的系統能找到 man
文件，除非你安裝到預設會被搜尋的位置，否則你需要在
shell 啟動檔中加入類似下面的內容：

```

MANPATH=/usr/local/pgsql/share/man:$MANPATH
export MANPATH
```

環境變數 `PGHOST` 與 `PGPORT`
會告訴用戶端應用程式資料庫伺服器的主機與埠號，
覆寫編譯時內建的預設值。如果你打算讓用戶端應用程式
從遠端連線，那麼讓每個打算使用該資料庫的使用者都設定
`PGHOST`，會比較方便。不過，這並非必要；
這些設定值也可以透過命令列選項，傳給大多數的用戶端程式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-post.html)（原文版本：18.6；核對日期：2026-09-25）
