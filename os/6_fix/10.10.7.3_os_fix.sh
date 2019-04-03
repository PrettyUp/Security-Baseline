#!/bin/bash
xml_file_name='/tmp/10.10.7.3_os_fix.log'
CATALINA_HOME='/opt/apache-tomcat-8.5.35'
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
            
fixUnnecessaryDevelopTool(){
    fix_object="gcc、gdb"
    fix_comment="检测编译、调试工具是否存在"
    fix_command="apt-get remove gcc -y;apt-get remove gdb -y;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixUnnecessarySoftware(){
    fix_object="pump、apmd、lsapnptools、redhat-logos、mt-st、kernel-pcmcia-cs、Setserial、redhat-relese、eject、linuxconf、kudzu、gd、bc、getty_ps、raidtools、pciutils、mailcap、setconsole、gnupg、nc"
    fix_comment=""
    fix_command="apt-get remove p -y;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixPasswordLengthLimit(){
    fix_object="/etc/login.defs"
    fix_comment="检测是否设置口令长度限制"
    fix_command="echo 'PASS_MIN_LEN 8' >> /etc/login.defs"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixPasswordComplexLimit(){
    fix_object="/etc/pam.d/common-password"
    fix_comment="检测是否设置口令复杂度限制"
    fix_command="echo '# add by security' >> /etc/pam.d/common-password;echo 'password requisite pam_cracklib.so retry=5 difok=3 minlen=8' >> /etc/pam.d/common-password;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixPasswordDateLimit(){
    fix_object="/etc/login.defs"
    fix_comment="检测是否设置口令有效期限制"
    fix_command="sed -i 's/^\s*PASS_MAX_DAYS/#PASS_MAX_DAYS/g' /etc/login.defs;echo 'PASS_MAX_DAYS 365' >> /etc/login.defs;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixFilterNetworkService(){
    fix_object="syslog"
    fix_comment="检测危险服务是否启动"
    fix_command="systemctl stop syslog ;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixEtcServices(){
    fix_object="/etc/services"
    fix_comment="check /etc/services owner and permit"
    fix_command="chown root:root -;chmod 600 -;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixEtcServices(){
    fix_object="tftp、sendmail、finger、uccp、ftp"
    fix_comment="检测ftp服务进程是否启动"
    fix_command="kill -9 `ps -ef | grep t | grep -v grep|cut -f 1`;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixClosePing(){
    fix_object="/proc/sys/net/ipv4/icmp_echo_ignore_all"
    fix_comment="check if ping have been closed"
    fix_command="echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all;echo 'net.ipv4.icmp_echo_ignore_all = 1' >> /etc/sysctl.conf;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixNoSpoof(){
    fix_object="/etc/host.conf"
    fix_comment="check /etc/host.conf"
    fix_command="echo '# add by security' >> /etc/host.conf;echo 'nospoof on' >> /etc/host.conf;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
fixDisableSourceRoute(){
    fix_object="/proc/sys/net/ipv4/conf/default/accept_source_route
/proc/sys/net/ipv4/conf/ens160/accept_source_route
/proc/sys/net/ipv4/conf/lo/accept_source_route"
    fix_comment="check if /proc/sys/net/ipv4/conf/lo/accept_source_route source route have been closed or not"
    fix_command='for f in /proc/sys/net/ipv4/conf/*/accept_source_route; do echo 0 > $f; done'
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
usage(){
  echo "
Usage:
  -h, --help        display this help and exit

  example(need root right): bash os_baseline_fix.sh
"
}

main_pre(){
    # set -- $(getopt i:p:h "$@")
    set -- $(getopt -o h --long help -- "$@")
    ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
    id=0

    while true
    do
      case "$1" in
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
    xml_file_name="/tmp/${ipaddr}_os_fix.log"
}
main(){
    main_pre $@
    createReportXml
		fixUnnecessaryDevelopTool
		fixUnnecessarySoftware
		fixPasswordLengthLimit
		fixPasswordComplexLimit
		fixPasswordDateLimit
		fixFilterNetworkService
		fixEtcServices
		fixCloseDangerProcess
		fixClosePing
		fixNoSpoof
		fixDisableSourceRoute
	closeReportXml
}

main $@
