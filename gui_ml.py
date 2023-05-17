
from PyQt5.QtWidgets import *
import sys, pickle
import pandas as pd

from PyQt5 import uic, QtWidgets, QtCore, QtGui

import data_visualize, table_display

class UI(QMainWindow):
    def __init__(self) : 
        super(UI, self).__init__()  # 자기자신(UI) 상속 받기
        uic.loadUi('./mainwindow.ui', self)

        global data
        data = data_visualize.data_()
        self.show()
        
        # 등록
        self.Browse = self.findChild(QPushButton,'Browse')
        self.column_list = self.findChild(QListWidget, 'column_list')
        self.Submit_btn = self.findChild(QPushButton,'Submit')
        self.target_col = self.findChild(QLabel,'target_col')
        self.tabel = self.findChild(QTableView,'tableView')
        self.data_shape = self.findChild(QLabel,'shape')

        self.scaler = self.findChild(QComboBox,'scaler')
        self.scale_btn = self.findChild(QPushButton,'scale_btn')

        self.cat_column = self.findChild(QComboBox,'cat_column')
        self.convert_btn = self.findChild(QPushButton,'convert_btn')

        self.drop_column = self.findChild(QComboBox,'drop_column')
        self.drop_btn = self.findChild(QPushButton,'drop_btn')

        self.empty_column = self.findChild(QComboBox,'empty_column')
        self.fill_mean_btn = self.findChild(QPushButton,'fill_mean_btn')
        self.fillna_btn = self.findChild(QPushButton,'fillna_btn')

        # Click -> 이벤트 (함수 연결해서 호출)
        self.Browse.clicked.connect(self.getCSV)
        self.Submit_btn.clicked.connect(self.set_target)
        self.column_list.clicked.connect(self.target)

    def set_target(self) :
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
        
    def fill_combo_box(self) :
        x = table_display.DataFrameModel(self.df)
        self.tabel.setModel(x)

    def filldetails(self, flag=1) :
        if flag == 0:
            self.df =data.read_file(self.filepath)
        
        self.column_list.clear()

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
        self.fill_combo_box()
        

# python을 이용해서 파일 실행시킬 때, 가장 먼저 실행시키고 싶다면 아래방식으로 if
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = UI()

    app.exec_() # 이벤트 루프 실행 -> 종료될 때 까지 실행