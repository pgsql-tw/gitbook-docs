## N.2. Configuring the Colors [#](#COLOR-WHICH)

The actual colors to be used are configured using the environment variable
`PG_COLORS`<a id="id-1.11.15.5.2.2"></a>
(note plural). The value is a colon-separated list of
`key=value`
pairs. The keys specify what the color is to be used for. The values are
SGR (Select Graphic Rendition) specifications, which are interpreted by the
terminal.

The following keys are currently in use:

`error`
:   used to highlight the text “error” in error messages

`warning`
:   used to highlight the text “warning” in warning
    messages

`note`
:   used to highlight the text “detail” and
    “hint” in such messages

`locus`
:   used to highlight location information (e.g., program name and
    file name) in messages

The default value is
`error=01;31:warning=01;35:note=01;36:locus=01`
(`01;31` = bold red, `01;35` = bold
magenta, `01;36` = bold cyan, `01` = bold
default color).

### Tip

This color specification format is also used by other software packages
such as GCC, GNU
coreutils, and GNU grep.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/color-which.html)（英文原文，待翻譯）
