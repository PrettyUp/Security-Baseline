#!/bin/bash
xml_file_name='/tmp/192.168.220.143_nginx_fix.log'
CATALINA_HOME='/usr/local/nginx'
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
    echo -e "<fix_time>$(date  +'%Y-%m-%d 星期%w %H:%M:%S')</fix_time>" >> $xml_file_name
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
    cat $file_name | while read line
    do
        result=`echo $line | grep -E $regexp`
        if [ -n "$result" ]
        then
            echo "$result"
            break
        fi
    done
    echo "not found"
}
            
fixNginxUserAgent(){
    fix_object="/usr/local/nginx/conf/nginx.conf"
    fix_comment="查看user-agent中否配置正确"
    fix_command="cd $CATALINA_HOME/conf;sed -i -r '/^\s*location[^{]*\{/a\            if (\$http_user_agent ~* \"java\|3_parse\|perl\|ruby\|curl\|bash\|echo\|uname\|base64\|decode\|md5sum\|select\|concat\|httprequest\|httpclient\|nmap\|scan\" ) \{\n                    return 403;\n            \}' nginx.conf; "
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixErrorLog(){
    fix_object="/usr/local/nginx/conf/nginx.conf"
    fix_comment="检查访问日志是否开启"
    fix_command="cd $CATALINA_HOME/conf; sed -i '/^\s*http\s*{/a\    access_log  logs/access.log  main;' nginx.conf; "
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
usage(){
  echo "
Usage:
  -d, --basedir     mysql security config path to save, default /usr/local/nginx
  -h, --help        display this help and exit

  example1: bash tomcat_baseline_fix.sh -d/usr/local/nginx
  example2: bash tomcat_baseline_fix.sh --basedir=/usr/local/nginx
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o d:h --long basedir:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0
    CATALINA_HOME='/usr/local/nginx'

    while true
    do
      case "$1" in
      -d|--basedir)
          CATALINA_HOME="$2"
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
    xml_file_name="/tmp/${ipaddr}_nginx_fix.log"
}
main(){
    main_pre $@
    createReportXml
		fixNginxUserAgent
		fixErrorLog
	closeReportXml
}

main $@
