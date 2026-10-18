<a id="LIBPQ-BUILD"></a>

## 32.22. 建置 libpq 程式 [#](#LIBPQ-BUILD)

<a id="id-1.7.3.29.2"></a>

要建置（也就是編譯並連結）使用 libpq 的程式，你需要完成下列所有事項：

* 引入 `libpq-fe.h` 標頭檔：

  ```

  #include <libpq-fe.h>
  ```

  如果你沒有這樣做，通常會從編譯器得到類似下面的錯誤訊息：

  ```

  foo.c: In function `main':
  foo.c:34: `PGconn' undeclared (first use in this function)
  foo.c:35: `PGresult' undeclared (first use in this function)
  foo.c:54: `CONNECTION_BAD' undeclared (first use in this function)
  foo.c:68: `PGRES_COMMAND_OK' undeclared (first use in this function)
  foo.c:95: `PGRES_TUPLES_OK' undeclared (first use in this function)
  ```
* 對編譯器提供 `-Idirectory` 選項，讓編譯器指向 PostgreSQL 標頭檔的安裝目錄。（在某些情況下，編譯器預設就會搜尋該目錄，因此你可以省略這個選項。）例如，你的編譯命令列可能像這樣：

  ```

  cc -c -I/usr/local/pgsql/include testprog.c
  ```

  如果你使用 makefile，請將這個選項加到 `CPPFLAGS` 變數中：

  ```

  CPPFLAGS += -I/usr/local/pgsql/include
  ```

  如果你的程式有可能由其他使用者編譯，就不應該像這樣把目錄位置寫死。你可以改為執行公用程式 `pg_config`<a id="id-1.7.3.29.3.2.2.2.2"></a>，找出本機系統上標頭檔的位置：

  ```

  $ pg_config --includedir
  /usr/local/include
  ```

  如果你已安裝 `pkg-config`<a id="id-1.7.3.29.3.2.2.3.2"></a>，也可以改為執行：

  ```

  $ pkg-config --cflags libpq
  -I/usr/local/include
  ```

  請注意，這樣輸出的內容已經在路徑前面加上了 `-I`。

  未對編譯器指定正確的選項，會產生類似下面的錯誤訊息：

  ```

  testlibpq.c:8:22: libpq-fe.h: No such file or directory
  ```
* 連結最終程式時，請指定 `-lpq` 選項，讓 libpq 函式庫被引入，並指定 `-Ldirectory` 選項，讓編譯器指向 libpq 函式庫所在的目錄。（同樣地，編譯器預設會搜尋某些目錄。）為了獲得最大的可攜性，請將 `-L` 選項放在 `-lpq` 選項之前。例如：

  ```

  cc -o testprog testprog1.o testprog2.o -L/usr/local/pgsql/lib -lpq
  ```

  你也可以使用 `pg_config` 找出函式庫目錄：

  ```

  $ pg_config --libdir
  /usr/local/pgsql/lib
  ```

  或者同樣使用 `pkg-config`：

  ```

  $ pkg-config --libs libpq
  -L/usr/local/pgsql/lib -lpq
  ```

  請再次注意，這會印出完整的選項，而不只是路徑。

  指出這方面問題的錯誤訊息可能如下：

  ```

  testlibpq.o: In function `main':
  testlibpq.o(.text+0x60): undefined reference to `PQsetdbLogin'
  testlibpq.o(.text+0x71): undefined reference to `PQstatus'
  testlibpq.o(.text+0xa4): undefined reference to `PQerrorMessage'
  ```

  這表示你忘了 `-lpq`。

  ```

  /usr/bin/ld: cannot find -lpq
  ```

  這表示你忘了 `-L` 選項，或沒有指定正確的目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-build.html)（原文版本：18.6；核對日期：2026-10-18）
