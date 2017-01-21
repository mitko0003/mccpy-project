python3 setup.py build

P=$(ls -d build/lib*)

for fn in `ls $P`; do cp $P/$fn quasirandom/$(echo $fn | cut -d'.' -f 1).so; done

