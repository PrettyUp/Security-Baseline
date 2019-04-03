#!/bin/bash
xml_file_name='/tmp/192.168.220.143_redis_fix.log'
CATALINA_HOME='/etc/mysql/mysql.conf.d'
id=0

createReportXml(){
    echo '<?xml version="1.0" encoding="UTF-8"?>' > $xml_file_name
    echo '<root>' >> $xml_file_name
}
closeReportXml(){
    echo '</root>' >> $xml_file_name
}
createChecklist(){
    echo -e "\t<checklist>" >> $xml_file_name
}
closeChecklist(){
    echo -e "\t</checklist>" >> $xml_file_name
}
createSection(){
    echo -e "\t\t<section id="$1">" >> $xml_file_name
}
closeSection(){
    echo -e "\t\t</section>" >> $xml_file_name
}
createNode(){
    echo -e "\t\t\t<node id="$1">" >> $xml_file_name
}
closeNode(){
    echo -e "\t\t\t</node>" >> $xml_file_name
}

# 各检测项生成报告函数
appendToXml(){
    echo -e "\t<item id=""$id"">" >> $xml_file_name
    echo -e "\t\t<fix_time>$(date  +'%Y-%m-%d 星期%w %H:%M:%S')</fix_time>" >> $xml_file_name
    echo -e "\t\t<fix_object>$1</fix_object>" >> $xml_file_name
    echo -e "\t\t<fix_command>$2</fix_command>" >> $xml_file_name
    echo -e "\t\t<fix_comment>$3</fix_comment>" >> $xml_file_name
    echo -e "\t\t<fix_result>$4</fix_result>" >> $xml_file_name
    echo -e "\t</item>" >> $xml_file_name
    id=`expr $id + 1`
}

# 用于通过传输过来的文件与正则查找匹配
searchValueByReg(){
    file_name=$1
    regexp=$2
    found_flag="0"
    if ! [ -e $file_name ]
    then
        echo "file $file_name not found"
        return 1
    fi
    while read line
    do
        result=`echo $line | grep -E $regexp`
        if [ -n "$result" ]
        then
            found_flag="1"
            echo "$result"
            break
        fi
    done <<< "$(cat $file_name)"
    if [ $found_flag == "0" ]
    then
        echo "not found"
    fi
}
            
fixRedisDangerCommand(){
    fix_object="^rename-command\s*\w{1,}"
    fix_comment="禁用高危命令FLUSHALL、FLUSHDB、KEYS"
    fix_command="echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHALL \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command FLUSHDB \\\"\\\"\" >> $CONF_PATH;echo -e \"rename-command KEYS \\\"\\\"\" >> $CONF_PATH;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        
usage(){
  echo "
Usage:
  -s, --server_path     redis_server absolutely path, default /opt/redis-5.0/bin/redis-server
  -c, --conf_path       redis config file, default /opt/redis-5.0/conf/redis.conf
  -p, --password        the password to set while redis have no password, default t*tsrch0st
  -h, --help            display this help and exit

  example1: bash redis_fix.sh -s/opt/redis-5.0/bin/redis-server -c/opt/redis-5.0/conf/redis.conf -pt*tsrch0st
  example2: bash redis_fix.sh --server_path=/opt/redis-5.0/bin/redis-server --conf_path=/opt/redis-5.0/conf/redis.conf --password=t*tsrch0st
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o s:c:p:h --long server_path:,conf_path:,password:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0
    SERVER_PATH='/opt/redis-5.0/bin/redis-server'
    CONF_PATH='/opt/redis-5.0/conf/redis.conf'
    PASSWORD="t*tsrch0st"

    while true
    do
      case "$1" in
      -s|--server_path)
          SERVER_PATH="$2"
          shift
          ;;
      -c|--conf_path)
          CONF_PATH="$2"
          shift
          ;;
      -p|--password)
          PASSWORD="$2"
          shift
          ;;
      -h|--help)
          usage
          exit
          ;;
      --)
        shift
        break
        ;;
      *)
        echo "$1 is not option"
        ;;
      esac
      shift
    done
    xml_file_name="/tmp/${ipaddr}_redis_fix.log"
}
main(){
    main_pre $@
    createReportXml
		fixRedisDangerCommand
	closeReportXml
}

main $@
