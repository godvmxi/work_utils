# Instruction
This library will build the password to the so file to protect message leak

# preppare
the library is based on cython to build it to so file, so you may need install some packages to build it
```c
apt install cython3 gcc
apt install python3-pip
pip3 install pycryptodome
```
# usage
## prepare a key file to protect your email user/password info
~/key.txt
```c
{
    "mail":
    {
        "user" :"test@test.com",
        "any_key" :"any_data you want to protect",
        "passwd": "dddddddddddd"
    }
}

```
## use the gen_lib.sh to update the library
it will generate the new library and md5 hash file
```bash
#./gen_lib.sh ~/key.txt
#ls lib/
email_utils.cpython-39-x86_64-linux-gnu.so  md5sum.txt
```
NOTE:you may need to build the library for all python3 version, such as 3.5,3.9 and so on
