# F.1. adminpack

adminpack 提供了許多支援性質的函數，pgAdmin 和其他管理工具可以用來提供其他功能，例如伺服器日誌檔案的遠程管理。預設情況下，僅超級使用者可以使用所有的這些函數，但使用 GRANT 指令可以允許其他使用者使用它們。

[Table F.1](adminpack.md#table-f-1-adminpack-functions) 中列出的函數提供了對伺服器的主機上檔案的寫入功能。 （另請參見 [Table 9.99](../../the-sql-language/functions-and-operators/system-administration.md#table-9-95-generic-file-access-functions) 中提供唯讀的功能。）只能存取資料庫叢集目錄中的檔案，除非使用者是超級使用者或具有 pg\_read\_server\_files 或 pg\_write\_server\_files 個角色（視情況而定） ，而相對路徑及絕對路徑都是允許的。

#### **Table F.1. `adminpack` Functions**

| <p>Function</p><p>Description</p>                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>pg_catalog.pg_file_write</code> ( <em><code>filename</code></em> <code>text</code>, <em><code>data</code></em> <code>text</code>, <em><code>append</code></em> <code>boolean</code> ) → <code>bigint</code></p><p>Writes, or appends to, a text file.</p> |
| <p><code>pg_catalog.pg_file_sync</code> ( <em><code>filename</code></em> <code>text</code> ) → <code>void</code></p><p>Flushes a file or directory to disk.</p>                                                                                                    |
| <p><code>pg_catalog.pg_file_rename</code> ( <em><code>oldname</code></em> <code>text</code>, <em><code>newname</code></em> <code>text</code> [, <em><code>archivename</code></em> <code>text</code> ] ) → <code>boolean</code></p><p>Renames a file.</p>           |
| <p><code>pg_catalog.pg_file_unlink</code> ( <em><code>filename</code></em> <code>text</code> ) → <code>boolean</code></p><p>Removes a file.</p>                                                                                                                    |
| <p><code>pg_catalog.pg_logdir_ls</code> () → <code>setof record</code></p><p>Lists the log files in the <code>log_directory</code> directory.</p>                                                                                                                  |

`pg_file_write` writes the specified _`data`_ into the file named by _`filename`_. If _`append`_ is false, the file must not already exist. If _`append`_ is true, the file can already exist, and will be appended to if so. Returns the number of bytes written.

pg\_file\_sync fsyncs filename 所指定檔案或目錄。 失敗時會拋出錯誤（例如，指定的路徑不存在）。 請注意，[data\_sync\_retry](../../server-administration/server-configuration/error-handling.md#data\_sync\_retry-boolean) 對此函數沒有影響，因此即使更新資料庫檔案失敗也不會引發 PANIC 層級的錯誤。

`pg_file_rename` renames a file. If _`archivename`_ is omitted or NULL, it simply renames _`oldname`_ to _`newname`_ (which must not already exist). If _`archivename`_ is provided, it first renames _`newname`_ to _`archivename`_ (which must not already exist), and then renames _`oldname`_ to _`newname`_. In event of failure of the second rename step, it will try to rename _`archivename`_ back to _`newname`_ before reporting the error. Returns true on success, false if the source file(s) are not present or not writable; other cases throw errors.

`pg_file_unlink` removes the specified file. Returns true on success, false if the specified file is not present or the `unlink()` call fails; other cases throw errors.

pg\_logdir\_ls 回傳 [log\_directory](../../server-administration/server-configuration/error-reporting-and-logging.md#log\_directory-string) 目錄中所有日誌檔案的開始時間戳記和路徑名稱。 [log\_filename](../../server-administration/server-configuration/error-reporting-and-logging.md#log\_filename-string) 參數必須有其預設設定 (postgresql-%Y-%m-%d\_%H%M%S.log) 才能使用此功能。
