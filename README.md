this project is configured with cmake

to build:

```
cmake -S . -B build
cmake --build build
```

on windows I had trouble with Sigc++ pkg-config include\_dirs where it wouldn't put both the include and lib includes folders in the variable if it was installed with Program Files. So I hacked cmake FindPkgConfig to get the right value, then ran into trouble getting the Boehm Garbage collector working on windows 
