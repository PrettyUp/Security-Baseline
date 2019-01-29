import os
import re
import sys
sys.path.append('../../')
from common.baseline_parse import BaselineParse


class GenOSHtmlReport(BaselineParse):
    def __init__(self,ip_addr):
        baseline_type = "OS"
        super().__init__(ip_addr,baseline_type)

    # 生成第一大节html报告
    def gen_html_report_UnnecessarySoftware_section(self):
        accordion_no = "1"
        collapse_no = 0
        accordion_class_sign = []
        # 第一大节展开菜单
        accordion_id = f"accordion{accordion_no}"
        accordion_title = "多余功能和软件安全"
        collapse_id = f"collapse{accordion_no}"
        show_flag = 1
        self.create_accordion_card(accordion_id,accordion_title,collapse_id,show_flag)

        collapse_no += 1
        # a、禁止任何现网运行的机器上安装有开发工具，包括编译器，调试器，开发库等。
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "禁止任何现网运行的机器上安装有开发工具，包括编译器，调试器，开发库等"
        collapse_id = f"collapse11{accordion_no}{collapse_no}"

        tool_check_list = []
        tool_exist_list = []
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='UnnecessarySoftware']/node[@id='UnnecessaryDevTool']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text

            tool_check_list.append(check_object)
            if check_result is None:
                self.config_right += 1
            else:
                tool_exist_list.append(check_object)
                self.config_error += 1



        if len(tool_exist_list) == 0:
            card_class = "bg-success text-white"
        else:
            card_class = "bg-danger text-white"
            accordion_class_sign.append("bg-danger")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已安装开发工具</th><td>{"、".join(tool_exist_list)}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>which $tool</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>检测编译、调试工具是否存在</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{"、".join(tool_check_list)}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        # 关闭内层
        self.close_div_label(5)

        collapse_no += 1
        # 1.2.2.1多余功能和软件安全
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "如果不使用，卸载下列高危软件"
        collapse_id = f"collapse{accordion_no}{collapse_no}"

        software_list = []
        installed_list = []
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='UnnecessarySoftware']/node[@id='UnnecessarySoftware']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text

            software_list.append(check_object)
            if check_result is None:
                self.config_right += 1
            else:
                installed_list.append(check_object)
                self.config_error += 1

        if len(installed_list) == 0:
            card_class = "bg-success text-white"
        else:
            card_class = "bg-danger text-white"
            accordion_class_sign.append("bg-danger")

        self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessarySoftware_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已安装软件</th><td>{"、".join(installed_list)}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>ps -ef | grep $software|grep -v grep</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td></td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{"、".join(software_list)}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        # 关闭内层
        self.close_div_label(5)
        # 关闭外层
        self.close_div_label(5)
        self.correct_accordion_class(f"collapse{accordion_no}",accordion_class_sign)

    # 生成第二大节“用户账号安全”html报告
    def gen_html_report_AcountLimit_section(self):
        accordion_no = "2"
        collapse_no = 0
        accordion_class_sign = []
        # 1.2.2.2用户账号安全
        # 编号保持一致即可
        accordion_id = f"accordion{accordion_no}"
        accordion_title = "用户账号安全"
        collapse_id = f"collapse{accordion_no}"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id,show_flag)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "口令长度限制"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='PasswdLengthLimit']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            if check_object == "/etc/login.defs":
                if "not found" in check_result:
                    check_result_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                else:
                    check_result_class = "bg-success text-white"
                    self.config_right += 1
                self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=check_result_class)
                self.html_report_obj.writelines("""<table id="AccountLengthLimit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                # 关闭内层自己
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "口令复杂度限制"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='PasswdComplexLimit']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            if check_object == "/etc/pam.d/common-password":
                if "not found" in check_result:
                    check_result_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                else:
                    check_result_class = "bg-success text-white"
                    self.config_right += 1
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=check_result_class)
                self.html_report_obj.writelines("""<table id="AccountLengthLimit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                # 关闭内层自己
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "口令日期限制"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='PasswdDateLimit']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            if check_object == "/etc/login.defs":
                if "not found" in check_result:
                    check_result_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                else:
                    check_result_class = "bg-success text-white"
                    self.config_right += 1
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=check_result_class)
                self.html_report_obj.writelines("""<table id="AccountDateLimit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                # 关闭内层自己
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "只允许wheel组su"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='SuLimit']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text

            if check_object == "/etc/pam.d/su":
                if check_result is None:
                    check_result_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                else:
                    check_result_class = "bg-success text-white"
                    self.config_right += 1
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=check_result_class)
                self.html_report_obj.writelines("""<table id="AccountLengthLimit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                # 关闭内层自己
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "/etc/passwd和/etc/shadow用户是否一致"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        item = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='PasswdContent']/item")[0]

        user_passwd = []
        check_object_passwd = item.xpath("check_object")[0].text.strip()
        check_command_passwd = item.xpath("check_command")[0].text.strip()
        check_comment_passwd = item.xpath("check_comment")[0].text.strip()
        check_result_passwd = item.xpath("check_result")[0].text
        check_result_passwd_list = check_result_passwd.split("\n")
        for line in check_result_passwd_list:
            user = line.split(":")[0]
            user_passwd.append(user)

        user_shadow = []
        item = self.xml_obj.xpath("/root/checklist/section[@id='AccountLimit']/node[@id='ShadowContent']/item")[0]
        check_object_shadow = item.xpath("check_object")[0].text.strip()
        check_command_shadow = item.xpath("check_command")[0].text.strip()
        check_comment_shadow = item.xpath("check_comment")[0].text.strip()
        check_result_shadow = item.xpath("check_result")[0].text
        check_result_shadow_list = check_result_shadow.split("\n")
        for line in check_result_shadow_list:
            user = line.split(":")[0]
            user_shadow.append(user)

        if user_passwd.sort() == user_shadow.sort():
            check_result_class = "bg-success text-white"
            self.config_right += 1
            check_result = "用户一致"
        else:
            check_result_class = "bg-warning text-white"
            self.config_warn += 1
            check_result = "用户不一致"
            accordion_class_sign.append("bg-danger")

        check_comment = "检测/etc/passwd和/etc/shadow用户是否一致"
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=check_result_class)
        self.html_report_obj.writelines("""<table id="AccountLengthLimit_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object_passwd}、{check_object_shadow}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command_passwd}、{check_command_shadow}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        # 关闭内层自己
        self.close_div_label(5)

        # 关闭外层
        self.close_div_label(5)
        self.correct_accordion_class(f"collapse{accordion_no}", accordion_class_sign)

    # 生成第三大节“网络服务器安全”html报告
    def gen_html_report_ServiceSecurity_section(self):
        accordion_no = "3"
        collapse_no = 0
        accordion_class_sign = []
        accordion_id = f"accordion{accordion_no}"
        accordion_title = "网络服务器安全"
        collapse_id = f"collapse{accordion_no}"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, show_flag)

        # 服务过滤Filtering
        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "服务过滤Filtering"
        collapse_id = f"collapse{accordion_no}{collapse_no}"

        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='ServiceSecurity']/node[@id='DangerService']/item")
        service_list = []
        active_service_list = []
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            service_list.append(check_object)
            if "active (running)" in check_result:
                self.config_error += 1
                active_service_list.append(check_object)
            else:
                self.config_right += 1
        card_class = "bg-success text-white"
        if len(active_service_list) != 0:
            card_class = "bg-danger text-white"
            accordion_class_sign.append("bg-danger")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id,card_class=card_class)
        self.html_report_obj.writelines("""<table id="ServiceSecurity_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已安装软件</th><td>{"、".join(active_service_list)}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>systemctl status $service</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>检测危险服务是否启动</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{"、".join(service_list)}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

        # 服务过滤Filtering
        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "/etc/inetd.conf"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='ServiceSecurity']/node[@id='InetdPermit']/item")

        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            if check_object == "/etc/xinetd.conf":
                permit_reg = "^-r*w*-{6,}"
                reg_result = re.match(permit_reg,check_result)

                if reg_result is not None:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    card_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="InetdPermit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        # 服务过滤Filtering
        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "/etc/services"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='ServiceSecurity']/node[@id='ServicesPermit']/item")

        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            if check_object == "/etc/services":
                permit_reg = "^[r|w|-]{3}-{6,}"
                reg_result = re.match(permit_reg, check_result)

                if reg_result is not None:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    card_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="ServicesPermit_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        # 服务过滤Filtering
        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "关闭危险服务进程"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='ServiceSecurity']/node[@id='ServicesProcess']/item")
        all_process_list = []
        active_process_list = []
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text

            all_process_list.append(check_object)
            if check_result is not None:
                active_process_list.append(check_object)
                self.config_error += 1
            else:
                self.config_right += 1

        if len(active_process_list) == 0:
            card_class = "bg-success text-white"
        else:
            card_class = "bg-danger text-white"
            accordion_class_sign.append("bg-danger")

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ServicesPermit_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已启动项</th><td>{"、".join(active_process_list)}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{"、".join(all_process_list)}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

        self.close_div_label(5)
        self.correct_accordion_class(f"collapse{accordion_no}", accordion_class_sign)

    # 生成第四大节“系统设置安全”html报告
    def gen_html_report_SystemSettingSecurity_section(self):
        accordion_no = "4"
        collapse_no = 0
        accordion_class_sign = []
        accordion_id = f"accordion{accordion_no}"
        accordion_title = "系统设置安全"
        collapse_id = f"collapse{accordion_no}"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, show_flag)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "限制控制台的使用"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='ConsoleAppsExists']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            card_class = "bg-danger text-white"
            if check_object == "/etc/security/console.apps":
                if check_result == "" or "No such file" in check_result:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="ConsoleAppsExists_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)
        # self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "系统关闭Ping"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='PingClose']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            card_class = "bg-danger text-white"
            if check_object == "/proc/sys/net/ipv4/icmp_echo_ignore_all":
                if check_result == "1":
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="PingClose_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "禁止其他tty"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='TtyStatus']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            if check_object == "/etc/securetty":
                if "not found" in check_result:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    card_class = "bg-warning text-white"
                    self.config_warn += 1
                    check_result = check_result.replace("\n","<br />")
                    accordion_class_sign.append("bg-warning")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="PingClose_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)


        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "检测IP欺骗"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='HostConf']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            card_class = "bg-danger text-white"
            if check_object == "/etc/host.conf":
                if "not found" not in check_result:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="PingClose_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "禁用源路由"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='DisableSourceRoute']/item")
        all_list = []
        need_fix_list = []
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            all_list.append(check_object)

            if check_result == "1":
                need_fix_list.append(check_object)
                self.config_error += 1
                accordion_class_sign.append("bg-danger")
            else:
                self.config_right += 1
        if len(need_fix_list) == 0:
            card_class = "bg-success text-white"
        else:
            card_class = "bg-danger text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="CtrlAltDelDisable_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>已启用项</th><td>{"<br />".join(need_fix_list)}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>所有检测项</th><td>{"<br />".join(all_list)}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "启用Syn Cookie"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='SynCookie']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()

            if check_object == "/proc/sys/net/ipv4/tcp_syncookies":
                if check_result == "1":
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    card_class = "bg-danger text-white"
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="CtrlAltDelDisable_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "Control-Alt-Delete 键盘关机命令"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='SystemSettingSecurity']/node[@id='CtrlAltDelDisable']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            card_class = "bg-danger text-white"
            if check_object == "/etc/init/control-alt-delete.conf":
                if "not found" in check_result:
                    card_class = "bg-success text-white"
                    self.config_right += 1
                else:
                    self.config_error += 1
                    accordion_class_sign.append("bg-danger")
                self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
                self.html_report_obj.writelines("""<table id="CtrlAltDelDisable_list" class="table">\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
                self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
                self.html_report_obj.writelines("""</table>\n""")
                self.close_div_label(5)
        self.close_div_label(5)
        self.correct_accordion_class(f"collapse{accordion_no}", accordion_class_sign)

    # 生成第五大节“文件系统安全”html报告
    def gen_html_report_FileSystemSecurity_section(self):
        accordion_no = "5"
        collapse_no = 0
        accordion_class_sign = []
        accordion_id = f"accordion{accordion_no}"
        accordion_title = "文件系统安全"
        collapse_id = f"collapse{accordion_no}"
        show_flag = 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, show_flag)

        collapse_no += 1
        accordion_id = f"accordion{accordion_no}{collapse_no}"
        accordion_title = "文件权限"
        collapse_id = f"collapse{accordion_no}{collapse_no}"
        current_node_items = self.xml_obj.xpath("/root/checklist/section[@id='FileSystemSecurity']/node[@id='FindSuidFile']/item")
        for item in current_node_items:
            check_object = item.xpath("check_object")[0].text.strip()
            check_command = item.xpath("check_command")[0].text.strip()
            check_comment = item.xpath("check_comment")[0].text.strip()
            check_result = item.xpath("check_result")[0].text.strip()
            # accordion_title = check_comment
            if check_result != "":
                card_class = "bg-warning text-white"
                self.config_warn += 1
                accordion_class_sign.append("bg-warning")
            else:
                card_class = "bg-success text-white"
            check_result = check_result.replace("\n", "<br />")
            self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
            self.html_report_obj.writelines("""<table id="SuidFile_list" class="table">\n""")
            self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
            self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
            self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
            self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
            self.html_report_obj.writelines("""</table>\n""")
            # 关闭内层
            self.close_div_label(5)
        # 关闭外层
        self.close_div_label(5)
        self.correct_accordion_class(f"collapse{accordion_no}", accordion_class_sign)

    # 这里只需要调用自己生成各检测项报告的函数即可
    # 头部已由在__init__()中调用super().__init()生成
    # 尾部已由在__del__()中调用super().__del__()生成
    def gen_html_report(self):
        self.gen_html_report_UnnecessarySoftware_section()
        self.gen_html_report_AcountLimit_section()
        self.gen_html_report_ServiceSecurity_section()
        self.gen_html_report_SystemSettingSecurity_section()
        self.gen_html_report_FileSystemSecurity_section()

    def __del__(self):
        super().__del__()
        self.html_report_obj.close()


if __name__ == "__main__":
    ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
    full_reg = f"{ip_reg}_os_info\.xml"
    pwd_file_list = os.listdir("../2_info")
    for file in pwd_file_list:
        if re.search(full_reg, file):
            ip_addr = re.search(ip_reg, file).group()
            gen_report_obj = GenOSHtmlReport(ip_addr)
            gen_report_obj.gen_html_report()