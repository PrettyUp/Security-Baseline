import getopt
import os
import re
import sys
sys.path.append('../../')
from common.baseline_fix import GenFixScript
from common.baseline_param_parse import BaselineParamParse


class GenMysqlFixScript(GenFixScript):
    def __init__(self,ip_addr):
        baseline_type = "Mysql"
        base_dir = "/etc/mysql/mysql.conf.d"
        super().__init__(ip_addr,baseline_type,base_dir)

    def gen_shell_script_usage(self):
        self.shell_script_obj.writelines("""
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
    mysql_ip="127.0.0.1"
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
}""")

    def gen_shell_script_change_mysql_runner(self,fix_object,fix_comment,check_result):
        fix_command = "cd $CATALINA_HOME;"
        fix_command += f"echo -e '[mysqld]\\nuser = mysql' > $CATALINA_HOME/mysql_runner.cnf && systemctl restart mysql"
        self.shell_script_obj.writelines("""
fixMysqlRunner(){
    fix_object=\""""+fix_object+"""\"
    fix_comment=\""""+fix_comment+"""\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        """)

    def gen_shell_script_config_max_connections(self, fix_object, fix_comment, check_result):
        fix_command = "cd $CATALINA_HOME;"
        fix_command += f"echo -e '[mysqld]\\nmax_connections = 1000' > $CATALINA_HOME/mysql_max_connections.cnf && systemctl restart mysql"
        self.shell_script_obj.writelines("""
fixMysqlMaxConnections(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        """)

    def gen_shell_script_delete_null_test_account(self, fix_object, fix_comment, check_result):
        fix_command = 'mysql_command=\\\"delete from mysql.user where user = \'\' or user=\'test\';FLUSH PRIVILEGES;\\\";'
        fix_command += "mysql -h${mysql_ip} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \\\"\${mysql_command}\\\""
        self.shell_script_obj.writelines("""
fixMysqlNullTestAccount(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        """)

    def gen_shell_script_correct_no_password(self, fix_object, fix_comment, check_result):
        fix_command = 'mysql_command=\\\"update mysql.user set authentication_string=PASSWORD(\'t*tsrch0st\') where length(authentication_string) = 0 or authentication_string is null;FLUSH PRIVILEGES;\\\";'
        fix_command += "mysql -h${mysql_ip} -P${mysql_port} -u${mysql_user} -p${mysql_password} -e \\\"\${mysql_command}\\\""
        self.shell_script_obj.writelines("""
fixMysqlNoPassword(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        """)


    def gen_shell_script_main_part(self):
        need_fix_item = self.node_xpath(self.html_obj.html, "//div[@class = 'card-header bg-danger text-white']/..")
        # need_fix_item = self.html_obj.html.xpath("//div[@class = 'card-header bg-danger text-white']/..")
        # need_fix_item = self.html_obj.html.xpath("//div[contains(@class, 'card-header')]/..")
        # all_need_fix_items = all_item_div.xpath("//div[@class='card-header bg-danger text-white']/..")
        # gg=self.soup.find_all(id="accordion2")
        for item in need_fix_item:
            check_title=self.text_xpath(item,"div//a")
            check_object=self.text_xpath(item,"div//table/tr[1]/td")
            check_command=self.text_xpath(item, "div//table/tr[2]/td")
            check_comment = self.text_xpath(item, "div//table/tr[3]/td")
            check_result = self.text_xpath(item, "div//table/tr[4]/td")
            if check_title == "禁止以root用户运行":
                self.gen_shell_script_change_mysql_runner(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_change_mysql_runner"] = "fixMysqlRunner"
                continue
            if check_title == "设置最大连接数限制":
                self.gen_shell_script_config_max_connections(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_config_max_connections"] = "fixMysqlMaxConnections"
                continue
            if check_title == "检测是否存在空账号或test账号":
                self.gen_shell_script_delete_null_test_account(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_change_mysql_runner"] = "fixMysqlNullTestAccount"
                continue
            if check_title == "检测是否存在密码为空的账号":
                self.gen_shell_script_correct_no_password(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_change_mysql_runner"] = "fixMysqlNoPassword"
                continue

    def gen_shell_script(self):
        self.gen_shell_script_head_part()
        self.gen_shell_script_main_part()
        self.gen_shell_script_usage()
        self.gen_shell_script_tail_part()



if __name__ == "__main__":
    bpp_obj = BaselineParamParse()
    model, ip = bpp_obj.param_parse(sys.argv[1:])
    # 如果指定ip模式
    if model == "ip":
        # 如果ip模式中未给出ip列出则报错退出
        if ip is None:
            bpp_obj.usage()
            sys.exit(1)
        else:
            ip_list = ip.split(",")
            for ip_addr in ip_list:
                # 如果指定的ip对应的文件并不存在则跳过
                if not os.path.exists(f"../4_report/{ip_addr}_mysql_report.html"):
                    print(f'sorry, file "../4_report/{ip_addr}_mysql_report.html" is not exist, it will be skip')
                    continue
                gen_fix_obj = GenMysqlFixScript(ip_addr)
                gen_fix_obj.gen_shell_script()
    # 如果指定文件夹模式
    elif model == "dir":
        argv = sys.argv[1:]
        ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
        full_reg = f"{ip_reg}_mysql_report\.html"
        pwd_file_list = os.listdir("../4_report")
        for file in pwd_file_list:
            if re.search(full_reg, file):
                ip_addr = re.search(ip_reg, file).group()
                gen_fix_obj = GenMysqlFixScript(ip_addr)
                gen_fix_obj.gen_shell_script()