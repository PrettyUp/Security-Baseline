import os
import re
from lxml import html
import html
import lxml
import sys
sys.path.append('../../')
from common.baseline_parse import BaselineParse
from common.baseline_param_parse import BaselineParamParse


class GenTomcatHtmlReport(BaselineParse):
    def __init__(self,ip_addr):
        baseline_type = "Tomcat"
        super().__init__(ip_addr,baseline_type)

    # 删除示例文档
    def gen_html_report_ExampleDoc_section(self):
        accordion_id = "accordion1"
        accordion_title = "删除示例文档"
        collapse_id = "collapse1"

        current_item=self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkExampleDoc']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        if check_result is None:
            card_class = "bg-success text-white"
            self.config_right += 1
            check_result = ""
        else:
            if "docs" in check_result or "examples" in check_result or "manager" in check_result or "ROOT" in check_result or "host-manager" in check_result:
                card_class = "bg-danger text-white"
                self.config_error += 1
            else:
                card_class = "bg-success text-white"
                self.config_right += 1
            check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ExampleDoc_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 禁用tomcat默认帐号
    def gen_html_report_DefaultAccount_section(self):
        accordion_id = "accordion2"
        accordion_title = "禁用tomcat默认帐号"
        collapse_id = "collapse2"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkDefaultAccount']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result_item = current_item.xpath("check_result")[0]
        check_result_not_escape = lxml.html.tostring(check_result_item).decode('utf-8')
        start_pos = re.search("<check_result>",check_result_not_escape).end()
        end_pos = re.search("</check_result>",check_result_not_escape).start()
        check_result_not_escape = check_result_not_escape.replace("></user>","/>")
        check_result= html.escape(check_result_not_escape[start_pos:end_pos].strip("\n"))
        check_result = check_result.replace("\n", "<br />")
        try:
            user_items = check_result_item.xpath("user")
            if len(user_items) == 0:
                card_class = "bg-success text-white"
                self.config_right += 1
            else:
                self.config_error += 1
                card_class = "bg-danger text-white"
            #check_result = etree.tostring(user_items[0])
        except:
            card_class = "bg-success text-white"
            self.config_right += 1
            check_result = "error occur while parse, please check it manually"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="DefaultAccount_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 禁止列目录
    def gen_html_report_ListDir_section(self):
        accordion_id = "accordion3"
        accordion_title = "禁止列目录"
        collapse_id = "collapse3"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkListDir']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result_item = current_item.xpath("check_result")[0]
        check_result = ""
        try:
            list_dir_item = check_result_item.xpath("init-param[param-name = 'listings']")[0]
            list_dir_item_value = list_dir_item.xpath("param-value/text()")[0]

            check_result_not_escape = lxml.html.tostring(list_dir_item).decode('utf-8')
            start_pos = re.search("<init-param>", check_result_not_escape).end()
            end_pos = re.search("</init-param>", check_result_not_escape).start()
            check_result = html.escape(check_result_not_escape[start_pos:end_pos].strip("\n"))
            check_result = check_result.replace("\n", "<br />")

            if list_dir_item_value == "false":
                card_class = "bg-success text-white"
                self.config_right += 1
            else:
                self.config_error += 1
                card_class = "bg-danger text-white"
        except:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ListDir_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 自定义错误页面
    def gen_html_report_ErrorPage_section(self):
        accordion_id = "accordion4"
        accordion_title = "自定义错误页面"
        collapse_id = "collapse4"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkErrorPage']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = ''
        check_result_item = current_item.xpath("check_result")[0]

        check_result_not_escape = lxml.html.tostring(check_result_item).decode('utf-8')
        # start_pos = re.search("<init-param>", check_result_not_escape).end()
        # end_pos = re.search("</init-param>", check_result_not_escape).start()
        check_result = html.escape(check_result_not_escape.strip("\n"))
        check_result = check_result.replace("\n", "<br />")
        try:
            error_code_list = check_result_item.xpath("error-page/error-code/text()")
            error_code_str = "、".join(error_code_list)
            if ("401" in error_code_str) and ("404" in error_code_str) and ("500" in error_code_str):
                card_class = "bg-success text-white"
                self.config_right += 1
            else:
                self.config_error += 1
                card_class = "bg-danger text-white"
        except:
            self.config_error += 1
            card_class = "bg-danger text-white"
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ErrorPage_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 开启访问日志
    def gen_html_report_EnableAccessLog_section(self):
        accordion_id = "accordion5"
        accordion_title = "开启访问日志"
        collapse_id = "collapse5"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkEnableAccessLog']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result_item = current_item.xpath("check_result")[0]

        check_result_not_escape = lxml.html.tostring(check_result_item).decode('utf-8')
        start_pos = re.search("<check_result>", check_result_not_escape).end()
        end_pos = re.search("</check_result>", check_result_not_escape).start()
        check_result = html.escape(check_result_not_escape[start_pos:end_pos].strip("\n"))
        check_result = check_result.replace("\n", "<br />")

        if check_result.strip() == "":
            self.config_error += 1
            card_class = "bg-danger text-white"
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="EnableAccessLog_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 隐藏版本号
    def gen_html_report_ServerVersion_section(self):
        accordion_id = "accordion6"
        accordion_title = "隐藏版本号"
        collapse_id = "collapse6"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkServerVersion']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result_item = current_item.xpath("check_result")[0]

        check_result_not_escape = lxml.html.tostring(check_result_item).decode('utf-8')
        start_pos = re.search("<check_result>", check_result_not_escape).end()
        end_pos = re.search("</check_result>", check_result_not_escape).start()
        check_result = html.escape(check_result_not_escape[start_pos:end_pos].strip("\n"))
        check_result = check_result.replace("\n", "<br />")

        version_name_pattern = "Server\s*number:\s*"
        version_value_pattern = "Server\s*number:\s*[\d|\.]+"
        version_str = ''
        # 找表版本号，表示未隐藏版本号
        try:
            version_value = re.search(version_value_pattern,check_result).group()
            self.config_error += 1
            card_class = "bg-danger text-white"
        except:
            # 如果找不到版本号，但找得到Server number:则表示已隐藏版本号
            try:
                version_name = re.search(version_name_pattern, check_result).group()
                self.config_right += 1
                card_class = "bg-success text-white"
            # 两个都找不到说明version.sh执行出错
            except:
                self.config_warn += 1
                card_class = "bg-warning text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ServerVersion_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 修改默认监听端口
    def gen_html_report_DefaultPort_section(self):
        accordion_id = "accordion7"
        accordion_title = "修改默认监听端口"
        collapse_id = "collapse7"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkDefaultPort']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result_item = current_item.xpath("check_result")[0]

        check_result_not_escape = lxml.html.tostring(check_result_item).decode('utf-8')
        start_pos = re.search("<check_result>", check_result_not_escape).end()
        end_pos = re.search("</check_result>", check_result_not_escape).start()
        check_result = html.escape(check_result_not_escape[start_pos:end_pos].strip("\n"))
        check_result = check_result.replace("\n", "<br />")

        if check_result.strip() != "":
            self.config_warn += 1
            card_class = "bg-warning text-white"
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="DefaultPort_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 不以root/admin用户运行程序
    def gen_html_report_ProcessRunner_section(self):
        accordion_id = "accordion8"
        accordion_title = "不以root/admin用户运行程序"
        collapse_id = "collapse8"

        current_item = self.node_xpath(self.xml_obj,"/root/checklist/section[@id='checkProcessRunner']/item")[0]
        check_object = self.text_xpath(current_item, "check_object")
        check_command = self.text_xpath(current_item, "check_command")
        check_comment = self.text_xpath(current_item, "check_comment")
        check_result = self.text_xpath(current_item, "check_result")
        try:
            check_result_dict = check_result.split()
            if check_result_dict[0] == "root":
                self.config_error += 1
                card_class = "bg-warn text-white"
            else:
                card_class = "bg-success text-white"
                self.config_right += 1
        except:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ProcessRunner_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 这里只需要调用自己生成各检测项报告的函数即可
    # 头部已由在__init__()中调用super().__init()生成
    # 尾部已由在__del__()中调用super().__del__()生成
    def gen_html_report(self):
        self.gen_html_report_ExampleDoc_section()
        self.gen_html_report_DefaultAccount_section()
        self.gen_html_report_ListDir_section()
        self.gen_html_report_ErrorPage_section()
        self.gen_html_report_EnableAccessLog_section()
        self.gen_html_report_ServerVersion_section()
        self.gen_html_report_DefaultPort_section()
        self.gen_html_report_ProcessRunner_section()

    def __del__(self):
        super().__del__()
        self.html_report_obj.close()


if __name__ == "__main__":
    bpp_obj = BaselineParamParse()
    model, ip = bpp_obj.param_parse(sys.argv[1:])
    if model == "ip":
        # 如果ip模式中未给出ip列出则报错退出
        if ip is None:
            bpp_obj.usage()
            sys.exit(1)
        else:
            ip_list = ip.split(",")
            for ip_addr in ip_list:
                # 如果指定的ip对应的文件并不存在则跳过
                if not os.path.exists(f"../2_info/{ip_addr}_tomcat_info.xml"):
                    print(f'sorry, file "../2_info/{ip_addr}_tmocat_info.xml" is not exist, it will be skip')
                    continue
                gen_report_obj = GenTomcatHtmlReport(ip_addr)
                gen_report_obj.gen_html_report()
    # 如果指定文件夹模式
    elif model == "dir":
        ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
        full_reg = f"{ip_reg}_tomcat_info\.xml"
        pwd_file_list = os.listdir("../2_info")
        for file in pwd_file_list:
            if re.search(full_reg, file):
                ip_addr = re.search(ip_reg, file).group()
                gen_report_obj = GenTomcatHtmlReport(ip_addr)
                gen_report_obj.gen_html_report()