#!/bin/bash
xml_file_name='/tmp/192.168.220.143_mysql_fix.log'
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
            
fixMysqlNullTestAccount(){
    fix_object="select user,host,authentication_string from mysql.user where user = '' or user='test';"
    fix_comment="检测是否存在空账号或test账号"
    fix_command="mysql_command=\"delete from mysql.user where user = '' or user='test';FLUSH PRIVILEGES;\";mysql -h${mysql_ip} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"\${mysql_command}\""
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        
fixMysqlNoPassword(){
    fix_object="select user,host,authentication_string from mysql.user where length(authentication_string) = 0 or authentication_string is null;"
    fix_comment="检测是否存在密码为空的账号"
    fix_command="mysql_command=\"update mysql.user set authentication_string=PASSWORD('t*tsrch0st') where length(authentication_string) = 0 or authentication_string is null;FLUSH PRIVILEGES;\";mysql -h${mysql_ip} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \"\${mysql_command}\""
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        
usage(){
  echo "
Usage:
  -i, --ip          mysql service ip, default 127.0.0.1
  -P, --port        mysql service port, default 3306
  -u, --user	    mysql service user, default root
  -p, --password    mysql service user's password, default toor
  -d, --basedir     mysql security config path to save, default /etc/mysql/mysql.conf.d
  -h, --help        display this help and exit

  example1: bash mysql_baseline_fix.sh -i127.0.0.1 -P3306 -uroot -ptoor
  example2: bash mysql_baseline_fix.sh --ip=127.0.0.1 --port=3306 --user=root --password=toor
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o i:P:u:p:d:h --long ip:,port:,user:,password:,basedir:,help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0
    CATALINA_HOME='/etc/mysql/mysql.conf.d'
    mysql_host="127.0.0.1"
    mysql_port="3306"
    mysql_user="root"
    mysql_password="toor"

    while true
    do
      case "$1" in
      -i|--ip)
          mysql_ip="$2"
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
    xml_file_name="/tmp/${ipaddr}_mysql_fix.log"
}
main(){
    main_pre $@
    createReportXml
		fixMysqlNoPassword
	closeReportXml
}

main $@
