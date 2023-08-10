# import yaml
#
# yaml_path = r"D:\codeMyself\pythonProject\KUNLun_Bushu\peizhi.yaml"
# try:
#     with open(yaml_path, "r", encoding="utf-8") as f:
#         data = yaml.load(f, Loader=yaml.FullLoader)
#         print(list(data.keys()))
# except:
#     print(None)


# try:
#         # 打开文件
#         with open(yaml_path,"r",encoding="utf-8") as f:
#             data=yaml.load(f,Loader=yaml.FullLoader)
#             return data
#     except:
#         return None


data = {"111":{"name":"张三"},"222":{"id":23,"age":23,"name":"李四"}}
print(data.items())