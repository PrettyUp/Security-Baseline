import untangle
import re
from lxml import etree

class GenHtmlReport():
    def __init__(self):
        self.xml_obj = untangle.parse('os_report_xml.xml')
        ip_addr = self.xml_obj.root.hostinfo.ipaddr.__dict__['cdata']
        self.html_report_obj = open(f"{ip_addr}.html", "w+", encoding='utf-8')

    def gen_html_report_head(self):
        ip_addr = self.xml_obj.root.hostinfo.ipaddr.__dict__['cdata']
        self.html_report_obj.writelines("<html>\n")
        self.html_report_obj.writelines("<head>\n")
        self.html_report_obj.writelines(f"""<meta charset="utf-8" />\n""")
        self.html_report_obj.writelines(f"<title>{ip_addr}</title>\n")
        self.html_report_obj.writelines(f'<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css"></link>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/jquery-3.3.1.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/popper.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/bootstrap.min.js"></script>\n')
        self.html_report_obj.writelines("</head>\n")

    def gen_html_report_hostinfo_table(self):
        hostname = self.xml_obj.root.hostinfo.hostname.__dict__['cdata']
        ip_addr = self.xml_obj.root.hostinfo.ipaddr.__dict__['cdata']
        os_version = self.xml_obj.root.hostinfo.os_version.__dict__['cdata'].strip()
        kernel_version = self.xml_obj.root.hostinfo.kernel_version.__dict__['cdata'].strip()
        tcp_services = self.xml_obj.root.hostinfo.tcp_services.__dict__['cdata']
        udp_services = self.xml_obj.root.hostinfo.udp_services.__dict__['cdata']
        tcp_services_lines = tcp_services.split("\n")
        udp_services_lines = udp_services.split("\n")
        listen_addr_reg = "[\.|\d]+:\d+"
        process_reg = "\d+/\w+"

        tcp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg,line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg,line).group().split("/")[-1]
                    tcp_listen_process_str += f"{listen_addr}-{process}<br />"

        udp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg, line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg, line).group().split("/")[-1]
                    udp_listen_process_str += f"{listen_addr}-{process}<br />"
        self.html_report_obj.writelines("<body>\n")
        self.html_report_obj.writelines("""<table id="hostinfo" class="table">\n""")
        self.html_report_obj.writelines("""<tr><th colspan="4" style="text-align:center;">主机基本信息<th></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>主机名</th><td>{hostname}</td><th>IP地址</th><td>{ip_addr}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>操作系统</th><td>{os_version}</td><th>内核</th><td>{kernel_version}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>TCP服务</th><td>{tcp_listen_process_str}</td><th>UDP服务</th><td>{udp_listen_process_str}</td></tr>\n""")
        self.html_report_obj.writelines(f"""</table>\n""")

    def gen_html_report_(self):
        pass

    def create_accordion_card(self,accordion_id,accordion_title,collapse_id,show_flag=0,card_class="bg-danger text-white"):
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines(f"""<div id="{accordion_id}">\n""")
        self.html_report_obj.writelines("""<div class="card">\n""")
        self.html_report_obj.writelines(f"""<div class="card-header {card_class}">\n""")
        self.html_report_obj.writelines(f"""<a class="card-link {card_class}" data-toggle="collapse" href="#{collapse_id}">{accordion_title}</a>\n""")
        self.html_report_obj.writelines("""</div>\n""")
        if show_flag == 1:
            self.html_report_obj.writelines(f"""<div id="{collapse_id}" class="collapse show" data-parent="#{accordion_id}">\n""")
        else:
            self.html_report_obj.writelines(f"""<div id="{collapse_id}" class="collapse" data-parent="#{accordion_id}">\n""")
        self.html_report_obj.writelines("""<div class="card-body" style="padding:0.25rem">\n""")

    def close_div_label(self,times=1):
        for i in range(times):
            # print(f"{i}")
            self.html_report_obj.writelines("""</div>\n""")


    def gen_html_report_UnnecessarySoftware_section(self):
        accordion_id = "accordion1"
        accordion_title = "多余功能和软件安全"
        collapse_id = "collapse1"
        show_flag = 1


        # self.html_report_obj.writelines("""<div class="container">\n""")
        # self.html_report_obj.writelines(f"""<div id="{accordion_id}">\n""")
        self.create_accordion_card(accordion_id,accordion_title,collapse_id,show_flag)
        # self.html_report_obj.writelines("""<div class="card">\n""")
        # self.html_report_obj.writelines("""<div class="card-header">\n""")
        # self.html_report_obj.writelines("""<a class="card-link" data-toggle="collapse" href="#collapseOne">多余功能和软件安全</a>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""<div id="collapseOne" class="collapse show" data-parent="#accordion">\n""")
        # self.html_report_obj.writelines("""<div class="card-body">\n""")

        # 1.2.2.1多余功能和软件安全
        accordion_id = "accordion11"
        accordion_title = "如果不使用，卸载下列高危软件"
        collapse_id = "collapse11"
        # self.html_report_obj.writelines("""<div class="container">\n""")
        # self.html_report_obj.writelines(f"""<div id="{accordion_id}">\n""")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id)

        # self.html_report_obj.writelines("""<div class="card">\n""")
        # self.html_report_obj.writelines("""<div class="card-header">\n""")
        # self.html_report_obj.writelines("""<a class="card-link" data-toggle="collapse" href="#collapseOne1">如果不使用，卸载下列高危软件</a>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""<div id="collapseOne1" class="collapse show" data-parent="#accordion1">\n""")
        # self.html_report_obj.writelines("""<div class="card-body">\n""")
        self.html_report_obj.writelines("""<table id="UnnecessarySoftware_list" class="table">\n""")
        # self.html_report_obj.writelines("""<thead><tr><th>检测项</th><th>是否合规</th><th>检测说明</th><th>检测命令</th><th>检测结果</th></tr></thead>\n<tbody>""")
        software_list = ""
        installed_list = ""
        current_node = self.xml_obj.root.checklist.section[0].node[0]
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']

            software_list += f"{check_object}、"
            if check_result == "":
                check_right = "是"
            else:
                installed_list += f"{check_object}、"
        self.html_report_obj.writelines(f"""<tr><th>已安装软件</th><td>{installed_list}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>ps -ef | grep $software|grep -v grep</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td></td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{software_list}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        # 关闭内层
        self.close_div_label(5)
        # 关闭外层
        self.close_div_label(5)
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        #
        # # 关闭外层
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""</div>\n""")

    def gen_html_report_AcountLimit_section(self):
        # 1.2.2.2用户账号安全
        # 编号保持一致即可
        accordion_id = "accordion2"
        accordion_title = "用户账号安全"
        collapse_id = "collapse2"
        show_flag = 1
        # self.html_report_obj.writelines("""<div class="container">\n""")
        # self.html_report_obj.writelines(f"""<div id="{accordion_id}">\n""")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id,show_flag)
        # self.html_report_obj.writelines("""<div class="container">\n""")
        # self.html_report_obj.writelines("""<div id="accordion2">\n""")
        # self.html_report_obj.writelines("""<div class="card">\n""")
        # self.html_report_obj.writelines("""<div class="card-header">\n""")
        # self.html_report_obj.writelines("""<a class="card-link" data-toggle="collapse" href="#collapseOne2">密码安全策略</a>\n""")
        # self.html_report_obj.writelines("""</div>\n""")
        # self.html_report_obj.writelines("""<div id="collapseOne2" class="collapse show" data-parent="#accordion2">\n""")
        # self.html_report_obj.writelines("""<div class="card-body">\n""")

        current_node = self.xml_obj.root.checklist.section[1].node[0]
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']

            if check_object == "/etc/login.defs":
                accordion_id = "accordion21"
                accordion_title = "限制三类字符"
                collapse_id = "collapse21"

                if "not found" in check_result:
                    check_result_class = "bg-danger text-white"
                else:
                    check_result_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=check_result_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                # 关闭内层自己
                self.close_div_label(5)
        # 关闭外层
        self.close_div_label(5)

    def gen_html_report_ServiceSecurity_section(self):
        accordion_id = "accordion3"
        accordion_title = "网络服务器安全"
        collapse_id = "collapse3"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, show_flag)

        # 服务过滤Filtering
        accordion_id = "accordion31"
        accordion_title = "如果不使用，卸载下列高危软件"
        collapse_id = "collapse31"

        current_node = self.xml_obj.root.checklist.section[2].node[0]
        service_list = ""
        active_service_list = ""
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']

            service_list += f"{check_object}、"
            if "active (running)" in check_result:
                active_service_list += f"{check_object}、"
        card_class = "bg-success text-white"
        if active_service_list.replace("、","") != "":
            card_class = "bg-danger text-white"
        self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=card_class)
        self.html_report_obj.writelines("""<table id="ServiceSecurity_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已安装软件</th><td>{active_service_list}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>ps -ef | grep $software|grep -v grep</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td></td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{service_list}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

        current_node = self.xml_obj.root.checklist.section[2].node[1]
        # 服务过滤Filtering
        accordion_id = "accordion31"
        accordion_title = "/etc/inetd.conf"
        collapse_id = "collapse32"
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']
            if check_object == "/etc/xinetd.conf":
                permit_reg = "^-r*w*-{6,}"
                reg_result = re.match(permit_reg,check_result)
                card_class = "bg-danger text-white"
                if reg_result is not None:
                    card_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
            self.close_div_label(5)

        current_node = self.xml_obj.root.checklist.section[2].node[2]
        # 服务过滤Filtering
        accordion_id = "accordion31"
        accordion_title = "/etc/services"
        collapse_id = "collapse33"
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']
            if check_object == "/etc/services":
                permit_reg = "^-r*w*-{6,}"
                reg_result = re.match(permit_reg, check_result)
                card_class = "bg-danger text-white"
                if reg_result is not None:
                    card_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        self.close_div_label(5)

    def gen_html_report_SystemSettingSecurity_section(self):
        accordion_id = "accordion4"
        accordion_title = "系统设置安全"
        collapse_id = "collapse4"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, show_flag)

        accordion_id = "accordion41"
        accordion_title = "限制控制台的使用"
        collapse_id = "collapse41"
        current_node = self.xml_obj.root.checklist.section[3].node[0]
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']
            card_class = "bg-danger text-white"
            if check_object == "/etc/security/console.apps":
                if check_result == "" or "No such file" in check_result:
                    card_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)
        # self.close_div_label(5)

        accordion_id = "accordion42"
        accordion_title = "系统关闭Ping"
        collapse_id = "collapse42"
        current_node = self.xml_obj.root.checklist.section[3].node[1]
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']
            card_class = "bg-danger text-white"
            if check_object == "/proc/sys/net/ipv4/icmp_echo_ignore_all":
                if check_result == "1":
                    card_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        accordion_id = "accordion43"
        accordion_title = "Control-Alt-Delete 键盘关机命令"
        collapse_id = "collapse43"
        current_node = self.xml_obj.root.checklist.section[3].node[3]
        for item in current_node.item:
            check_object = item.check_object.__dict__['cdata']
            check_command = item.check_command.__dict__['cdata']
            check_comment = item.check_comment.__dict__['cdata']
            check_result = item.check_result.__dict__['cdata']
            card_class = "bg-danger text-white"
            if check_object == "/etc/init/control-alt-delete.conf":
                if "not found" not in check_result:
                    card_class = "bg-success text-white"
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="section_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)
        self.close_div_label(5)

    def gen_html_report_tail(self):
        self.html_report_obj.writelines("</body>\n")
        self.html_report_obj.writelines("</html>\n")

    def gen_html_report(self):
        self.gen_html_report_head()
        self.gen_html_report_hostinfo_table()
        self.gen_html_report_UnnecessarySoftware_section()
        self.gen_html_report_AcountLimit_section()
        self.gen_html_report_ServiceSecurity_section()
        self.gen_html_report_SystemSettingSecurity_section()
        self.gen_html_report_tail()

    def __del__(self):
        self.html_report_obj.close()


if __name__ == "__main__":
    gen_report_obj = GenHtmlReport()
    gen_report_obj.gen_html_report()