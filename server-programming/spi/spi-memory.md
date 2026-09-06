## 45.3. Memory Management [#](#SPI-MEMORY)

[SPI_palloc](spi-spi-palloc.md) — allocate memory in the upper executor context

[SPI_repalloc](spi-realloc.md) — reallocate memory in the upper executor context

[SPI_pfree](spi-spi-pfree.md) — free memory in the upper executor context

[SPI_copytuple](spi-spi-copytuple.md) — make a copy of a row in the upper executor context

[SPI_returntuple](spi-spi-returntuple.md) — prepare to return a tuple as a Datum

[SPI_modifytuple](spi-spi-modifytuple.md) — create a row by replacing selected fields of a given row

[SPI_freetuple](spi-spi-freetuple.md) — free a row allocated in the upper executor context

[SPI_freetuptable](spi-spi-freetupletable.md) — free a row set created by `SPI_execute` or a similar function

[SPI_freeplan](spi-spi-freeplan.md) — free a previously saved prepared statement

<a id="id-1.8.12.10.2.1"></a>
PostgreSQL allocates memory within
*memory contexts*, which provide a convenient method of
managing allocations made in many different places that need to
live for differing amounts of time. Destroying a context releases
all the memory that was allocated in it. Thus, it is not necessary
to keep track of individual objects to avoid memory leaks; instead
only a relatively small number of contexts have to be managed.
`palloc` and related functions allocate memory
from the “current” context.

`SPI_connect` creates a new memory context and
makes it current. `SPI_finish` restores the
previous current memory context and destroys the context created by
`SPI_connect`. These actions ensure that
transient memory allocations made inside your C function are
reclaimed at C function exit, avoiding memory leakage.

However, if your C function needs to return an object in allocated
memory (such as a value of a pass-by-reference data type), you
cannot allocate that memory using `palloc`, at
least not while you are connected to SPI. If you try, the object
will be deallocated by `SPI_finish`, and your
C function will not work reliably. To solve this problem, use
`SPI_palloc` to allocate memory for your return
object. `SPI_palloc` allocates memory in the
“upper executor context”, that is, the memory context
that was current when `SPI_connect` was called,
which is precisely the right context for a value returned from your
C function. Several of the other utility functions described in
this section also return objects created in the upper executor context.

When `SPI_connect` is called, the private
context of the C function, which is created by
`SPI_connect`, is made the current context. All
allocations made by `palloc`,
`repalloc`, or SPI utility functions (except as
described in this section) are made in this context. When a
C function disconnects from the SPI manager (via
`SPI_finish`) the current context is restored to
the upper executor context, and all allocations made in the
C function memory context are freed and cannot be used any more.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-memory.html)（英文原文，待翻譯）
