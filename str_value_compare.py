import pandas as pd
import argparse
import xml.etree.ElementTree as ET
import copy

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
            for text_piece in it:
                value += text_piece
            data_list.append([child.get('name'), value])
    return data_list
    
def compare(source_, dest_):
    source_data_list = parse_xml(source_)
    # TODO: Fake replace here with how to read dest data list
    dest_data_list  = copy.deepcopy(source_data_list)
    df_source = pd.DataFrame(data=source_data_list, columns=["name", "value_source"])
    df_dest = pd.DataFrame(data=dest_data_list, columns=["name", "value_dest"])
    
    df_cmp = df_source.merge(df_dest, on="name", how="inner", left_index=False, right_index=False)
    res_df = df_cmp[df_cmp["value_source"] != df_cmp["value_dest"]]
    print(res_df.head())
    return len(res_df) == 0
   
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare source file and dest file content')
    parser.add_argument("--source", dest="source", type=str, help="Source file path" )
    parser.add_argument("--dest", dest="dest", type=str, help="Destination file path")
    
    args = parser.parse_args()
    source_ = args.source
    dest_ = args.dest
    
    res = compare(source_, dest_)
    if res is True:
        print("Compare successfully, source is equal to dest")
    else:
        print("Compare failure, source is not equal to dest")
      