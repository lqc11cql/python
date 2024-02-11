# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidget,QApplication,QLineEdit,QWidget,QFormLayout,QPushButton
import sys
import psycopg2

class lineEditDemo(QWidget):
    
    
    def ButtonSearchClicked(self,PList1,PEdit1):
        PList1.clear()
        gConn = psycopg2.connect(host="127.0.0.1", port="54321", user="system", password = "123456", database ="test")

        if gConn:
            print("connected")
        
        cur = gConn.cursor()
        cur.execute("select * from course")
        rows = cur.fetchall()
        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]))
        cur.close()

        gConn.close()
                
    def PButtonInsertClicked(self,PList1,PEdit1):
        PList1.clear()
        print("开始")
        gConn = psycopg2.connect(host="127.0.0.1", port="54321", user="system", password = "123456", database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        cur = gConn.cursor()
        str = PEdit1.text()
        row = str.split(',')
        for i in row:
            print(i)
        try:
            cur.execute(
                f"INSERT INTO public.course VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}')")
        except:
            PList1.addItem(f'重复键违反唯一约束"course_pkey"DETAIL:  键值"(number)=({row[0]})" 已经存在')
            PList1.addItem(cur.statusmessage)
        else:
            PList1.addItem('插入成功')
        cur.close()
        gConn.close()

  
        
    def ButtonDeleteHaveClicked(self,PList1,PEdit1):
        gConn = psycopg2.connect(host="127.0.0.1", port="54321", user="system", password = "123456", database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        cur = gConn.cursor()
        str1 = PList1.currentItem().text()
        a = str1.split(',')

        cur.execute(f"""delete from course where "ISBN"='{a[0]}'""")
        cur.execute(f"""select * from course order by "ISBN" asc""")

        rows = cur.fetchall()

        PList1.clear()
        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(
                row[4]) + ", " + str(row[5]))

        cur.close()
        gConn.close()


    def ButtonQuitClicked(self,PList1,PEdit1):

        app.quit()

        
    def __init__(self,parent=None):
        super(lineEditDemo, self).__init__(parent)
        self.setWindowTitle('PyQT5使用')
        self.resize(1840, 950)  

        #实例化表单布局
        flo=QFormLayout()

        #创建4个文本输入框
        PNormalLineEdit=QLineEdit()
        PButtonSearch=QPushButton('查询已有')


        PButtonInsert=QPushButton('插入上述')

        PButtonDeleteHave=QPushButton('删除选择')
        PButtonQuit=QPushButton('退出程序')
        
        PList=QListWidget()
        PList.setResizeMode(1);
        PButtonSearch.clicked.connect(lambda: self.ButtonSearchClicked(PList,PNormalLineEdit)) 
        PButtonInsert.clicked.connect(lambda: self.PButtonInsertClicked(PList,PNormalLineEdit)) 

        PButtonDeleteHave.clicked.connect(lambda: self.ButtonDeleteHaveClicked(PList,PNormalLineEdit)) 
        PButtonQuit.clicked.connect(lambda: self.ButtonQuitClicked(PList,PNormalLineEdit)) 


        #添加到表单布局中
        #flo.addRow(文本名称（可以自定义），文本框)
        flo.addRow('按顺序输入待插入记录（以英文逗号间隔）',PNormalLineEdit)
        flo.addRow('请点击插入上述记录',PButtonInsert)
        flo.addRow('请点击查询已有记录',PButtonSearch)
        flo.addRow('消息列表',PList)
        flo.addRow('请选中一行，点击删除该记录',PButtonDeleteHave)


        #设置setPlaceholderText()文本框浮现的文字
        PNormalLineEdit.setPlaceholderText('')

        #setEchoMode()：设置显示效果

        #QLineEdit.Normal：正常显示所输入的字符，此为默认选项
        PNormalLineEdit.setEchoMode(QLineEdit.Normal)

        #设置窗口的布局
        self.setLayout(flo)
        

        
        def resizeEvent(self, e):
            self.PList.height = self.flo.height -20
            
        
            

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    win=lineEditDemo()
    win.show()

    sys.exit(app.exec_())








