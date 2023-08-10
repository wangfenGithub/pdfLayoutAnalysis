import pdfplumber
import pandas as pd

# tablecsv_save_dir = r".\TableJsonResult"
def tableProcess(pdf_path,pdf_page,table_excel_path):
    # 读取pdf文件,保存为pdf实例
    pdf = pdfplumber.open(pdf_path)

    # 访问第一页
    first_page = pdf.pages[pdf_page]

    # 自动读取表格信息,返回列表
    table = first_page.extract_table()
    # 将列表转化为dataframe
    if table:
        table_data = pd.DataFrame(table[1:], columns=table[0])

        # 保存为excel
        table_data.to_excel(table_excel_path, index=False)

        print("table:{}".format(table))
