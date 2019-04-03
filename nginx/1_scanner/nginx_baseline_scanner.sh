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


#查看nginx的版本信息
checkNginxVersion(){
	check_command="nginx -V"	
	check_comment="查看nginx的版本信息"
	check_result=$(nginx -V 2>&1)
	appendToXml "System" "$check_command" "$check_comment" "$check_result"
}


#查看nginx是否隐藏版本号
checkNginxHiddenVersion(){
	config_file_name="$CATALINA_HOME/conf/nginx.conf"
	HiddenVersion_reg='^\s*server_tokens\s*off;'
	check_command="cat $config_file_name|grep -E $HiddenVersion_reg"
	check_comment="查看nginx是否隐藏版本号"
	result=`cat $config_file_name|grep -E $HiddenVersion_reg`
	if [ -z "$result" ]
	then
		result="not found"
	fi
	appendToXml "$config_file_name" "$check_command" "$check_comment" "$result"
}


#查看user-agent中否配置正确
checkNginxUserAgent(){
	config_file_name="$CATALINA_HOME/conf/nginx.conf"
	UserAgent_reg='^\s*if\s*\(\s*\$http_user_agent'
	check_command="cat $config_file_name|grep -A 3 -E $UserAgent_reg"
	check_comment="查看user-agent中否配置正确"
	result=`cat $config_file_name|grep -A 3 -E $UserAgent_reg`
	if [ -z "$result" ]
	then
		result="not found"
	fi
	appendToXml "$config_file_name" "$check_command" "$check_comment" "$result"
	
}

#检查访问日志是否开启
checkErrorLog(){
	config_file_name="$CATALINA_HOME/conf/nginx.conf"
	check_error_log='^\s*log_format\s*main'
	check_access_log='^\s*access_log\s*logs/access.log\s*main;'
	check_command="cat $config_file_name|grep -A 3 -E $check_error_log ； \n cat $config_file_name | grep -E $check_access_log"
	check_comment='检查访问日志是否开启'
	result1=`cat $config_file_name|grep -A 2 -E $check_error_log`
	if [ -z "$result1" ]
	then
		result1="error_log not found "
	fi
	result2=`cat $config_file_name | grep -E $check_access_log`
	if [ -z "$result2" ]
	then
		result2="access_log not found"
	fi
	appendToXml "$config_file_name" "$check_command" "$check_comment" "$result1 ;\n$result2"
}
#是否为特殊文件夹设置白名单IP
checkLocationIpWhiteList(){
	config_file_name="$CATALINA_HOME/conf/nginx.conf"
	check_command="cat $config_file_name | sed -n '/^\s*location[^{]*{/,/ }/'p"
	check_comment='是否为特殊文件夹设置白名单IP'
	result=`cat $config_file_name | sed -n '/^\s*location[^{]*{/,/ }/'p`
	if [ -z "$result" ]
	then
		result="Location not found"
	fi
	appendToXml "$config_file_name" "$check_command" "$check_comment" "$result"
}


#禁止访问没有默认页面文件夹时列出目录下所有文件
checkAutoindex(){
	config_file_name="$CATALINA_HOME/conf/nginx.conf"
	autoindex_reg='^\s*autoindex\s*on'
	check_command="cat $config_file_name | grep -E $autoindex_reg"
	check_comment='禁止访问没有默认页面文件夹时列出目录下所有文件'
	result=`cat $config_file_name | grep -E $autoindex_reg`

	if [ -z "$result" ]
	then
		result="Autoindex not found"
	fi

	appendToXml "$config_file_name" "$check_command" "$check_comment" "$result"

}

usage(){
  echo "
Usage:
  -d, --dir	target software home dir
  -h, --help	display this help and exit

  example1: bash tomcat_baseline_scanner.sh
  example2: bash tomcat_baseline_scanner.sh -d home_dir
  example3: bash tomcat_baseline_scanner.sh --dir home_dir
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o d:h --long dir:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    CATALINA_HOME='/usr/local/nginx'
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
    xml_file_name="/tmp/${ipaddr}_nginx_info.xml"
}

main(){
    main_pre $@
    createReportXml
        getHostInfo
        createChecklist
            createSection "checkNginxVersion"
                checkNginxVersion
            closeSection
            createSection "checkNginxHiddenVersion"
                checkNginxHiddenVersion
            closeSection
            createSection "checkNginxUserAgent"
                checkNginxUserAgent
            closeSection
            createSection "checkErrorLog"
                checkErrorLog
            closeSection
            createSection "checkLocationIpWhiteList"
                checkLocationIpWhiteList
            closeSection
            createSection "checkAutoindex"
                checkAutoindex
            closeSection
        closeChecklist
    closeReportXml
}

main $@






















