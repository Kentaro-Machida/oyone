# bash
source oyonepy_env/bin/activate
python3 main.py -s -ss --mode manual -os linux
vcgencmd measure_temp
du -shc ./data
