
from PyQt5.QtWidgets import *
import sys, pickle
import pandas as pd


from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap

import data_visualize, table_display
import Linear_Regression, SVM, Logistic_Regression, Random_Forest

class UI(QMainWindow):
    def __init__(self) : 
        super(UI, self).__init__()  # 자기자신(UI) 상속 받기
        uic.loadUi('./mainwindow.ui', self)

        # self.setWindowTitle("이미지 표시")
        # self.label1 = QLabel(self)
        # image_path = "./rainbowbonobono.jpg"
        # pixmap = QPixmap(image_path)
        # self.label1.setPixmap(pixmap)
        # self.resize(pixmap.width(), pixmap.height())

        global data
        data = data_visualize.data_()
        self.show()
        self.target_value = ''

        
        # 등록
        self.Browse = self.findChild(QPushButton,'Browse')
        self.column_list = self.findChild(QListWidget, 'column_list')
        self.Submit_btn = self.findChild(QPushButton,'Submit')
        self.target_col = self.findChild(QLabel,'target_col')
        self.tabel = self.findChild(QTableView,'tableView')
        self.data_shape = self.findChild(QLabel,'shape')
        self.notarget_alarm = self.findChild(QLabel,'notarget_alarm')

        self.scaler = self.findChild(QComboBox,'scaler')
        self.scale_btn = self.findChild(QPushButton,'scale_btn')

        self.cat_column = self.findChild(QComboBox,'cat_column')
        self.convert_btn = self.findChild(QPushButton,'convert_btn')

        self.drop_column = self.findChild(QComboBox,'drop_column')
        self.drop_btn = self.findChild(QPushButton,'drop_btn')

        self.empty_column = self.findChild(QComboBox,'empty_column')
        self.fill_mean_btn = self.findChild(QPushButton,'fill_mean_btn')
        self.fillna_btn = self.findChild(QPushButton,'fillna_btn')

            # scatterplot 등록
        self.scatter_x = self.findChild(QComboBox,'scatter_x')
        self.scatter_y = self.findChild(QComboBox,'scatter_y')
        self.scatter_c = self.findChild(QComboBox,'scatter_c')
        self.scatter_mark = self.findChild(QComboBox,'scatter_mark')
        self.scatterplot = self.findChild(QPushButton,"scatterplot")

            # lineplot 등록
        self.plot_x = self.findChild(QComboBox,'plot_x')
        self.plot_y = self.findChild(QComboBox,'plot_y')
        self.plot_c = self.findChild(QComboBox,'plot_c')
        self.plot_mark = self.findChild(QComboBox,'plot_mark')
        self.lineplot = self.findChild(QPushButton,"lineplot")

            # Model Training
        self.model_select = self.findChild(QComboBox,'model_select')
        self.train = self.findChild(QPushButton,'train')



        # Click -> 이벤트 (함수 연결해서 호출)
        self.Browse.clicked.connect(self.getCSV)
        self.Submit_btn.clicked.connect(self.set_target)
        self.column_list.clicked.connect(self.target)
        self.convert_btn.clicked.connect(self.convert_cat)
        self.drop_btn.clicked.connect(self.dropc)
        self.fill_mean_btn.clicked.connect(self.fillme)
        self.fillna_btn.clicked.connect(self.fillna)
        self.scale_btn.clicked.connect(self.scale_value)
            # 시각화 Show
        self.scatterplot.clicked.connect(self.scatter_plot)
        self.lineplot.clicked.connect(self.line_plot)
            # Training btn
        self.train.clicked.connect(self.train_func)

    def train_func(self) :
        my_dict = {'Linear Regression' : Linear_Regression,
                   'SVM' : SVM,
                   'Logistic Regression' : Logistic_Regression,
                   'Random Forest' : Random_Forest}
        if self.target_value != '' :
            name = self.model_select.currentText()
            self.win = my_dict[name].UI(self.df, self.target_value)

        

    def line_plot(self) :
        x = self.plot_x.currentText()
        y = self.plot_y.currentText()
        c = self.plot_c.currentText()
        mark = self.plot_mark.currentText()
        data.line_graph(df=self.df, x=x, y=y, c=c, mark=mark)

    def scatter_plot(self) :
        x = self.scatter_x.currentText()
        y = self.scatter_y.currentText()
        c = self.scatter_c.currentText()
        mark = self.scatter_mark.currentText()
        data.scatter_graph(df=self.df, x=x, y=y, c=c, mark=mark)


    def scale_value(self) :
        if self.scaler.currentText() == 'StandardScaler' :
            self.df = data.StandardScaler(self.df, self.target_value)

        elif self.scaler.currentText() == 'MinMaxScaler' :
            self.df = data.MinMaxScaler(self.df, self.target_value)

        elif self.scaler.currentText() == 'PowerScaler' :
            self.df = data.PowerScaler(self.df, self.target_value)

        self.filldetails()

    def fillna(self) :
        name = self.empty_column.currentText()
        self.df[name] = data.fillnan(self.df, name)
        self.filldetails()



    def fillme(self) :
        name = self.empty_column.currentText()
        self.df[name] = data.fillmean(self.df, name)
        self.filldetails()

    def dropc(self) :
        name = self.drop_column.currentText()
        if self.target_value == '':
            self.notarget_alarm.setText('!!Plz SetTarget!!')
        else :
            if (name == self.target_value) : 
                pass
            
            else :
                self.df = data.drop_columns(self.df, name)
                self.filldetails()
                
    

    def convert_cat(self) :
        name = self.cat_column.currentText()
        self.df[name] = data.convert_category(self.df, name)
        self.filldetails()

    def set_target(self) :
        self.notarget_alarm.setText('')
        self.target_value = str(self.item).split()[0]
        print(self.target_value)
        self.target_col.setText(self.target_value)
        
    def target(self):
        # 클릭한 데이터 저장
        self.item = self.column_list.currentItem().text()
        print(self.item)

    def getCSV(self):
        # 파일 처음 열때 뜨는 문자열, 기본 경로,  
        self.filepath, _ =QFileDialog.getOpenFileName(self,
                                                      'Open File',
                                                      'C:/apps/ml_7/ML_ubion/datasets',
                                                      'csv(*.csv)')
        # print(self.filepath)
        self.column_list.clear()
        # self.column_list.addItems(['Browse', 'Brazil', 'WorldCup'])
        self.filldetails(0)

        self.notarget_alarm.setText('No Target')
        
    def fill_combo_box(self) :
        
        self.cat_column.clear()
        self.cat_column.addItems(self.cat_col_list)
        
        self.drop_column.clear()
        self.drop_column.addItems(self.column_arr)
        
        self.empty_column.clear()
        self.empty_column.addItems(self.empty_column_name)

        self.scatter_x.clear()
        self.scatter_x.addItems(self.column_arr)
        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_arr)

        self.plot_x.clear()
        self.plot_x.addItems(self.column_arr)
        self.plot_y.clear()
        self.plot_y.addItems(self.column_arr)

        x = table_display.DataFrameModel(self.df)
        self.tabel.setModel(x)
        

    def filldetails(self, flag=1) :
        if flag == 0:
            self.df =data.read_file(self.filepath)
        
        self.column_list.clear()
        self.empty_column_name = data.get_empty_list(self.df)

        if len(self.df) == 0 :
            pass
        else :
            self.column_arr = data.get_column_list(self.df)
            # print(self.column_arr)
            for i, j in enumerate(self.column_arr) :
                stri = f'{j} ------- {str(self.df[j].dtype)}'
                self.column_list.insertItem(i, stri)
        df_shape = f'Shape -> rows : {self.df.shape[0]}, columns : {self.df.shape[1]}'
        self.data_shape.setText(df_shape)

        self.cat_col_list = data.get_cat(self.df)
        self.fill_combo_box()
            

# python을 이용해서 파일 실행시킬 때, 가장 먼저 실행시키고 싶다면 아래방식으로 if
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = UI()

    # window.show()

    app.exec_() # 이벤트 루프 실행 -> 종료될 때 까지 실행