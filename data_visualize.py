import pandas as pd


class data_ :

    def read_file(self, filepath) :
        if str(filepath) == '':
            return ''
        
        else:
            return pd.read_csv(str(filepath), index_col=False)
    

    def get_column_list(self, df) :
        # print (df.columns) #-> dtype:object라서 아래과정 진행
        
        # 리스트로 return 받기위한 과정
        columnname_list = []
        for i in df.columns :
            columnname_list.append(i)
        self.column_arr = columnname_list
        return columnname_list
    
    
