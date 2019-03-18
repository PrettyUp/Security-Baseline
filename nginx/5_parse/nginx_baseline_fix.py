import re
import os
import sys

from common.baseline_fix import GenFixScript


class GenNginxFixScript(GenFixScript):
    def __init__(self,argv,ip_addr):
        baseline_type = "nginx"
        base_dir ="/usr/local/nginx"
        super().__init__(argv,ip_addr,baseline_type,base_dir)

    def gen_shell_script_usage(self):
        self.shell_script_obj.writelines("""
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
}""")
    def gen_shell_script_Nginx_Version(self,fix_object,fix_comment,check_result):
        fix_command = "nginx -V;"

        self.shell_script_obj.writelines("""
fixNginxVersion(){
    fix_object=\""""+fix_object+"""\"
    fix_comment=\""""+fix_comment+"""\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
        """)

    def gen_shell_script_Nginx_Hidden_Version(self,fix_object,fix_comment,check_result):
        fix_command = "cd $CATALINA_HOME/conf; sed -i '/^\s*http\s*{/a\    server_tokens  off;' nginx.conf;"
        self.shell_script_obj.writelines("""
fixNginxHiddenVersion(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)


    def gen_shell_script_Nginx_User_Agent(self,fix_object,fix_comment,check_result):
        fix_command="cd $CATALINA_HOME/conf;"
        if "not found" in check_result[0] :
            fix_command += """sed -i -r '/^\s*location[^{]*\\{/a\            if (\\$http_user_agent ~* \\"java\\|3_parse\\|perl\\|ruby\\|curl\\|bash\\|echo\\|uname\\|base64\\|decode\\|md5sum\\|select\\|concat\\|httprequest\\|httpclient\\|nmap\\|scan\\" ) \{""" \
                           """\\n                    return 403;""" \
                            """\\n            \}' nginx.conf; """
        if "http_user_agent" in check_result[0] :
            fix_command += """sed -i 's/if (^\s*location[^{]*{\~\*.*/if (\\$http_user_agent ~* \\"java|3_parse|perl|ruby|curl|bash|echo|uname|base64|decode|md5sum|select|concat|httprequest|httpclient|nmap|scan\\" ) {/g' nginx.conf ;"""
        self.shell_script_obj.writelines("""
fixNginxUserAgent(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)


    def gen_shell_script_self_open_error_log(self,fix_object,fix_comment,check_result):
        fix_command = "cd $CATALINA_HOME/conf;"
        if "access_log not found" in check_result[0] :
            fix_command += " sed -i '/^\s*http\s*{/a\    access_log  logs/access.log  main;' nginx.conf; "

        if "error_log not found" in check_result[0] :
            if "access_log not found" in check_result[0]:
                fix_command += """sed -i -r \\"/^\s*http\s*\{/a\    log_format  main  \\'\\\\\$remote_addr - \\\\\$remote_user [\\\\\$time_local] \\\\\\"\\\\\$request\\\\\\" \\'""" \
                               """\\n                      \\'\\\\\$status \\\\\$body_bytes_sent \\\\\\"\\\\\$http_referer\\\\\\" \\'""" \
                               """\\n                      \\'\\\\\\"\\\\\$http_user_agent\\\\\\" \\\\\\"\\\\\$http_x_forwarded_for\\\\\\"\\';\\" nginx.conf; """
            else:
                fix_command += """sed -i -r \\"/^\s*access_log\s*logs/i\    log_format  main  \\'\\\\\$remote_addr - \\\\\$remote_user [\\\\\$time_local] \\\\\\"\\\\\$request\\\\\\" \\'""" \
                               """\\n                      \\'\\\\\$status \\\\\$body_bytes_sent \\\\\\"\\\\\$http_referer\\\\\\" \\'""" \
                               """\\n                      \\'\\\\\\"\\\\\$http_user_agent\\\\\\" \\\\\\"\\\\\$http_x_forwarded_for\\\\\\"\\';\\" nginx.conf; """

        self.shell_script_obj.writelines("""
fixErrorLog(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_location_ip_whitelist(self,fix_object,fix_comment,check_result):
         fix_command = "cd $CATALINA_HOME/conf;"
         self.shell_script_obj.writelines("""
fixLocationIpWhiteList(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command` 
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_remove_autoindex(self,fix_object,fix_comment,check_result):
        fix_command = "cd $CATALINA_HOME/conf; sed -i -e '/^\s*autoindex/d' nginx.conf;"

        self.shell_script_obj.writelines("""
fixRemoveAutoindex(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)


    def gen_shell_script_main_part(self):
        need_fix_item = self.html_obj.html.xpath("//div[@class = 'card-header bg-danger text-white']/..")
        # need_fix_item = self.html_obj.html.xpath("//div[contains(@class, 'card-header')]/..")
        # all_need_fix_items = all_item_div.xpath("//div[@class='card-header bg-danger text-white']/..")
        # gg=self.soup.find_all(id="accordion2")
        for item in need_fix_item:
            check_title = item.xpath("div//a/text()")[0]
            check_object = item.xpath("div//table/tr[1]/td/text()")[0]
            check_command = item.xpath("div//table/tr[2]/td/text()")[0]
            check_comment = item.xpath("div//table/tr[3]/td/text()")[0]
            check_result = item.xpath("div//table/tr[4]/td/text()")
            if check_title == "查看nginx版本信息":
                self.gen_shell_script_Nginx_Version(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_Nginx_Version"] = "fixNginxVersion"
                continue
            elif check_title == "查看nginx是否隐藏版本号":
                self.gen_shell_script_Nginx_Hidden_Version(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_Nginx_Hidden_Version"] = "fixNginxHiddenVersion"
                continue
            elif check_title == "查看user-agent中否配置正确":
                self.gen_shell_script_Nginx_User_Agent(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_Nginx_User_Agent"] = "fixNginxUserAgent"
                continue

            elif check_title == "是否开启errorlog和accesslog访问日志":
                self.gen_shell_script_self_open_error_log(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_self_define_error_page"] = "fixErrorLog"
                continue
            elif check_title == "是否为特殊文件夹设置白名单IP":
                self.gen_shell_script_location_ip_whitelist(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_location_ip_whitelist"] = "fixLocationIpWhiteList"
                continue
            elif check_title == "禁止访问没有默认页面文件夹时列出目录下所有文件":
                self.gen_shell_script_remove_autoindex(check_object,check_comment,check_result)
                self.fix_item_list["gen_shell_script_remove_autoindex"] = "fixRemoveAutoindex"
                continue
        pass

    def gen_shell_script(self):
        self.gen_shell_script_head_part()
        self.gen_shell_script_main_part()
        self.gen_shell_script_usage()
        self.gen_shell_script_tail_part()


if __name__ == "__main__":
    argv = sys.argv[1:]
    ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
    full_reg = f"{ip_reg}_nginx_report\.html"
    pwd_file_list = os.listdir("../4_report")
    for file in pwd_file_list:
        if re.search(full_reg, file):
            ip_addr = re.search(ip_reg, file).group()
            obj = GenNginxFixScript(argv,ip_addr)
            obj.gen_shell_script()