import pandas as pd
import numpy as np
import openpyxl.utils as open_xl_util


def get_join_column_name(file_name, sheet_name, row_num):
    """
        file_name excel的文件位置
        sheet_name 表单名或序号
        row_num 取sheet的前几行
    """
    row_num -= 1
    if type(sheet_name) is int:
        sheet_name -= 1
    excel_file = pd.read_excel(file_name, sheet_name=sheet_name)
    # print(excel_file)
    all_list = []
    for row in excel_file.itertuples():
        # 由用户输入来确定取前几行
        if row[0] < row_num:
            all_list.append(list(row[1:]))
        else:
            break
    # for least_item in all_list:
    #     print(least_item)

    least_list = []
    op_list = all_list
    for first_index, list_item in enumerate(op_list):
        temp_list = []
        for second_index, item_of_list in enumerate(list_item):
            if item_of_list is np.nan and second_index == 0:
                temp_list.append(item_of_list)
            # 如果该列是最后一列则不处理
            elif first_index == len(op_list)-1:
                temp_list.append(item_of_list)
            elif item_of_list is np.nan:
                # 如果该列的下面的列都为nan则不处理
                flag = False
                for i in range(first_index+1, len(op_list)-1):
                    if op_list[i][second_index] is not np.nan:
                        flag = True
                        break
                if flag is True:
                    # 找到前面一个不为nan的值
                    dest = ''
                    for i in range(second_index, 0, -1):
                        if list_item[i] is np.nan and i == 0:
                            break
                        if list_item[i] is not np.nan:
                            dest = list_item[i]
                            break
                    if dest == '':
                        temp_list.append(np.nan)
                    else:
                        temp_list.append(dest)
                else:
                    temp_list.append(item_of_list)
            else:
                temp_list.append(item_of_list)
        least_list.append(temp_list)

    for print_item in least_list:
        print(print_item)

    result = []
    for j in range(0, len(least_list[0])):
        column_name = ''
        for i in range(0, len(least_list)):
            if least_list[i][j] is not np.nan:
                temp = str(least_list[i][j]) + '_'
                column_name += temp
        result.append(column_name)
    return result


if __name__ == '__main__':
    # 用户输入Excel文件位置和Sheet名称
    column_list = get_join_column_name('D:/gaojiao_2019.xlsx', 1, 8)
    col_len = len(column_list)
    print(col_len)
    pre_concat_column_name = []

    pre_concat_list = list(map(lambda x: x.replace(' ', '').replace('\n', '')[0:-1], column_list))

    print(pre_concat_column_name)
    real_final_list = []
    for pre_index, pre_item in enumerate(pre_concat_list):
        real_final_str = '`'
        real_final_str += open_xl_util.get_column_letter(pre_index+1)
        real_final_str += '` string COMMENT \''
        real_final_str += pre_item
        real_final_str += '\','
        real_final_list.append(real_final_str)
        print(real_final_str)

