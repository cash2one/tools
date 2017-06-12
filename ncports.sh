#!/bin/bash
cd /root/csy/scripts
#检测服务器端口是否开放，成功会返回0值，打不开会返回1值
cat ip-ports.txt | while read line
do
  nc -w 10 -z $line > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo $line:ok
  else
    echo $line:fail
    echo "Server $line port impassability, please deal with as soon as possible" |mutt -s "【Machine room monitoring】server $line Port impassability" chenshiyang460@emao.com,gaojie419@emao.com,zhangyafeng097@emao.com,shengkuang380@emao.com
fi
done
