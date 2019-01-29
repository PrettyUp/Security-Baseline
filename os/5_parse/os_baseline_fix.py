import os
import re
import sys
sys.path.append('../../')
from common.baseline_fix import GenFixScript


class GenOSFixScript(GenFixScript):
    def __init__(self,ip_addr):
        baseline_type = "OS"
        super().__init__(ip_addr,baseline_type)

    def gen_shell_script_uninstall_unnecessary_develop_tool(self,fix_object,fix_comment,check_result):
        check_result_list = check_result[0].split("、")
        fix_command = ""
        for tool in check_result_list:
            fix_command += f"apt-get remove {tool} -y;"
        self.shell_script_obj.writelines("""
fixUnnecessaryDevelopTool(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_commgen_shell_script_disable_console_appsand" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_uninstall_unnecessary_software(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split("、")
        fix_command = ""
        for software in check_result_list:
            fix_command += f"apt-get remove {software} -y;"
        self.shell_script_obj.writelines("""
fixUnnecessarySoftware(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_add_password_length_limit(self, fix_object, fix_comment, check_result):
        fix_command = "echo 'PASS_MIN_LEN 8' >> /etc/login.defs"
        self.shell_script_obj.writelines("""
fixPasswordLengthLimit(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_add_password_complex_limit(self, fix_object, fix_comment, check_result):
        # check_result_list = check_result[0].split()
        fix_command = f"echo '# add by security' >> /etc/pam.d/common-password;"
        fix_command += f"echo 'password requisite pam_cracklib.so retry=5 difok=3 minlen=8' >> /etc/pam.d/common-password;"
        self.shell_script_obj.writelines("""
fixPasswordComplexLimit(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_add_password_date_limit(self, fix_object, fix_comment, check_result):
        fix_command = f"sed -i 's/^\s*PASS_MAX_DAYS/#PASS_MAX_DAYS/g' /etc/login.defs;"
        fix_command += f"echo 'PASS_MAX_DAYS 365' >> /etc/login.defs;"
        self.shell_script_obj.writelines("""
fixPasswordDateLimit(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_add_su_limit(self, fix_object, fix_comment, check_result):
        fix_command = f"echo 'add by security' >> /etc/pam.d/su;"
        fix_command += f"echo 'auth       required   pam_wheel.so' >> /etc/pam.d/su;"
        self.shell_script_obj.writelines("""
fixSuLimit(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_filter_network_service(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split("、")
        fix_command = ""
        for service in check_result_list:
            fix_command += f"systemctl stop {service} ;"
        self.shell_script_obj.writelines("""
fixFilterNetworkService(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_etc_inetd_conf(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"chown root:root {check_result_list[-1]};"
        fix_command += f"chmod 600 {check_result_list[-1]};"
        self.shell_script_obj.writelines("""
fixEtcInetdConf(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_etc_services(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"chown root:root {check_result_list[-1]};"
        fix_command += f"chmod 600 {check_result_list[-1]};"
        self.shell_script_obj.writelines("""
fixEtcServices(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_close_danger_process(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split("、")
        fix_command = ""
        for process in check_result_list:
            fix_command += f"kill -9 `ps -ef | grep {process} | grep -v grep|cut -f 1`;"
        self.shell_script_obj.writelines("""
fixEtcServices(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_disable_console_apps(self, fix_object, fix_comment, check_result):
        pass

    def gen_shell_script_close_ping(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all;"
        fix_command += f"echo 'net.ipv4.icmp_echo_ignore_all = 1' >> /etc/sysctl.conf;"
        self.shell_script_obj.writelines("""
fixClosePing(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_enable_no_spoof(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"echo '# add by security' >> /etc/host.conf;"
        fix_command += f"echo 'nospoof on' >> /etc/host.conf;"
        self.shell_script_obj.writelines("""
fixNoSpoof(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_disable_source_route(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"for f in /proc/sys/net/ipv4/conf/*/accept_source_route; do echo 0 > $f; done"
        self.shell_script_obj.writelines("""
fixDisableSourceRoute(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command='""" + fix_command + """'
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_enable_syn_cookie(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"echo 1 > /proc/sys/net/ipv4/tcp_syncookies;"
        fix_command += f"echo 'net.ipv4.tcp_syncookies = 1' >> /etc/sysctl.conf;"
        self.shell_script_obj.writelines("""
fixSynCookie(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script_disable_ctrl_alt_delete(self, fix_object, fix_comment, check_result):
        check_result_list = check_result[0].split()
        fix_command = f"sed -i -r 's/^\s*start\s+on\s+control-alt-delete\s*$/#start on control-alt-delete/' /etc/init/control-alt-delete.conf;"
        # fix_command += f"chmod 600 {check_result_list[-1]};"
        self.shell_script_obj.writelines("""
fixCtrlAltDelete(){
    fix_object=\"""" + fix_object + """\"
    fix_comment=\"""" + fix_comment + """\"
    fix_command=\"""" + fix_command + """\"
    fix_result=`eval $fix_command`
    appendToXml "$fix_object" "$fix_command" "$fix_comment" "$fix_result"
}
                """)

    def gen_shell_script(self):
        need_fix_item = self.html_obj.html.xpath("//div[@class = 'card-header bg-danger text-white']/..")
        # need_fix_item = self.html_obj.html.xpath("//div[contains(@class, 'card-header')]/..")
        # all_need_fix_items = all_item_div.xpath("//div[@class='card-header bg-danger text-white']/..")
        # gg=self.soup.find_all(id="accordion2")
        for item in need_fix_item:
            check_title = item.xpath("div//a/text()")[0]
            check_object = item.xpath("div//table/tr[1]/td/text()")
            if len(check_object) == 0:
                check_object = ""
            else:
                check_object = check_object[0]
            check_command = item.xpath("div//table/tr[2]/td/text()")[0]
            check_comment = item.xpath("div//table/tr[3]/td/text()")[0]
            check_result = item.xpath("div//table/tr[4]/td/text()")
            if check_title == "禁止任何现网运行的机器上安装有开发工具，包括编译器，调试器，开发库等":
                check_result = [check_object]
                self.gen_shell_script_uninstall_unnecessary_develop_tool(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_uninstall_unnecessary_develop_tool"] = "fixUnnecessaryDevelopTool"
                continue
            elif check_title == "如果不使用，卸载下列高危软件":
                self.gen_shell_script_uninstall_unnecessary_software(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_uninstall_unnecessary_software"] = "fixUnnecessarySoftware"
                continue
            elif check_title == "口令长度限制":
                self.gen_shell_script_add_password_length_limit(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_add_password_length_limit"] = "fixPasswordLengthLimit"
                continue
            elif check_title == "口令复杂度限制":
                self.gen_shell_script_add_password_complex_limit(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_add_complex_length_limit"] = "fixPasswordComplexLimit"
                continue
            elif check_title == "口令日期限制":
                self.gen_shell_script_add_password_date_limit(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_add_date_length_limit"] = "fixPasswordDateLimit"
                continue
            elif check_title == "只允许wheel组su":
                self.gen_shell_script_add_su_limit(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_add_su_limit"] = "fixSuLimit"
                continue
            elif check_title == "服务过滤Filtering":
                check_result = [check_object]
                self.gen_shell_script_filter_network_service(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_filter_network_service"] = "fixFilterNetworkService"
                continue
            elif check_title == "/etc/inetd.conf":
                self.gen_shell_script_etc_inetd_conf(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_etc_inetd_conf"] = "fixEtcInetdConf"
                continue
            elif check_title == "/etc/services":
                self.gen_shell_script_etc_services(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_remove_server_number"] = "fixEtcServices"
                continue
            elif check_title == "关闭危险服务进程":
                self.gen_shell_script_close_danger_process(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_close_danger_process"] = "fixCloseDangerProcess"
                continue
            elif check_title == "限制控制台的使用":
                self.gen_shell_script_disable_console_apps(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_change_default_port"] = "fixDefaultPort"
                continue
            elif check_title == "系统关闭Ping":
                self.gen_shell_script_close_ping(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_close_ping"] = "fixClosePing"
                continue
            elif check_title == "检测IP欺骗":
                self.gen_shell_script_enable_no_spoof(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_enable_no_spoof"] = "fixNoSpoof"
                continue
            elif check_title == "禁用源路由":
                self.gen_shell_script_disable_source_route(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_disable_source_route"] = "fixDisableSourceRoute"
                continue
            elif check_title == "启用Syn Cookie":
                self.gen_shell_script_enable_syn_cookie(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_enable_syn_cookie"] = "fixSynCookie"
                continue
            elif check_title == "Control-Alt-Delete 键盘关机命令":
                self.gen_shell_script_disable_ctrl_alt_delete(check_object, check_comment, check_result)
                self.fix_item_list["gen_shell_script_disable_ctrl_alt_delete"] = "fixCtrlAltDelete"
        pass



if __name__ == "__main__":
    ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
    full_reg = f"{ip_reg}_os_report\.html"
    pwd_file_list = os.listdir("../4_report")
    for file in pwd_file_list:
        if re.search(full_reg, file):
            ip_addr = re.search(ip_reg, file).group()
            obj = GenOSFixScript(ip_addr)
            obj.gen_shell_script()