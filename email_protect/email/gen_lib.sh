#!/bin/bash
target_dir=build
#rm -rf ${target_dir}
mkdir -p ${target_dir}
cp -rfv *.py ${target_dir}
echo "scbu_diags_email_info=\"\"\"" >> ${target_dir}/email_utils.py
./crypto_test.py enc_file $1 >> ${target_dir}/email_utils.py
echo  "\"\"\"" >> ${target_dir}/email_utils.py
cd ${target_dir}

# we can still do more protections with upx
python3 setup.py build_ext
cd ..
find ${target_dir} -name "*.so" |xargs -i cp -rfv {} lib/
cd lib
md5sum *.so  > md5sum.txt
cd ..