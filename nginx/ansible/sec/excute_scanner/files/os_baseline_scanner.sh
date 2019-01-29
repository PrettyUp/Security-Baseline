ipaddr=`ifconfig|grep 'inet'|grep -v '127.0.0.1'|awk '{print $2}'|cut -d':' -f 2`
xml_file_name="/tmp/${ipaddr}_os_info.xml"
id=0

createReportXml(){
    echo '<root>' > $xml_file_name
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

# 1.2.2.1 多余功能和软件安全
# a、禁止任何现网运行的机器上安装有开发工具，包括编译器，调试器，开发库等。---未实现
checkDevelopTool(){
    array_tool[0]="gcc"
    array_tool[1]="gdb"
    for tool in ${array_tool[@]}
    do
        command="which $tool"
        comment="检测$tool是否存在"
        result=`which $tool`
        appendToXml "$tool" "$command" "$comment" "$result"
    done
}

# b、如果不使用，卸载下列高危软件
# 只负责使用dpkg -l查询，登规判断放到解析器去处理
checkUnnecessarySoftware(){
    array_software[0]="pump"
    array_software[1]="apmd"
    array_software[2]="lsapnptools"
    array_software[3]="redhat-logos"
    array_software[4]="mt-st"
    array_software[5]="kernel-pcmcia-cs"
    array_software[6]="Setserial"
    array_software[7]="redhat-relese"
    array_software[8]="eject"
    array_software[9]="linuxconf"
    array_software[10]="kudzu"
    array_software[11]="gd"
    array_software[12]="bc"
    array_software[13]="getty_ps"
    array_software[14]="raidtools"
    array_software[15]="pciutils"
    array_software[16]="mailcap"
    array_software[17]="setconsole"
    array_software[18]="gnupg"
    array_software[19]="nc"
    for software in ${array_software[@]}
    do
        command="ps -ef | grep $software |grep -v grep"
        comment="check if $software have been installed"
        result=`ps -ef | grep -E "\s+$software\s+" | grep -v grep`
        appendToXml "$software" "$command" "$comment" "$result"
    done
}



# 1.2.2.2 用户账号安全
# a) 密码安全策略
# 口令长度限制
checkPasswdLengthLimit(){
    password_config_file='/etc/login.defs'
    passwd_length_reg='^\s*PASS_MIN_LEN\s*[0-9]+\s*'
    comment='检测是否设置口令长度限制'
    result=$(searchValueByReg "$password_config_file" "$passwd_length_reg")
    appendToXml "$password_config_file" "$passwd_length_reg" "$comment" "$result"
}
# 限制三类字符
checkPasswdComplexLimit(){
    password_config_file='/etc/pam.d/common-password'
    passwd_complex_reg='^\s*password\s+requisite\s+pam_cracklib\.so.*'
    comment='检测是否设置口令复杂度限制'
    result=$(searchValueByReg "$password_config_file" "$passwd_complex_reg")
    appendToXml "$password_config_file" "$passwd_complex_reg" "$comment" "$result"
}

# b) 口令必须有过期日期
checkPasswdDateLimit(){
    password_config_file='/etc/login.defs'
    password_expires_reg='^\s*PASS_MAX_DAYS\s*[0-9]{,3}\s*$'
    comment='检测是否设置口令有效期限制'
    result=$(searchValueByReg "$password_config_file" "$password_expires_reg")
    appendToXml "$password_config_file" "$password_expires_reg" "$comment" "$result"
}

# c) 检查密码是否安全 -- 未实现
# hydra

# d) Password Shadowing
checkShadowPermit(){
    shadow_file='/etc/shadow'
    command="ls -l $shadow_file"
    comment='check if /etc/shadow permit'
    result=`ls -l $shadow_file`
    appendToXml "$shadow_file" "$command" "$comment" "$result"
}
# /etc/passwd第二位为x
# /etc/passwd 用户与/etc/shadow一致，由下g)实现

# e) 管理密码 ---- 未实现，和b)有什么区别

# f)  只允许特定用户使用su命令成为root ---- 这里理解成限制只允许wheel组用户su
checkSuLimit(){
    su_config_file='/etc/pam.d/su'
    limit_wheel_reg='^\s*auth\s+required\s+pam_wheel.so\s+[^d]*'
    comment='check if limit only wheel can su'
    result=$(searchValueByReg "$su_config_file" "$limit_wheel_reg")
    appendToXml "$su_config_file" "$limit_wheel_reg" "$comment" "$result"
}

# g) 清除一切不使用的账户 ---- 不好判断哪些用户是没用的，只能先获取用户列表
readPasswdContent(){
    passwd_file='/etc/passwd'
    command="cat $passwd_file"
    result=`cat /etc/passwd`
    appendToXml "$passwd_file" "$command" "$comment" "$result"
}

readShadowContent(){
    passwd_file='/etc/shadow'
    command="cat $passwd_file"
    result=`cat /etc/shadow`
    appendToXml "$passwd_file" "$command" "$comment" "$result"
}

# 1.2.2.3 网络服务器安全
# 服务过滤Filtering
checkDangerService(){
    service_list[0]='echo'
    service_list[1]='systat'
    service_list[2]='netstat'
    service_list[3]='bootp'
    service_list[4]='tftp'
    service_list[5]='link'
    service_list[6]='supdup'
    service_list[7]='sunrpc'
    service_list[8]='news'
    service_list[9]='snmp'
    service_list[10]='xdmcp'
    service_list[11]='exec'
    service_list[12]='login'
    service_list[13]='shell'
    service_list[14]='printer'
    service_list[15]='biff'
    service_list[16]='who'
    service_list[17]='syslog'
    service_list[18]='uccp'
    service_list[19]='route'
    service_list[20]='openwin'
    service_list[21]='nfs'
    service_list[22]='x11'
    # udp服务
    service_list[23]='rpc.ypupdated'
    service_list[24]='rpcbind'
    service_list[25]='rpc.cmsd'
    service_list[26]='rpc.statd'
    service_list[27]='rpc.ttdbserver'
    service_list[28]='sadmind'
    # R服务
    service_list[29]='rtvsd'
    # tftpd
    service_list[30]='tftpd'
    # uccp
    service_list[31]='uccp'
    for service in ${service_list[*]}
    do
        command="systemctl status $service"
        comment="check if service $service have been setup"
        result=`systemctl status $service`
        appendToXml "$service" "$command" "$comment" "$result"
    done
}

# /etc/inetd.conf文件权限 ---- 不需要的服务未实现
checkInetdPermit(){
    config_file_name1='/etc/inetd.conf'
    config_file_name2='/etc/xinetd.conf'
    comment="check inetd config file permit"
    if [ -e $config_file_name1 ]
    then
        config_file_name=$config_file_name1
        command="ls -l $config_file_name"
        result=`ls -l $config_file_name`
    elif [ -e $config_file_name2 ]
    then
        config_file_name=$config_file_name2
        command="ls -l $config_file_name"
        result=`ls -l $config_file_name`
    else
        config_file_name='/etc/inetd.conf'
        command='none'
        result='inetd not installed'
    fi
    appendToXml "$config_file_name" "$command" "$comment" "$result"
}

# R 服务----关闭R服务未实现，不知道怎么操作

# Tcp_wrapper----未实现，不太明白具体该做什么

# /etc/hosts.equiv----未实现，不太明白具体该怎么做

# /etc/services权限配置
checkServicesPermit(){
    file_name='/etc/services'
    command='ls -l $file_name'
    comment='check /etc/services owner and permit'
    result=`ls -l $file_name`
    appendToXml "$file_name" "$command" "$comment" "$result"
}

# /etc/aliases ---- 当前没有这个文件注释不懂具体怎么样的
checkAliasesPermit(){
    file_name="/etc/aliases"
    command="ls -l $file_name"
    comment="check /etc/aliases owner and permit"
    result='file not found'
    if [ -e $file_name ]
    then
        result=`ls -l $file_name`
    fi
    appendToXml "$file_name" "$command" "$comment" "$result"
}

# NFS ---- 不太懂具体实现

# Trivial ftp (tftp) ---- 这个直接放前面实现 以下软件不允许启动
checkServiceProcess(){
    array_process[0]="tftp"
    array_process[1]="sendmail"
    array_process[2]="finger"
    array_process[3]="uccp"
    array_process[4]="ftp"
    
    for process in ${array_process[*]}
    do
        command="ps -ef |grep $process | grep -v grep"
        comment="检测$process服务进程是否启动"
        result=`ps -ef |grep -E "\s+$process\s+" | grep -v grep`
        appendToXml "$process" "$command" "$comment" "$result"
    done
}

# Sendmail ---- 不太懂具体实现

# finger ---- 这个直接放前面实现

# uucp ---- 不太懂具体实现

# ftp ---- 另找时间实现

# 1.2.2.4 系统设置安全
# 限制控制台的使用
checkConsoleAppsExists(){
    dir_name='/etc/security/console.apps'
    command='ls -l $dir_name'
    comment='check if /etc/security/console.apps dir exist any services'
    if [ -e $dir_name ]
    then
        result=`ls -l $dir_name`
    else
        result="$dir_name: No such file or directory"
    fi
    appendToXml "$dir_name" "$command" "$comment" "$result"
}
# 关闭ping
checkPingClose(){
    config_file_name=' /proc/sys/net/ipv4/icmp_echo_ignore_all'
    command='cat $config_file_name'
    comment='check if ping have been closed'
    result=`cat $config_file_name`
    appendToXml "$config_file_name" "$command" "$comment" "$result"
}
# telnet信息处理

# /etc/securetty
# tty\d+
checkTtyStatus(){
    tty_file="/etc/securetty"
    tty_reg="tty[0-9]+"
    command="cat /etc/securetty|grep -Ev ^#|grep -Ev ^$ | grep -Ev $tty_reg"
    comment="check if other tty"
    result=`cat /etc/securetty|grep -Ev ^#|grep -Ev ^$ | grep -Ev $tty_reg`
    appendToXml "$tty_file" "$command" "$comment" "$result"
}

# /etc/host.conf
# 必须要有nospoof on
checkHostConf(){
    file_name="/etc/host.conf"
    regexp="^\s*nospoof\s+on\s*"
    comment="check /etc/host.conf"
    result=$(searchValueByReg $file_name $regexp)
    appendToXml "$file_name" "$regexp" "$comment" "$result"
}

# 禁止IP源路径路由
checkDisableSourceRoute(){
    for file in /proc/sys/net/ipv4/conf/*/accept_source_route
    do
        command="cat $file"
        comment="check if $file source route have been closed or not"
        result=`cat $file`
        appendToXml "$file" "$command" "$comment" "$result"
    done
}

# 资源限制，值有待商榷
# 查询core、rss、nproc

# TCP SYN Cookie
checkSynCookie(){
    file_name="/proc/sys/net/ipv4/tcp_syncookies"
    command="cat $file_name"
    comment="检测SYN Cookie是否开启"
    result=`cat $file_name`
    appendToXml "$file_name" "$command" "$comment" "$result"
}


# LILO安全

# Control-Alt-Delete 键盘关机命令
checkCtrlAltDelDisable(){
    file_name='/etc/init/control-alt-delete.conf'
    regexp='^\s*start\s+on\s+control-alt-delete\s*$'
    comment='check if Control-Alt-Delete have been enabled'
    result=$(searchValueByReg "$file_name" "$regexp")
    appendToXml "$file_name" "$regexp" "$comment" "$result"
}
# 日志系统安全

#dir_name='/etc/init.d/'
#result=`ls -l $dir_name`

# 修正脚本文件在“/etc/rc.d/init.d”目录下的权限

# 1.2.2.5 文件系统安全

# （查出）去掉不必要的suid程序，可以通过脚本查看
checkSuidFile(){
    obj="suid"
    command="find / -type f -perm -04000 -o -perm -02000 -exec ls -lg {} \;"
    comment="检测suid文件"
    result=`find / -type f -perm -04000 -o -perm -02000 -exec ls -ldb {} \;|grep -Ev "Permission\s*denied"|grep -Ev "No\s*such"`
    appendToXml "$obj" "$command" "$comment" "$result"
}

# 控制mount上的文件系统
# 列出没有nosuid,nodev,noexec的文件系统

# 备份与恢复

main(){
    createReportXml
        getHostInfo
        createChecklist
            createSection "UnnecessarySoftware"
                createNode "UnnecessaryDevTool"
                    checkDevelopTool
                closeNode
                createNode "UnnecessarySoftware"
                    checkUnnecessarySoftware
                closeNode
            closeSection
            createSection "AccountLimit"
                createNode "PasswdLengthLimit"
                    checkPasswdLengthLimit
                closeNode
                createNode "PasswdComplexLimit"
                    checkPasswdComplexLimit
                closeNode
                createNode "PasswdDateLimit"
                    checkPasswdDateLimit
                closeNode
                createNode "SuLimit"
                    checkSuLimit
                closeNode
                createNode "PasswdContent"
                    readPasswdContent
                closeNode
                createNode "ShadowContent"
                    readShadowContent
                closeNode
            closeSection
            createSection "ServiceSecurity"
                createNode "DangerService"
                    checkDangerService
                closeNode
                createNode "InetdPermit"
                    checkInetdPermit
                closeNode
                createNode "ServicesPermit"
                    checkServicesPermit
                closeNode
                createNode "ServicesProcess"
                    checkServiceProcess
                closeNode
            closeSection
            createSection "SystemSettingSecurity"
                createNode "ConsoleAppsExists"
                    checkConsoleAppsExists
                closeNode
                createNode "PingClose"
                    checkPingClose
                closeNode
                createNode "TtyStatus"
                    checkTtyStatus
                closeNode
                createNode "HostConf"
                    checkHostConf
                closeNode
                createNode "DisableSourceRoute"
                    checkDisableSourceRoute
                closeNode
                createNode "SynCookie"
                    checkSynCookie
                closeNode
                createNode "CtrlAltDelDisable"
                    checkCtrlAltDelDisable
                closeNode
            closeSection
            createSection "FileSystemSecurity"
                createNode "FindSuidFile"
                    checkSuidFile
                closeNode
            closeSection
        closeChecklist
    closeReportXml
}

main