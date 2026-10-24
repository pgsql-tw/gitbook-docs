<a id="ECPG-CPP"></a>

## 34.13. C++ 應用程式 [#](#ECPG-CPP)

[34.13.1. 主機變數的作用域](ecpg-cpp.md#ecpg-cpp-scope)

[34.13.2. 搭配外部 C 模組開發 C++ 應用程式](ecpg-cpp.md#ecpg-cpp-and-c)

ECPG 對 C++ 應用程式提供有限的支援。本節說明一些需要注意的事項。

`ecpg` 前置處理器接受以 C（或類似 C 的語言）撰寫並含有嵌入式 SQL 命令的輸入檔，將嵌入式 SQL 命令轉換為 C 語言片段，最後產生 `.c` 檔。`ecpg` 所產生的 C 語言片段會用到一些函式庫函式，這些函式在標頭檔中的宣告於 C++ 下使用時，會包在 `extern "C" { ... }` 區塊中，因此應該可以在 C++ 中順暢運作。

然而，一般而言，`ecpg` 前置處理器只理解 C；它不處理 C++ 語言的特殊語法與保留字。因此，寫在使用了 C++ 特有複雜功能之 C++ 應用程式碼中的某些嵌入式 SQL 程式碼，可能無法被正確地前置處理，或可能無法如預期運作。

在 C++ 應用程式中使用嵌入式 SQL 程式碼的一種安全方式，是將 ECPG 呼叫隱藏在 C 模組中，由 C++ 應用程式碼呼叫該模組來存取資料庫，再將它與其餘的 C++ 程式碼連結在一起。相關說明請參閱[第 34.13.2 節](ecpg-cpp.md#ecpg-cpp-and-c)。

<a id="ECPG-CPP-SCOPE"></a>

### 34.13.1. 主機變數的作用域 [#](#ecpg-cpp-scope) <a href="#ecpg-cpp-scope" id="ecpg-cpp-scope"></a>

`ecpg` 前置處理器理解 C 中變數的作用域。在 C 語言中，這相當簡單，因為變數的作用域是以其所在的程式碼區塊為準。然而在 C++ 中，類別成員變數是在與宣告位置不同的程式碼區塊中被參照，因此 `ecpg` 前置處理器無法理解類別成員變數的作用域。

例如，在下列情況中，`ecpg` 前置處理器在 `test` 方法中找不到變數 `dbname` 的任何宣告，因此會發生錯誤。

```

class TestCpp
{
    EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
    EXEC SQL END DECLARE SECTION;

  public:
    TestCpp();
    void test();
    ~TestCpp();
};

TestCpp::TestCpp()
{
    EXEC SQL CONNECT TO testdb1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
}

void Test::test()
{
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current_database = %s\n", dbname);
}

TestCpp::~TestCpp()
{
    EXEC SQL DISCONNECT ALL;
}
```

譯註：上方範例中 test 方法的定義原文寫作 Test::test()，但類別名稱是 TestCpp，正確應為 TestCpp::test()（下文修改後的版本即寫作 TestCpp::test()）。範例程式碼依原文保留；此處的錯字與本例要說明的作用域問題無關。

這段程式碼會產生類似下面的錯誤：

```

ecpg test_cpp.pgc
test_cpp.pgc:28: ERROR: variable "dbname" is not declared
```

為了避免這個作用域問題，可以修改 `test` 方法，改用區域變數作為中介儲存區。但這種做法只是拙劣的權宜之計，因為它會讓程式碼變得難看，也會降低效能。

```

void TestCpp::test()
{
    EXEC SQL BEGIN DECLARE SECTION;
    char tmp[1024];
    EXEC SQL END DECLARE SECTION;

    EXEC SQL SELECT current_database() INTO :tmp;
    strlcpy(dbname, tmp, sizeof(tmp));

    printf("current_database = %s\n", dbname);
}
```

譯註：上方範例中的 strlcpy 並非標準 C 函式，部分平台的 C 函式庫並未提供（例如 glibc 2.38 之前的版本），此時需改用其他字串複製方式（例如 snprintf）。範例程式碼依原文保留。

<a id="ECPG-CPP-AND-C"></a>

### 34.13.2. 搭配外部 C 模組開發 C++ 應用程式 [#](#ecpg-cpp-and-c) <a href="#ecpg-cpp-and-c" id="ecpg-cpp-and-c"></a>

如果你了解 `ecpg` 前置處理器在 C++ 中的這些技術限制，你可能會得出這樣的結論：在連結階段將 C 目的檔與 C++ 目的檔連結起來，讓 C++ 應用程式得以使用 ECPG 功能，可能比直接在 C++ 程式碼中撰寫嵌入式 SQL 命令更好。本節以一個簡單的範例，說明如何將嵌入式 SQL 命令從 C++ 應用程式碼中分離出來。在此範例中，應用程式以 C++ 實作，而連線到 PostgreSQL 伺服器的部分則使用 C 與 ECPG。

需要建立三種檔案：C 檔（`*.pgc`）、標頭檔，以及 C++ 檔：

<a id="ECPG-CPP-AND-C-TEST-MOD-PGC"></a>

`test_mod.pgc` [#](#ECPG-CPP-AND-C-TEST-MOD-PGC)
:   用來執行嵌入在 C 中之 SQL 命令的副程式模組。它會由前置處理器轉換為 `test_mod.c`。

    ```

    #include "test_mod.h"
    #include <stdio.h>

    void
    db_connect()
    {
        EXEC SQL CONNECT TO testdb1;
        EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    }

    void
    db_test()
    {
        EXEC SQL BEGIN DECLARE SECTION;
        char dbname[1024];
        EXEC SQL END DECLARE SECTION;

        EXEC SQL SELECT current_database() INTO :dbname;
        printf("current_database = %s\n", dbname);
    }

    void
    db_disconnect()
    {
        EXEC SQL DISCONNECT ALL;
    }
    ```
<a id="ECPG-CPP-AND-C-TEST-MOD-H"></a>

`test_mod.h` [#](#ECPG-CPP-AND-C-TEST-MOD-H)
:   宣告 C 模組（`test_mod.pgc`）中各函式的標頭檔，由 `test_cpp.cpp` 引入。由於它會被 C++ 模組連結使用，此檔案必須以 `extern "C"` 區塊包住這些宣告。

    ```

    #ifdef __cplusplus
    extern "C" {
    #endif

    void db_connect();
    void db_test();
    void db_disconnect();

    #ifdef __cplusplus
    }
    #endif
    ```
<a id="ECPG-CPP-AND-C-TEST-CPP-CPP"></a>

`test_cpp.cpp` [#](#ECPG-CPP-AND-C-TEST-CPP-CPP)
:   應用程式的主要程式碼，包含 `main` 常式，以及本例中的一個 C++ 類別。

    ```

    #include "test_mod.h"

    class TestCpp
    {
      public:
        TestCpp();
        void test();
        ~TestCpp();
    };

    TestCpp::TestCpp()
    {
        db_connect();
    }

    void
    TestCpp::test()
    {
        db_test();
    }

    TestCpp::~TestCpp()
    {
        db_disconnect();
    }

    int
    main(void)
    {
        TestCpp *t = new TestCpp();

        t->test();
        return 0;
    }
    ```

    譯註：上方 test_cpp.cpp 的 main 以 new 建立 TestCpp 物件後並未 delete，因此解構函式不會被呼叫，db_disconnect() 也就不會執行；若要如類別設計所預期在結束前中斷連線，應在 return 之前加上 delete t;。範例程式碼依原文保留。

要建置此應用程式，請依下列步驟進行。執行 `ecpg` 將 `test_mod.pgc` 轉換為 `test_mod.c`，再以 C 編譯器編譯 `test_mod.c` 產生 `test_mod.o`：

```

ecpg -o test_mod.c test_mod.pgc
cc -c test_mod.c -o test_mod.o
```

接著，以 C++ 編譯器編譯 `test_cpp.cpp`，產生 `test_cpp.o`：

```

c++ -c test_cpp.cpp -o test_cpp.o
```

最後，使用 C++ 編譯器驅動程式，將 `test_cpp.o` 與 `test_mod.o` 這兩個目的檔連結成一個執行檔：

```

c++ test_cpp.o test_mod.o -lecpg -o test_cpp
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-cpp.html)（原文版本：18.6；核對日期：2026-10-22）
