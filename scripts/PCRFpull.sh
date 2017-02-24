#!/usr/bin/expect -f
spawn mkdir -p /stage
spawn scp root@10.53.212.105:/stage/BSR9.9/pcrf/* /stage/
expect "(yes/no)?"
send "yes\r"
expect "password:"
send "amdocs\r"
expect "*\r"
sleep 5
expect "\r"
spawn scp root@10.53.212.105:/stage/iso/* /stage/
expect "password:"
send "amdocs\r"
expect "*\r"
sleep 60
expect "\r"
