# 16.3. Getting The Source

The PostgreSQL 10.5 sources can be obtained from the download section of our website: [https://www.postgresql.org/download/](https://www.postgresql.org/download/). You should get a file named `postgresql-10.5.tar.gz` or `postgresql-10.5.tar.bz2`. After you have obtained the file, unpack it:

```text
gunzip postgresql-10.5.tar.gz
tar xf postgresql-10.5.tar
```

\(Use `bunzip2` instead of `gunzip` if you have the `.bz2` file.\) This will create a directory `postgresql-10.5` under the current directory with the PostgreSQL sources. Change into that directory for the rest of the installation procedure.

You can also get the source directly from the version control repository, see [Appendix I](https://www.postgresql.org/docs/10/static/sourcerepo.html).

