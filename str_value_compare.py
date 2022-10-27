from ast import parse
import pandas as pd
import argparse
import xml.etree.ElementTree as ET

def parse_xml(source_):
    e_tree = ET.parse(source_)
    root = e_tree.getroot()
    children = root.getchildren()
    data_list = list()
    
    for child in children:
        if child.text is not None:
            data_list.append([child.get('name'), child.text])
        else:
            it = child.itertext()
            value = ""
            # import pdb; pdb.set_trace()
            tag_name = child.getchildren()[0].tag
            i = 0
            for text_piece in it:
                if i==0:
                    value += "<" + tag_name + ">"
                value += text_piece
                if i==0:
                    value += "</" + tag_name + ">"
                i+=1
            data_list.append([child.get('name'), value])
    return data_list
    
def parse_csv(dest_, origin_col_name,  cmp_col_name):
    dest_df = pd.read_csv(dest_, usecols = ['String ID', origin_col_name], encoding='utf-8')
    dest_df.rename({"String ID": "name", origin_col_name: cmp_col_name}, inplace=True, axis='columns')
    return dest_df

def compare(source_, source_col, dest_, dest_col):
    
    df_source = parse_csv(source_, source_col, "value_source")
    df_dest  = parse_csv(dest_, dest_col, "value_dest")
    df_cmp = df_source.merge(df_dest, on="name", how="inner", left_index=False, right_index=False)
    print("total_len:" + str(len(df_cmp)))
    # Multi conditon reference: https://blog.csdn.net/qq_38727626/article/details/100164430
    res_df = df_cmp[df_cmp["value_source"] != df_cmp["value_dest"]]
    
    if len(res_df) > 0:
        print("Total diff elements:"+ str(len(res_df)))
        res_df.to_csv("./diff.csv", index=False, encoding='utf-8')
    return len(res_df) == 0
   
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare source file and dest file content')
    parser.add_argument("--source", dest="source", type=str, help="Source file path" )
    parser.add_argument("--source_col", dest="source_col", type=str, help="Source file path" )
    parser.add_argument("--dest", dest="dest", type=str, help="Destination file path")
    parser.add_argument("--dest_col", dest="dest_col", type=str, help="The destination column name")
    
    args = parser.parse_args()
    source_ = args.source
    source_col = args.source_col
    dest_ = args.dest
    dest_col = args.dest_col
    
    res = compare(source_, source_col, dest_, dest_col)
    if res is True:
        print("Compare successfully, source is equal to dest")
    else:
        print("Compare failure, source is not equal to dest")
      