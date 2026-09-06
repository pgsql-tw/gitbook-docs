## 30.1. What Is JIT compilation? [#](#JIT-REASON)

[30.1.1. JIT Accelerated Operations](jit-reason.md#JIT-ACCELERATED-OPERATIONS)

[30.1.2. Inlining](jit-reason.md#JIT-INLINING)

[30.1.3. Optimization](jit-reason.md#JIT-OPTIMIZATION)

Just-in-Time (JIT) compilation is the process of turning
some form of interpreted program evaluation into a native program, and
doing so at run time.
For example, instead of using general-purpose code that can evaluate
arbitrary SQL expressions to evaluate a particular SQL predicate
like `WHERE a.col = 3`, it is possible to generate a
function that is specific to that expression and can be natively executed
by the CPU, yielding a speedup.

PostgreSQL has builtin support to perform
JIT compilation using [LLVM](https://llvm.org/) when
PostgreSQL is built with
[`--with-llvm`](../installation/install-make.md#CONFIGURE-WITH-LLVM).

See `src/backend/jit/README` for further details.

<a id="JIT-ACCELERATED-OPERATIONS"></a>

### 30.1.1. JIT Accelerated Operations [#](#JIT-ACCELERATED-OPERATIONS)

Currently PostgreSQL's JIT
implementation has support for accelerating expression evaluation and
tuple deforming. Several other operations could be accelerated in the
future.

Expression evaluation is used to evaluate `WHERE`
clauses, target lists, aggregates and projections. It can be accelerated
by generating code specific to each case.

Tuple deforming is the process of transforming an on-disk tuple (see [Section 66.6.1](../../internals/storage/storage-page-layout.md#STORAGE-TUPLE-LAYOUT)) into its in-memory representation.
It can be accelerated by creating a function specific to the table layout
and the number of columns to be extracted.

<a id="JIT-INLINING"></a>

### 30.1.2. Inlining [#](#JIT-INLINING)

PostgreSQL is very extensible and allows new
data types, functions, operators and other database objects to be defined;
see [Chapter 36](../../server-programming/extend/README.md). In fact the built-in objects are implemented
using nearly the same mechanisms. This extensibility implies some
overhead, for example due to function calls (see [Section 36.3](../../server-programming/extend/xfunc.md)).
To reduce that overhead, JIT compilation can inline the
bodies of small functions into the expressions using them. That allows a
significant percentage of the overhead to be optimized away.

<a id="JIT-OPTIMIZATION"></a>

### 30.1.3. Optimization [#](#JIT-OPTIMIZATION)

LLVM has support for optimizing generated
code. Some of the optimizations are cheap enough to be performed whenever
JIT is used, while others are only beneficial for
longer-running queries.
See <https://llvm.org/docs/Passes.html#transform-passes> for
more details about optimizations.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-reason.html)（英文原文，待翻譯）
