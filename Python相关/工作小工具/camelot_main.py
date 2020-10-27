import os
import time
import camelot
import numpy as np
import pandas as pd


def get_file_name(path):
    return path.split('/')[-1]


# 1.这张表全部在pdf的某一页上
# 2.表在多张pdf上
# 3.表在多张pdf上，并且某页pdf上还有其他的表格
# 综上，需要提供解析pdf的 `哪几页` `哪几个分表` 并且一第一个指定分表的形状为准
# 文件路径 页数 从第几个开始 到第几个结束 表头长度
# 限制：一次只能解析一张表
def parse_tables_in_pdf(
        file_path,
        page_list,
        sub_table_start=1,
        sub_table_end=1,
        table_header_len=1):
    """
    将pdf里的一个表格解析并输出到一个Excel表里
    :param (str) file_path: pdf文件路径
    :param (list) page_list: 这张表所在的页数
    :param (num) sub_table_start: 如果这张表被分布在不同的pdf页面中，
    请输入该表格开始部分是位于所有已解析的所有表格的第几个
    :param (num) sub_table_end: 如果这张表被分布在不同的pdf页面中，
    请输入该表格结束部分是位于所有已解析的所有表格的第几个
            Note: 如果这张表被分成了多个部分，分表之间不应该包含其他表格，
            或者你可以通过设置@param page_nums来灵活使用
    :param (num) table_header_len: 要解析的表格的表头长度
    :return: None
    """
    # check the legality of the params
    if os.path.exists(file_path) is False:
        print('please input the correct pdf file path!')
        return
    if len(page_list) < 1:
        print('page_nums\'s length at least 1')
        return

    # parse tables of the pdf
    pages_str = ','.join(str(x) for x in page_list)
    tables = camelot.read_pdf(file_path, pages=pages_str)
    real_table_num = len(tables)
    if real_table_num < 1:
        print('can not find any tables in pdf with specify params!')
        return

    all_data_list = []
    for sub_table_num in range(sub_table_start - 1, sub_table_end):
        if sub_table_num > sub_table_start - 1 and real_table_num > 1:
            # 去掉相同的表头
            all_data_list.extend(tables[sub_table_num].data[table_header_len:])
        else:
            all_data_list.extend(tables[sub_table_num].data)
    data_matrix = np.array(all_data_list)
    data_frame = pd.DataFrame(data_matrix)
    output_file_name = ''
    output_file_name += get_file_name(file_path)
    output_file_name += '_第'
    output_file_name += pages_str
    output_file_name += '页_第'
    output_file_name += str(sub_table_start)
    if sub_table_start != sub_table_end:
        output_file_name += '-'
        output_file_name += str(sub_table_end)
    output_file_name += '个_'
    output_file_name += time.strftime('%Y-%m-%d-%H%M%S', time.localtime())
    output_file_name += '.xlsx'
    with pd.ExcelWriter(output_file_name, mode='w') as writer:
        data_frame.to_excel(writer)
    # data_frame.to_csv(output_file_name)


if __name__ == '__main__':
    input_file_path = 'D://教育管理基础信息.pdf'
    input_page_list = [44]
    input_start = 1
    input_end = 1

    parse_tables_in_pdf(
        file_path=input_file_path,
        page_list=input_page_list,
        sub_table_start=input_start,
        sub_table_end=input_end
    )
