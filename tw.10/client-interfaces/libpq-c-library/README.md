# 33. libpq - C Library

libpq is the C application programmer's interface to PostgreSQL. libpq is a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.

libpq is also the underlying engine for several other PostgreSQL application interfaces, including those written for C++, Perl, Python, Tcl and ECPG. So some aspects of libpq's behavior will be important to you if you use one of those packages. In particular, [Section 33.14](https://www.postgresql.org/docs/10/static/libpq-envars.html),[Section 33.15](https://www.postgresql.org/docs/10/static/libpq-pgpass.html) and [Section 33.18](https://www.postgresql.org/docs/10/static/libpq-ssl.html) describe behavior that is visible to the user of any application that uses libpq.

Some short programs are included at the end of this chapter \([Section 33.21](https://www.postgresql.org/docs/10/static/libpq-example.html)\) to show how to write programs that use libpq. There are also several complete examples of libpq applications in the directory `src/test/examples` in the source code distribution.

Client programs that use libpq must include the header file `libpq-fe.h` and must link with the libpq library.

