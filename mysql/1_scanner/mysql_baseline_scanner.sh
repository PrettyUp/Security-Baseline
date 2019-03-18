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

# 禁止以root用户运行
# ps -ef |grep $CATALINA_HOME|grep -v grep
checkMysqlRunner(){
    grep_flag="mysqld"
    check_command="ps -ef |grep $grep_flag|grep -v grep"
    check_comment="禁止以root用户运行"
    check_result=`eval $check_command`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

# 设置最大连接数限制
checkMysqlMaxConnections(){
    mysql_command="show variables like 'max_connections';"
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    check_comment="设置最大连接数限制"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

# 检测是否存在空账号或test账号
checkMysqlNullTestAccount(){
    mysql_command="select user,host,authentication_string from mysql.user where user = '' or user='test';"
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    check_comment="检测是否存在空账号或test账号"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

# 检测是否存在密码为空的账号
checkMysqlNoPassword(){
    mysql_command="select user,host,authentication_string from mysql.user where length(authentication_string) = 0 or authentication_string is null;"
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    check_comment="检测是否存在密码为空的账号"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

# 分角色创建账号同时删除不必要的账号
checkMysqlAccount(){
    mysql_command="select user,host,authentication_string from mysql.user;"
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    check_comment="分角色创建账号同时删除不必要的账号"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

# 开启日志
checkMysqlLog(){
    mysql_command="show variables like \\\"log_%\\\";"
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    echo "$check_command"
    check_comment="开启日志"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

# 确认mysql是最新版本
checkMysqlVersion(){
    mysql_command='select VERSION();'
    check_command="mysql -h${mysql_host} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"${mysql_command}\""
    check_comment="确认mysql是最新版本"
    check_result=`eval $check_command`
    appendToXml "$mysql_command" "$check_command" "$check_comment" "$check_result"
}

usage(){
  echo "
Usage:
  -i, --ip          mysql host ip, default 127.0.0.1
  -P, --port        mysql service port, default 3306
  -u, --user	    mysql service user, default root
  -p, --password    mysql service user's password, default toor
  -h, --help        display this help and exit

  example1: bash mysql_baseline_scanner.sh -h127.0.0.1 -P3306 -uroot -ptoor
  example2: bash mysql_baseline_scanner.sh --host=127.0.0.1 --port=3306 --user=root --password=toor
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o i:P:u:p:h --long ip:,port:,user:,password:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0
    # CATALINA_HOME='/opt/apache-tomcat-8.5.35'
    mysql_host="127.0.0.1"
    mysql_port="3306"
    mysql_user="root"
    mysql_password="toor"

    while true
    do
      case "$1" in
      -i|--ip)
          mysql_host="$2"
          shift
          ;;
      -P|--port)
          mysql_port="$2"
          shift
          ;;
      -u|--user)
          mysql_user="$2"
          shift
          ;;
      -p|--password)
          mysql_password="$2"
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
    xml_file_name="/tmp/${ipaddr}_mysql_info.xml"
}

main(){
    main_pre $@
    createReportXml
        getHostInfo
        createChecklist
            createSection "checkMysqlRunner"
                checkMysqlRunner
            closeSection
            createSection "checkMysqlMaxConnections"
                checkMysqlMaxConnections
            closeSection
            createSection "checkMysqlNullTestAccount"
                checkMysqlNullTestAccount
            closeSection
            createSection "checkMysqlNoPassword"
                checkMysqlNoPassword
            closeSection
            createSection "checkMysqlAccount"
                checkMysqlAccount
            closeSection
            createSection "checkMysqlLog"
                checkMysqlLog
            closeSection
            createSection "checkMysqlVersion"
                checkMysqlVersion
            closeSection
        closeChecklist
    closeReportXml
}

main $@