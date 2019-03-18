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

# 删除示例文档
checkExampleDoc(){
    dir_name="$CATALINA_HOME/webapps/"
    check_command='ls -l $dir_name | grep -E "\s+docs$|\s+examples$|\s+host-manager$|\s+manager$|\s+ROOT$"'
    check_comment="删除示例文档"
    if [ -e $dir_name ]
    then
        check_result=`ls -l $dir_name | grep -E "\s+docs$|\s+examples$|\s+host-manager$|\s+manager$|\s+ROOT$"`
    else
        check_result=""
    fi
    appendToXml "$dir_name" "$check_command" "$check_comment" "$check_result"
}

# 禁用tomcat默认帐号
# cat tomcat-users.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<user username=.*>/p'
checkDefaultAccount(){
    file_name="$CATALINA_HOME/conf/tomcat-users.xml"
    # 第一行是<?xml version="1.0" encoding="UTF-8"?>需要去掉
    check_command="cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/user username=.*/p'"
    check_comment="禁用tomcat默认帐号"
    if [ -e $file_name ]
    then
        check_result=`cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<user username=.*>/p'|sed -r 's/"+</"/'`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 禁止列目录
# cat web.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<welcome-file-list/,/welcome-file-list>/p'
# cat web.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<init-param>/,/init-param>/p'
checkListDir(){
    file_name="$CATALINA_HOME/conf/web.xml"
    check_command="cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/init-param/,/init-param>/p'"
    check_comment="禁止列目录"
    if [ -e $file_name ]
    then
        check_result=`cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<init-param>/,/init-param>/p'`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 自定义错误页面
# cat web.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<error-page>/,/error-page>/p'
checkErrorPage(){
    file_name="$CATALINA_HOME/conf/web.xml"
    check_command="cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/error-page/,/error-page>/p'"
    check_comment="自定义错误页面"
    if [ -e $file_name ]
    then
        check_result=`cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<error-page>/,/error-page>/p'`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 开启访问日志
# cat server.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|sed -n '/<Valve className="org.apache.catalina.valves.AccessLogValve"/'p
# cat server.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '<Valve className="org.apache.catalina.valves.AccessLogValve"'
checkEnableAccessLog(){
    file_name="$CATALINA_HOME/conf/server.xml"
    check_command="cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E 'Valve className=\"org.apache.catalina.valves.AccessLogValve\"'"
    check_comment="开启访问日志"
    if [ -e $file_name ]
    then
        check_result=`cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '<Valve className="org.apache.catalina.valves.AccessLogValve"'`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 隐藏版本号
# java -cp /opt/apache-tomcat-8.5.35/lib/catalina.jar org.apache.catalina.util.ServerInfo
checkServerVersion(){
    file_name="$CATALINA_HOME/bin/version.sh"
    check_command="bash $file_name"
    check_comment="隐藏版本号"
    if [ -e $file_name ]
    then
        check_result=`bash $file_name`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 修改默认监听端口
# cat server.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '^\s*<Connector port="8080"'
# cat server.xml |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '^\s*<Connector port="8443"'
checkDefaultPort(){
    file_name="$CATALINA_HOME/conf/server.xml"
    check_command="cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '^\s*Connector port="8080"'"
    check_comment="修改默认监听端口"
    if [ -e $file_name ]
    then
        check_result=`cat $file_name |sed '/<!--.*-->/d' | sed '/<!--/,/-->/d'|grep -A 3 -E '^\s*<Connector port="8080"'`
    else
        check_result=''
    fi
    appendToXml "$file_name" "$check_command" "$check_comment" "$check_result"
}

# 不以root/admin用户运行程序
# ps -ef |grep $CATALINA_HOME|grep -v grep
checkProcessRunner(){
    grep_flag="$CATALINA_HOME"
    check_command="ps -ef |grep $grep_flag|grep -v grep"
    check_comment="不以root/admin用户运行程序"
    check_result=`ps -ef |grep $grep_flag|grep -v grep`
    appendToXml "$grep_flag" "$check_command" "$check_comment" "$check_result"
}

usage(){
  echo "
Usage:
  -i, --ip	target machine ip
  -d, --dir	target software home dir
  -h, --help	display this help and exit

  example1: bash tomcat_baseline_scanner.sh
  example2: bash tomcat_baseline_scanner.sh -i ip_addr -dir home_dir
  example3: bash tomcat_baseline_scanner.sh --ip ip_addr --dir home_dir
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o i:d:h --long ip:,dir:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    CATALINA_HOME='/opt/apache-tomcat-8.5.35'
    id=0
    while true
    do
      case "$1" in
      -i|--ip)
          ipaddr="$2"
          shift
          ;;
      -d|--dir)
          CATALINA_HOME=="$2"
          shift
          ;;
      -h|--help)
          usage
          break
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
    xml_file_name="/tmp/${ipaddr}_tomcat_info.xml"
}

main(){
    main_pre $@
    createReportXml
        getHostInfo
        createChecklist
            createSection "checkExampleDoc"
                checkExampleDoc
            closeSection
            createSection "checkDefaultAccount"
                checkDefaultAccount
            closeSection
            createSection "checkListDir"
                checkListDir
            closeSection
            createSection "checkErrorPage"
                checkErrorPage
            closeSection
            createSection "checkEnableAccessLog"
                checkEnableAccessLog
            closeSection
            createSection "checkServerVersion"
                checkServerVersion
            closeSection
            createSection "checkDefaultPort"
                checkDefaultPort
            closeSection
            createSection "checkProcessRunner"
                checkProcessRunner
            closeSection
        closeChecklist
    closeReportXml
}

main $@