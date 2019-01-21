# 70. How the Planner Uses Statistics

This chapter builds on the material covered in [Section 14.1](https://www.postgresql.org/docs/10/static/using-explain.html) and [Section 14.2](https://www.postgresql.org/docs/10/static/planner-stats.html) to show some additional details about how the planner uses the system statistics to estimate the number of rows each part of a query might return. This is a significant part of the planning process, providing much of the raw material for cost calculation.

The intent of this chapter is not to document the code in detail, but to present an overview of how it works. This will perhaps ease the learning curve for someone who subsequently wishes to read the code.

