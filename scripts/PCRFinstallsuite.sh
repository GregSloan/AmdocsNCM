#!/usr/bin/expect -f
spawn yum install /stage/BPCttdb-49RELv0_27-hga00a00057885.el6.x86_64.rpm
sleep 2
expect ":"
send "y\r"
expect "*\r"
sleep 10
expect "\r"
sleep 10
spawn yum install /stage/BPCsnmp-49RELv0_16-hga00a00049718.el6.x86_64.rpm
sleep 2
expect ":"
send "y\r"
expect "*\r"
sleep 10
expect "\r"
sleep 10
spawn yum install /stage/BPCapps-49RELv0_30-hga00a00059206.el6.x86_64.rpm
sleep 2
expect ":"
send "y\r"
expect "*\r"
sleep 5
expect "\r"
sleep 10

