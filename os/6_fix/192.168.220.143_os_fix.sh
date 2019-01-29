#!/bin/bash
xml_file_name='/tmp/192.168.220.143_os_fix.log'
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
            
fixUnnecessaryDevelopTool(){
    fix_object="gcc、gdb"
    fix_comment="检测编译、调试工具是否存在"
    fix_command="apt-get remove gcc -y;apt-get remove gdb -y;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_commgen_shell_script_disable_console_appsand" "$fix_comment" "$fix_result"
}
                
fixFilterNetworkService(){
    fix_object="syslog"
    fix_comment="检测危险服务是否启动"
    fix_command="systemctl stop syslog ;"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                
main(){
    createReportXml
		fixUnnecessaryDevelopTool
		fixFilterNetworkService
	closeReportXml
}

main
