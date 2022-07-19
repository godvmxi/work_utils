
# System info
Dependence
- Ubuntu 18.04 X64 (related Linux distrbutions are also fine),
- GCC
- cmake

**NOTE** i386 may have trouble on file limit
# Directory
```bash
$ tree
.
├── .vscode         # vscode config directory
├── .git            # git local repo
├── data            # test data directory, will install 
├── CMakeLists.txt  #cmake file
├── data            # test data directory, will install to output dir
│   └── dat_0.txt   # normal file
│   └── dat_0.txt   # contain empty line and wrong format
├── largest_x.cpp   #main code
└── README.md       #markdown help file

```
# Confusing issue
The question do not cover a scenario clearly, similar as the pdf example, there are four records in the file:
```bash
0001 200
0002 200
0003 115
0004 110
````
There are two records wtih value 200, But when X = 1,which choice should we take ? 
1. Drop one of ids of the 200  ?? 
2. Print them all ??

So I add a parameter(drop_duplcate), when it set to 1, and second records with value 200 will be dropped.
```bash
# output when drop_duplcate = 1
0001
# output when drop_duplcate = 0
0001
0002
```
# Build the code
```bash
mkdir build &&cd build
cmake  -DCMAKE_BUILD_TYPE=Debug  ../
cmake  -DCMAKE_BUILD_TYPE=Release  ../
make install
```
# Run the code
## Help from App
```bash
bright@vm:~/code/demo_code/largest_x/build$ ./largest_x 
Usage: 

  read from file 
    ./largest_x largtest_x drop_duplcate [filePath] 

  read from stdin
    cat your_file | ./largest_x largtest_x drop_duplcate

  para : 
    largtest_x    : X value
    drop_duplcate : remove the the min & same value ids when largtest_x is less then real ids num
		Take the example in pdf [200,200,115,110] and X = 1
		 0: output: 
			  ids of the first 200 
			  ids of the second 200 
		 1: output: 
			  ids of the first 200
```
## Read from file
```bash
bright@vm:~/code/demo_code/largest_x/build$  ./largest_x 3  1  data/dat_0.txt 
00000003
00000001
00000002

```
## Read from stdin
```bah
$ cat ../data/dat_0.txt |./largest_x  3 1 
00000003
00000001
00000002
```
# Robust
the dat_1.txt contail empty line and wrong format, the code will skip it and try to move on.

maybe we should consider more io error, but I think it is enough for the code test.