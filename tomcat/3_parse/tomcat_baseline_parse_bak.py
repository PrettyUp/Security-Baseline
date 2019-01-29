import re
from lxml import etree

class GenTomcatHtmlReport():
    def __init__(self):
        self.xml_obj = etree.parse("tomcat_report_xml.xml")
        # self.xml_obj = untangle.parse('os_report_xml.xml')
        ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        self.html_report_obj = open(f"{ip_addr}_tomcat.html", "w+", encoding='utf-8')
        self.config_right = 0
        self.config_warn = 0
        self.config_error = 0


    # 生成html头部信息
    def gen_html_report_head(self):
        ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        self.html_report_obj.writelines("<html>\n")
        self.html_report_obj.writelines("<head>\n")
        self.html_report_obj.writelines(f"""<meta charset="utf-8" />\n""")
        self.html_report_obj.writelines(f"<title>{ip_addr}</title>\n")
        self.html_report_obj.writelines(f'<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css"></link>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/jquery-3.3.1.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/popper.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="bootstrap/js/bootstrap.min.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/highcharts.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/highcharts-3d.js"></script>\n')
        self.html_report_obj.writelines(f'<script src="highcharts/exporting.js"></script>\n')
        self.html_report_obj.writelines("</head>\n")

    def gen_html_report_header(self):
        self.html_report_obj.writelines("<body>\n")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines('<h3 style="text-align:center;">Tomcat基线扫描报告</h3>\n')
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""</div>\n""")


    def gen_html_report_tail(self):
        self.html_report_obj.writelines("</body>\n")
        self.html_report_obj.writelines("</html>\n")

    # 生成主机信息节区
    def gen_html_report_hostinfo_table(self):
        hostname = self.xml_obj.xpath("/root/hostinfo/hostname")[0].text
        ip_addr = self.xml_obj.xpath("/root/hostinfo/ipaddr")[0].text
        os_version = self.xml_obj.xpath("/root/hostinfo/os_version")[0].text.strip()
        kernel_version = self.xml_obj.xpath("/root/hostinfo/kernel_version")[0].text.strip()
        tcp_services = self.xml_obj.xpath("/root/hostinfo/tcp_services")[0].text
        udp_services = self.xml_obj.xpath("/root/hostinfo/udp_services")[0].text
        tcp_services_lines = tcp_services.split("\n")
        udp_services_lines = udp_services.split("\n")
        listen_addr_reg = "[\.|\d]+:\d+"
        process_reg = "\d+/\w+"

        tcp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg, line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg, line).group().split("/")[-1]
                    tcp_listen_process_str += f"{listen_addr}-{process}<br />"

        udp_listen_process_str = ""
        for line in tcp_services_lines:
            if "tcp6" not in line:
                listen_addr = re.search(listen_addr_reg, line)
                if listen_addr is not None:
                    listen_addr = listen_addr.group()
                    process = re.search(process_reg, line).group().split("/")[-1]
                    udp_listen_process_str += f"{listen_addr}-{process}<br />"

        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>1. 主机基本信息<th></h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<table id="hostinfo" class="table table-striped">\n""")
        # self.html_report_obj.writelines("""<tr><th colspan="4" style="text-align:center;">主机基本信息<th></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>主机名</th><td>{hostname}</td><th>IP地址</th><td>{ip_addr}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>操作系统</th><td>{os_version}</td><th>内核</th><td>{kernel_version}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>TCP服务</th><td>{tcp_listen_process_str}</td><th>UDP服务</th><td>{udp_listen_process_str}</td></tr>\n""")
        self.html_report_obj.writelines(f"""</table>\n""")
        self.html_report_obj.writelines("""</div>\n""")

    def gen_html_report_pie(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>2. 合规统计信息<th></h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div id="pie_container" style="min-width:400px;height:400px"></div>""")
        self.html_report_obj.writelines("""</div>\n""")

    # 数据在后边各项统计完成后才能得出所以得分出来
    def gen_html_report_pie_fill_data(self):
        self.html_report_obj.writelines("""
                <script>
                    var  chart = Highcharts.chart('pie_container', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                options3d: {
                    enabled: true,
                    alpha: 45,
                    beta: 0
                }
            },
            title: {
                text: '合规检测统计图'
            },
            tooltip: {
                headerFormat: '{series.name}<br>',
                pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    depth: 35,
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    },
                    states: {
                        hover: {
                            enabled: false
                        }  
                    },
                    slicedOffset: 10,         // 突出间距
                    point: {                  // 每个扇区是数据点对象，所以事件应该写在 point 下面
                        events: {
                            // 鼠标滑过是，突出当前扇区
                            mouseOver: function() {
                                this.slice();
                            },
                            // 鼠标移出时，收回突出显示
                            mouseOut: function() {
                                this.slice();
                            },
                            // 默认是点击突出，这里屏蔽掉
                            click: function() {
                                return false;
                            }
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: '检测项占比',
                data: [
                    {name:'合规',   """)
        # 这里不没有很好的格式化办法，各项数据只能单独写入
        self.html_report_obj.writelines(f"y:{self.config_right}")
        self.html_report_obj.writelines(""",color:'#28a745'},
                    {name:'待审查',""")
        self.html_report_obj.writelines(f"y: {self.config_warn}")
        self.html_report_obj.writelines(""",color:'#ffc107'},
                    {name:'不合规',   """)
        self.html_report_obj.writelines(f"y:{self.config_error}")
        self.html_report_obj.writelines(""",color:'#dc3545'}
                ]
            }]
        });
                </script>\n""")

    # 生成展开卡片
    def create_accordion_card(self, accordion_id, accordion_title, collapse_id, show_flag=0, card_class="bg-danger text-white"):
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
        for _ in range(times):
            # print(f"{i}")
            self.html_report_obj.writelines("""</div>\n""")

    def gen_html_report_ExampleDoc_section(self):
        accordion_id = "accordion1"
        accordion_title = "删除示例文档"
        collapse_id = "collapse1"

        current_item=self.xml_obj.xpath("/root/checklist/section[@id='checkExampleDoc']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if "docs" in check_result or "examples" in check_result or "manager" in check_result or "ROOT" in check_result or "host-manager" in check_result:
            card_class = "bg-danger text-white"
            self.config_error += 1
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    def gen_html_report_DefaultAccount_section(self):
        accordion_id = "accordion2"
        accordion_title = "禁用tomcat默认帐号"
        collapse_id = "collapse2"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkDefaultAccount']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        try:
            user_items = check_result.xpath("user")
            self.config_error += 1
            card_class = "bg-danger text-white"
        except:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 这个处理过程没实现
    def gen_html_report_ListDir_section(self):
        accordion_id = "accordion3"
        accordion_title = "禁止列目录"
        collapse_id = "collapse3"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkListDir']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = ''
        check_result_item = current_item.xpath("check_result")[0]
        try:
            list_dir_item = check_result_item.xpath("init-param[param-name = 'listings']")[0]
            check_result += "listings:"
            list_dir_item_value = list_dir_item.xpath("param-value/text()")[0]
            check_result += list_dir_item_value
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
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    # 这个处理过程没实现
    def gen_html_report_ErrorPage_section(self):
        accordion_id = "accordion4"
        accordion_title = "自定义错误页面"
        collapse_id = "collapse4"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkErrorPage']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = ''
        check_result_item = current_item.xpath("check_result")[0]
        try:
            error_code_list = check_result_item.xpath("error-page/error-code/text()")
            error_code_str = "、".join(error_code_list)
            check_result += error_code_str
            if ("401" in error_code_str) and ("404" in error_code_str) and ("500" in error_code_str):
                card_class = "bg-success text-white"
                self.config_right += 1
        except:
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

    def gen_html_report_EnableAccessLog_section(self):
        accordion_id = "accordion5"
        accordion_title = "开启访问日志"
        collapse_id = "collapse5"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkEnableAccessLog']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result.strip() == "":
            self.config_error += 1
            card_class = "bg-danger text-white"
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    def gen_html_report_ServerVersion_section(self):
        accordion_id = "accordion6"
        accordion_title = "隐藏版本号"
        collapse_id = "collapse6"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkServerVersion']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
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
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    def gen_html_report_DefaultPort_section(self):
        accordion_id = "accordion7"
        accordion_title = "修改默认监听端口"
        collapse_id = "collapse7"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkDefaultPort']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        if check_result.strip() != "":
            self.config_error += 1
            card_class = "bg-danger text-white"
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    def gen_html_report_ProcessRunner_section(self):
        accordion_id = "accordion8"
        accordion_title = "不以root/admin用户运行程序"
        collapse_id = "collapse8"

        current_item = self.xml_obj.xpath("/root/checklist/section[@id='checkProcessRunner']/item")[0]
        check_object = current_item.xpath("check_object")[0].text
        check_command = current_item.xpath("check_command")[0].text
        check_comment = current_item.xpath("check_comment")[0].text
        check_result = current_item.xpath("check_result")[0].text
        check_result_dict = check_result.split()
        if check_result_dict[0] == "root":
            self.config_error += 1
            card_class = "bg-danger text-white"
        else:
            card_class = "bg-success text-white"
            self.config_right += 1
        self.create_accordion_card(accordion_id, accordion_title, collapse_id, card_class=card_class)
        self.html_report_obj.writelines("""<table id="UnnecessaryDevTool_list" class="table">\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测项</th><td>{check_object}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测命令</th><td>{check_command}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测说明</th><td>{check_comment}</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><th>检测结果</th><td>{check_result}</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.close_div_label(5)

    def gen_html_report_create_section_collect(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>3. 合规检测项详情<th></h4>\n""")
        self.html_report_obj.writelines("""<br />""")

    def gen_html_report_close_section_collect(self):
        self.close_div_label()

    def gen_html_report_explain(self):
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<div class="container">\n""")
        self.html_report_obj.writelines("""<h4>4. 说明<th></h4>\n""")
        self.html_report_obj.writelines("""<br />""")
        self.html_report_obj.writelines("""<table id="report_explain" class="table table-striped">\n""")
        self.html_report_obj.writelines(f"""<tr><td>红色</td><td>不符合配置规范要求，需要进行加固</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><td>黄色</td><td>不确定是否符合配置规范要求，需要人工介入确认</td></tr>\n""")
        self.html_report_obj.writelines(f"""<tr><td>绿色</td><td>确认符合配置规范要求，不需要进行修改</td></tr>\n""")
        self.html_report_obj.writelines("""</table>\n""")
        self.html_report_obj.writelines("""</div>""")



    def gen_html_report(self):
        self.gen_html_report_head()
        self.gen_html_report_header()
        self.gen_html_report_hostinfo_table()
        self.gen_html_report_pie()
        self.gen_html_report_create_section_collect()
        self.gen_html_report_ExampleDoc_section()
        self.gen_html_report_DefaultAccount_section()
        self.gen_html_report_ListDir_section()
        self.gen_html_report_ErrorPage_section()
        self.gen_html_report_EnableAccessLog_section()
        self.gen_html_report_ServerVersion_section()
        self.gen_html_report_DefaultPort_section()
        self.gen_html_report_ProcessRunner_section()
        self.gen_html_report_close_section_collect()
        self.gen_html_report_explain()
        self.gen_html_report_pie_fill_data()
        self.gen_html_report_tail()

    def __del__(self):
        self.html_report_obj.close()


if __name__ == "__main__":
    gen_report_obj = GenTomcatHtmlReport()
    gen_report_obj.gen_html_report()