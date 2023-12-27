======================
What's New
======================

v0.6
==========

* Converted utils and main lib to cffi's API mode for better `performance`_
* Added inline type hints and stubs for the C extension part
* Added unit tests and ruff formatter
* `utils.try_open_single_program` now returns `ProgramHandle` instead of returning the pointer directly, and `utils.close_single_program` accepts that object (used to accept the pointer)
  should be safe, unless somebody relied on it being a `CData` object


.. _`performance`: https://cffi.readthedocs.io/en/latest/overview.html#purely-for-performance-api-level-out-of-line

=======


Older Versions
==============


v0.5
------

* initial public release with most samples ported from the original