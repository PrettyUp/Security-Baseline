import re
import os

from common.baseline_parse import BaselineParse


class GenNginxHtmlReport(BaselineParse):
    def __init__(self,ip_addr):
        baseline_type = "Nginx"
        super().__init__(ip_addr,baseline_type)

    # 查看nginx版本信息
    def gen_html_report_NginxVersion_section(self):
        accordion_id = "accordion1"
        accordion_title = "查看nginx版本信息"
        collapse_id = "collapse1"

        current_item=self.xml_obj.xpath("/root/checklist/section[@id='checkNginxVersion']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text

        self.config_warn += 1

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class="bg-warning text-white")
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 查看nginx是否隐藏版本号
    def gen_html_report_NginxHiddenVersion_section(self):
        accordion_id = "accordion2"
        accordion_title = "查看nginx是否隐藏版本号"
        collapse_id = "collapse2"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkNginxHiddenVersion']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if "off" in check_result:
            self.config_right += 1
            card_class="bg-success text-white"
        else:
            self.config_error += 1
            card_class="bg-danger text-white"
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")

        self.close_div_label(5)

    # 查看user-agent中否配置正确
    def gen_html_report_NginxUserAgent_section(self):
        accordion_id = "accordion3"
        accordion_title = "查看user-agent中否配置正确"
        collapse_id = "collapse3"
        n = 0

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkNginxUserAgent']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        str_reg = "java|3_parse|perl|ruby|curl|bash|echo|uname|base64|decode|md5sum|select|concat|httprequest|httpclient|nmap|scan"
        userAgent_reg = str_reg.split('|')

        for s in userAgent_reg:
            if s in check_result:
                n += 1
        if n == len(userAgent_reg):
            self.config_right += 1
            card_class="bg-success text-white"
        else:
            self.config_error += 1
            card_class="bg-danger text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 是否开启errorlog和accesslog访问日志
    def gen_html_report_ErrorLog_section(self):
        accordion_id = "accordion4"
        accordion_title = "是否开启errorlog和accesslog访问日志"
        collapse_id = "collapse4"
        n = 0
        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkErrorLog']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if "log_format" in check_result:
            n += 1
        if "access.log" in check_result:
            n += 1
        if n == 2:
            self.config_right += 1
            card_class = "bg-success text-white"
        else:
            self.config_error += 1
            card_class = "bg-danger text-white"
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 是否为特殊文件夹设置白名单IP
    def gen_html_report_LocationIpWhiteList_section(self):
        accordion_id = "accordion5"
        accordion_title = "是否为特殊文件夹设置白名单IP"
        collapse_id = "collapse5"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkLocationIpWhiteList']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text

        self.config_warn += 1

        self.create_accordion_card(accordion_id , accordion_title , collapse_id , card_class = "bg-warning text-white")
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 禁止访问没有默认页面文件夹时列出目录下所有文件
    def gen_html_report_checkAutoindex_section(self):
        accordion_id = "accordion6"
        accordion_title = "禁止访问没有默认页面文件夹时列出目录下所有文件"
        collapse_id = "collapse6"
        n = 0
        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkAutoindex']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if "not found" in check_result:
            self.config_right += 1
            card_class = "bg-success text-white"
        else:
            arr = check_result.split(';')
            for s in arr:
                if "on" in s:
                    n += 1
            if n == 0:
                self.config_right += 1
                card_class = "bg-success text-white"
            else:
                self.config_error += 1
                card_class = "bg-danger text-white"


        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)


    def gen_html_report(self):
        self.gen_html_report_NginxVersion_section()
        self.gen_html_report_NginxHiddenVersion_section()
        self.gen_html_report_NginxUserAgent_section()
        self.gen_html_report_ErrorLog_section()
        self.gen_html_report_LocationIpWhiteList_section()
        self.gen_html_report_checkAutoindex_section()

    def __del__(self):
        super().__del__()
        self.html_report_obj.close()

if __name__ == "__main__":
    ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
    full_reg = f"{ip_reg}_nginx_info\.xml"
    pwd_file_list = os.listdir("../2_info")
    for file in pwd_file_list:
        if re.search(full_reg, file):
            ip_addr = re.search(ip_reg, file).group()
            gen_report_obj = GenNginxHtmlReport(ip_addr)
            gen_report_obj.gen_html_report()