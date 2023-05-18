import pandas as pd
from sklearn.preprocessing \
    import LabelEncoder, StandardScaler, MinMaxScaler, PowerTransformer
import matplotlib.pyplot as plt


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
    
    def get_cat(self,df) :
        cat_col=[x for x in df.columns if df[x].dtype=='object']
        # cat_col = []
        # for i in df.columns :
        #     if (df[i].dtype == 'object') :
        #         cat_col.append(i)
        return cat_col


    def convert_category(self, df, column_name) :
        le = LabelEncoder()
        df[column_name] = le.fit_transform(df[column_name])
        return df[column_name]
    

    def drop_columns(self, df, column_name) :
        return df.drop(column_name, axis =1)


    def get_empty_list(self, df) :
        empty_list = [x for x in df.columns if df[x].isnull().values.any()]
        return empty_list
    
    def fillmean(self, df, column_name) :
        df[column_name].fillna(df[column_name].mean(), inplace = True)
        return df[column_name] 

    def fillnan(self, df, column_name) :
        df[column_name].fillna('Unknown', inplace = True)
        return df[column_name]
    
    def StandardScaler(self, df, target_name) : 
        sc = StandardScaler()
        x = df.drop(target_name, axis=1)
        scaled_features = sc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features,
                                          index = x.index,
                                          columns=x.columns)
        scaled_features_df[target_name] = df[target_name]
        return scaled_features_df

    def MinMaxScaler(self, df, target_name) : 
        mc = MinMaxScaler()
        x = df.drop(target_name, axis=1)
        scaled_features = mc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features,
                                          index = x.index,
                                          columns=x.columns)
        scaled_features_df[target_name] = df[target_name]
        return scaled_features_df

    def PowerScaler(self, df, target_name) : 
        pc = PowerTransformer()
        x = df.drop(target_name, axis=1)
        scaled_features = pc.fit_transform(x)
        scaled_features_df = pd.DataFrame(scaled_features,
                                          index = x.index,
                                          columns=x.columns)
        scaled_features_df[target_name] = df[target_name]
        return scaled_features_df
        
    def scatter_graph(self, df, x, y, c, mark) :
        plt.figure()
        plt.scatter(df[x], df[y], c=c, marker=mark)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{y} vs {x}')
        plt.show()

    def line_graph(self, df, x, y, c, mark) :
        df = df.sort_values(by=[x])
        plt.figure()
        plt.plot(df[x], df[y], c=c, marker=mark)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{y} vs {x}')
        plt.show()


