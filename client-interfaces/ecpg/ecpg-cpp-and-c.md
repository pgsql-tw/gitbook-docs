<a id="ECPG-CPP-AND-C"></a>

## 34.13.2. 搭配外部 C 模組開發 C++ 應用程式 [#](#ecpg-cpp-and-c) <a href="#ecpg-cpp-and-c" id="ecpg-cpp-and-c"></a>

如果你了解 `ecpg` 前置處理器在 C++ 中的這些技術限制，你可能會得出這樣的結論：在連結階段將 C 目的檔與 C++ 目的檔連結起來，讓 C++ 應用程式得以使用 ECPG 功能，可能比直接在 C++ 程式碼中撰寫嵌入式 SQL 命令更好。本節以一個簡單的範例，說明如何將嵌入式 SQL 命令從 C++ 應用程式碼中分離出來。在此範例中，應用程式以 C++ 實作，而連線到 PostgreSQL 伺服器的部分則使用 C 與 ECPG。

需要建立三種檔案：C 檔（`*.pgc`）、標頭檔，以及 C++ 檔：

<a id="ECPG-CPP-AND-C-TEST-MOD-PGC"></a>

### `test_mod.pgc` [#](#ecpg-cpp-and-c-test-mod-pgc) <a href="#ecpg-cpp-and-c-test-mod-pgc" id="ecpg-cpp-and-c-test-mod-pgc"></a>

用來執行嵌入在 C 中之 SQL 命令的副程式模組。它會由前置處理器轉換為 `test_mod.c`。

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

### `test_mod.h` [#](#ecpg-cpp-and-c-test-mod-h) <a href="#ecpg-cpp-and-c-test-mod-h" id="ecpg-cpp-and-c-test-mod-h"></a>

宣告 C 模組（`test_mod.pgc`）中各函式的標頭檔，由 `test_cpp.cpp` 引入。由於它會被 C++ 模組連結使用，此檔案必須以 `extern "C"` 區塊包住這些宣告。

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

### `test_cpp.cpp` [#](#ecpg-cpp-and-c-test-cpp-cpp) <a href="#ecpg-cpp-and-c-test-cpp-cpp" id="ecpg-cpp-and-c-test-cpp-cpp"></a>

應用程式的主要程式碼，包含 `main` 常式，以及本例中的一個 C++ 類別。

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

[返回 34.13. C++ 應用程式](ecpg-cpp.md#ecpg-cpp)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-cpp.html)（原文版本：18.6；核對日期：2026-10-22）
