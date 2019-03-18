import os
import re


from lxml import html
import html
import lxml
import sys
sys.path.append('../../')
from common.baseline_parse import BaselineParse


class GenMysqlHtmlReport(BaselineParse):
    def __init__(self,ip_addr):
        baseline_type = "Mysql"
        super().__init__(ip_addr,baseline_type)

    # 禁止以root用户运行
    def gen_html_report_MysqlRunner_section(self):
        accordion_id = "accordion1"
        accordion_title = "禁止以root用户运行"
        collapse_id = "collapse1"

        current_item=self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlRunner']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result is None or check_result.split()[0] != "root":
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ExampleDoc_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 设置最大连接数限制
    def gen_html_report_MysqlMaxConnections_section(self):
        accordion_id = "accordion2"
        accordion_title = "设置最大连接数限制"
        collapse_id = "collapse2"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlMaxConnections']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result is not None:
            card_class = "bg-success text-white"
            self.config_right += 1
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
            check_result = ""
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ExampleDoc_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 检测是否存在空账号或test账号
    def gen_html_report_MysqlNullTestAccount_section(self):
        accordion_id = "accordion3"
        accordion_title = "检测是否存在空账号或test账号"
        collapse_id = "collapse3"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlNullTestAccount']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result is None:
            card_class = "bg-success text-white"
            self.config_right += 1
            check_result = ""
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
            check_result = ""
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ExampleDoc_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 检测是否存在密码为空的账号
    def gen_html_report_MysqlNoPassword_section(self):
        accordion_id = "accordion4"
        accordion_title = "检测是否存在密码为空的账号"
        collapse_id = "collapse4"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlNoPassword']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result is None:
            card_class = "bg-success text-white"
            self.config_right += 1
            check_result = ""
        else:
            card_class = "bg-danger text-white"
            self.config_error += 1
            check_result = ""
        check_result = check_result.replace("\n", "<br />")
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ExampleDoc_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)


    # 分角色创建账号同时删除不必要的账号
    def gen_html_report_MysqlAccount_section(self):
        accordion_id = "accordion5"
        accordion_title = "分角色创建账号同时删除不必要的账号"
        collapse_id = "collapse5"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlAccount']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        check_result = check_result.replace("\n", "<br />")

        self.config_warn += 1
        card_class = "bg-warning text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="DefaultAccount_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 开启日志
    def gen_html_report_MysqlLog_section(self):
        accordion_id = "accordion6"
        accordion_title = "开启日志"
        collapse_id = "collapse6"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlLog']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        check_result = check_result.replace("\n", "<br />")

        self.config_warn += 1
        card_class = "bg-warning text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ListDir_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 确认mysql是最新版本
    def gen_html_report_MysqlVersion_section(self):
        accordion_id = "accordion7"
        accordion_title = "确认mysql是最新版本"
        collapse_id = "collapse7"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkMysqlVersion']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text

        self.config_warn += 1
        card_class = "bg-warning text-white"

        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="ErrorPage_list" class="table">\n""")
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
        self.gen_html_report_MysqlRunner_section()
        self.gen_html_report_MysqlMaxConnections_section()
        self.gen_html_report_MysqlNullTestAccount_section()
        self.gen_html_report_MysqlNoPassword_section()
        self.gen_html_report_MysqlAccount_section()
        self.gen_html_report_MysqlLog_section()
        self.gen_html_report_MysqlVersion_section()

    def __del__(self):
        super().__del__()
        self.html_report_obj.close()


if __name__ == "__main__":
    ip_reg = "(\d{1,3}\.{1}){3}\d{1,3}"
    full_reg = f"{ip_reg}_mysql_info\.xml"
    pwd_file_list = os.listdir("../2_info")
    for file in pwd_file_list:
        if re.search(full_reg, file):
            ip_addr = re.search(ip_reg, file).group()
            gen_report_obj = GenMysqlHtmlReport(ip_addr)
            gen_report_obj.gen_html_report()