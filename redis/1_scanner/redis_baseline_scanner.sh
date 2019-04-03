#!/bin/bash

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
    echo -e "\t\t<section id=\"$1\">" >> $xml_file_name
}
closeSection(){
    echo -e "\t\t</section>" >> $xml_file_name
}
createNode(){
    echo -e "\t\t\t<node id=\"$1\">" >> $xml_file_name
}
closeNode(){
    echo -e "\t\t\t</node>" >> $xml_file_name
}

# 各检测项生成报告函数
appendToXml(){
    echo -e "\t\t\t\t<item id="\"$id\"">" >> $xml_file_name
    echo -e "\t\t\t\t\t<check_object>$1</check_object>" >> $xml_file_name
    echo -e "\t\t\t\t\t<check_command>$2</check_command>" >> $xml_file_name
    echo -e "\t\t\t\t\t<check_comment>$3</check_comment>" >> $xml_file_name
    echo -e "\t\t\t\t\t<check_result>$4</check_result>" >> $xml_file_name
    echo -e "\t\t\t\t</item>" >> $xml_file_name
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

# 获取主机基本信息
getHostInfo(){
    hostname=`hostname`
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    os_version=`lsb_release -d |cut -d":" -f 2`
    kernel_version=`uname -r`
    tcp_services=`netstat -tlnp|grep tcp`
    udp_service=`netstat -ulnp|grep udp`
    echo -e "\t<hostinfo>" >> $xml_file_name
    echo -e "\t\t<hostname>$hostname</hostname>" >> $xml_file_name
    echo -e "\t\t<ipaddr>$ipaddr</ipaddr>" >> $xml_file_name
    echo -e "\t\t<os_version>$os_version</os_version>" >> $xml_file_name
    echo -e "\t\t<kernel_version>$kernel_version</kernel_version>" >> $xml_file_name
    echo -e "\t\t<tcp_services>$tcp_services</tcp_services>" >> $xml_file_name
    echo -e "\t\t<udp_services>$udp_service</udp_services>" >> $xml_file_name
    echo -e "\t</hostinfo>" >> $xml_file_name
}

# 为redis设置密码
checkRedisPassword(){
    grep_flag="^requirepass\s*\w{1,}"
    check_command="searchValueByReg $CONF_PATH \"$grep_flag\""
    check_comment="为redis设置密码"
    check_result=`eval $check_command`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

# 禁用高危命令FLUSHALL、FLUSHDB、KEYS
checkRedisDangerCommand(){
    grep_flag="^rename-command\s*\w{1,}"
    check_command="searchValueByReg $CONF_PATH \"$grep_flag\""
    check_comment="禁用高危命令FLUSHALL、FLUSHDB、KEYS"
    check_result=`eval $check_command`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

# 建议只监听本地地址
checkRedisAddress(){
    grep_flag="^bind\s*"
    check_command="searchValueByReg $CONF_PATH $grep_flag"
    check_comment="建议只监听本地地址"
    check_result=`eval $check_command`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

# 禁止以root用户运行
# ps -ef |grep $CATALINA_HOME|grep -v grep
checkRedisRunner(){
    grep_flag="redis-server"
    check_command="ps -ef |grep $grep_flag|grep -v grep"
    check_comment="禁止以root用户运行"
    check_result=`eval $check_command`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

# 确认redis是最新版本
checkRedisVersion(){
    check_object='$SERVER_PATH'
    check_command="$SERVER_PATH -v"
    check_comment="确认redis是最新版本"
    check_result=`eval $check_command`
    appendToXml "$check_object" "$check_command" "$check_comment" "$check_result"
}

usage(){
  echo "
Usage:
  -s, --server_path     redis_server absolutely path, default /opt/redis-5.0/bin/redis-server
  -c, --conf_path       redis config file, default /opt/redis-5.0/conf/redis.conf
  -h, --help            display this help and exit

  example1: bash redis_baseline_scanner.sh -s/opt/redis-5.0/bin/redis-server -c/opt/redis-5.0/conf/redis.conf
  example2: bash redis_baseline_scanner.sh --server_path=/opt/redis-5.0/bin/redis-server -conf_path=/opt/redis-5.0/conf/redis.conf
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o s:c:h --long server_path:,conf_path:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0
    SERVER_PATH='/opt/redis-5.0/bin/redis-server'
    CONF_PATH='/opt/redis-5.0/conf/redis.conf'

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
    xml_file_name="/tmp/${ipaddr}_redis_info.xml"
}

main(){
    main_pre $@
    createReportXml
        getHostInfo
        createChecklist
            createSection "checkRedisPassword"
                checkRedisPassword
            closeSection
            createSection "checkRedisDangerCommand"
                checkRedisDangerCommand
            closeSection
            createSection "checkRedisAddress"
                checkRedisAddress
            closeSection
            createSection "checkRedisRunner"
                checkRedisRunner
            closeSection
            createSection "checkRedisVersion"
                checkRedisVersion
            closeSection
        closeChecklist
    closeReportXml
}

main $@