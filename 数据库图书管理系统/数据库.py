from PyQt5.QtWidgets import QListWidget, QApplication, QLineEdit, QWidget, QFormLayout, QPushButton
import sys
import psycopg2
from PyQt5 import QtCore
from PyQt5.Qt import *
import datetime


class lineEditDemo(QWidget):

    def ButtonSearchClicked(self, PList1, PEdit1, Username, Passward, way):
        PList1.clear()
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")

        if gConn:
            print("connected")

        if way == '按ISBN查询':
            way = 'ISBN'
        elif way == '按书名查询':
            way = '书名'
        elif way == "按出版社查询":
            way = '出版社'
        elif way == "按作者查询":
            way = '作者'
        elif way == "按图书分类查询":
            way = '图书分类'
        elif way == "按出版年份查询":
            way = '出版年份'
        cur = gConn.cursor()
        str1 = PEdit1.text()
        a = str1.split(',')
        if way == '查询所有':
            cur.execute(f"""select * from course order by "ISBN" asc""")
        else:
            cur.execute(f"""select * from course where "{way}"='{a[0]}' order by "ISBN" asc""")

        rows = cur.fetchall()
        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(
                row[4]) + ", " + str(row[5]))

        cur.close()
        gConn.close()

    def PButtonInsertClicked(self, PList1, List1, Username, Passward):
        PList1.clear()
        print("开始")
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        cur = gConn.cursor()
        str = List1.text()
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

    def ButtonDeleteHaveClicked(self, PList1, PEdit1, Username, Passward):
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
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

    def ButtonUpdateClicked(self, PList1, PEdit1, Username, Passward, way, str2):
        PList1.clear()
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        if way == '更改ISBN':
            way = 'ISBN'
        elif way == '更改书名':
            way = '书名'
        elif way == "更改出版社":
            way = '出版社'
        elif way == "更改作者":
            way = '作者'
        elif way == "更改图书分类":
            way = '图书分类'
        elif way == "更改出版年份":
            way = '出版年份'
        cur = gConn.cursor()

        str1 = PEdit1.text()
        a = str2.split(',')
        cur.execute(f"""update course set "{way}"='{str1}' where "ISBN"='{a[0]}'""")
        cur.execute(f"""select * from course order by "ISBN" asc""")
        rows = cur.fetchall()

        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(
                row[4]) + ", " + str(row[5]))

        cur.close()
        gConn.close()

    def ButtonQuitClicked(self, PList1, PEdit1):
        app1.quit()

    def __init__(self, username, passward, parent=None):
        super(lineEditDemo, self).__init__(parent)

        self.setWindowTitle('PyQT5使用')
        self.resize(400, 600)
        self.way = 0
        # 实例化表单布局
        flo = QFormLayout()
        self.str = 0
        # 创建4个文本输入框
        PNormalLineEdit = QLineEdit()
        PList = QListWidget()
        PList.setResizeMode(1)
        PButtonSearch = QPushButton('查询已有')
        menu = QMenu(self)
        menu.addAction(QAction("查询所有", self))
        menu.addSeparator()
        menu.addAction("按ISBN查询")
        menu.addSeparator()
        menu.addAction("按书名查询")
        menu.addSeparator()
        menu.addAction("按出版社查询")
        menu.addSeparator()
        menu.addAction("按作者查询")
        menu.addSeparator()
        menu.addAction("按图书分类查询")
        menu.addSeparator()
        menu.addAction("按出版年份查询")
        PButtonSearch.setMenu(menu)
        menu.triggered[QAction].connect(self.processtrigger)
        menu.triggered.connect(lambda: self.ButtonSearchClicked(PList, PNormalLineEdit, username, passward, self.way))

        PList.itemClicked.connect(lambda: self.item(PList))
        PButtonInsert = QPushButton('插入上述')
        PButtonUpdate = QPushButton('更新数据')
        menu1 = QMenu(self)
        menu1.addAction("更改ISBN")
        menu1.addSeparator()
        menu1.addAction("更改书名")
        menu1.addSeparator()
        menu1.addAction("更改出版社")
        menu1.addSeparator()
        menu1.addAction("更改作者")
        menu1.addSeparator()
        menu1.addAction("更改图书分类")
        menu1.addSeparator()
        menu1.addAction("更改出版年份")
        PButtonUpdate.setMenu(menu1)
        menu1.triggered[QAction].connect(self.processtrigger)

        menu1.triggered.connect(
            lambda: self.ButtonUpdateClicked(PList, PNormalLineEdit, username, passward, self.way, self.str))
        PButtonDeleteHave = QPushButton('删除选择')
        PButtonQuit = QPushButton('退出程序')

        # PButtonSearch.clicked.connect(lambda: self.ButtonSearchClicked(PList, PNormalLineEdit, username, passward))
        PButtonInsert.clicked.connect(lambda: self.PButtonInsertClicked(PList, PNormalLineEdit, username, passward))
        PButtonDeleteHave.clicked.connect(
            lambda: self.ButtonDeleteHaveClicked(PList, PNormalLineEdit, username, passward))
        PButtonQuit.clicked.connect(lambda: self.ButtonQuitClicked(PList, PNormalLineEdit))

        flo.addRow(' ', PNormalLineEdit)
        flo.addRow(' ', PButtonInsert)
        flo.addRow(' ', PButtonUpdate)
        flo.addRow(' ', PButtonSearch)
        flo.addRow(' ', PButtonDeleteHave)
        flo.addRow(' ', PList)
        flo.addRow(' ', PButtonQuit)
        # 设置setPlaceholderText()文本框浮现的文字
        PNormalLineEdit.setPlaceholderText('')

        # setEchoMode()：设置显示效果

        # QLineEdit.Normal：正常显示所输入的字符，此为默认选项
        PNormalLineEdit.setEchoMode(QLineEdit.Normal)

        # 设置窗口的布局
        self.setLayout(flo)

        def resizeEvent(self, e):
            self.PList.height = self.flo.height - 20

    def processtrigger(self, q):
        self.way = q.text()

    def item(self, PList2):
        self.str = PList2.currentItem().text()


class User(QWidget):

    def ButtonSearchClicked(self, PList1, PEdit1, Username, Passward, way):
        PList1.clear()
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")

        if gConn:
            print("connected")

        if way == '按ISBN查询':
            way = 'ISBN'
        elif way == '按书名查询':
            way = '书名'
        elif way == "按出版社查询":
            way = '出版社'
        elif way == "按作者查询":
            way = '作者'
        elif way == "按图书分类查询":
            way = '图书分类'
        elif way == "按出版年份查询":
            way = '出版年份'
        cur = gConn.cursor()
        str1 = PEdit1.text()
        a = str1.split(',')
        if way == '查询所有':
            cur.execute(f"""select * from course order by "ISBN" asc""")
        else:
            cur.execute(f"""select * from course where "{way}"='{a[0]}' order by "ISBN" asc""")

        rows = cur.fetchall()
        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(
                row[4]) + ", " + str(row[5]))

        cur.close()
        gConn.close()

    def PButtonBorrowClicked(self, PList1, List1, Username, Passward, user):
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        cur = gConn.cursor()
        str1 = PList1.currentItem().text()
        b = str1.split(',')

        cur.execute(f"""select * from borrow where "借书人"='{Username}'""")
        rows = cur.fetchall()
        num = 0
        for row in rows:
            num = num + 1

        if (user == '校外登录' and num == 2) or (user == '校内登录' and num == 5):
            PList1.clear()
            PList1.addItem('您已达借书上限')
        else:
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d'))
            try:
                cur.execute(
                    f"INSERT INTO public.borrow VALUES ('{b[0]}', '{b[1]}', '{now.strftime('%Y-%m-%d')}', '0', '{Username}')")
            except:
                PList1.clear()
                PList1.addItem(f'重复键违反唯一约束"borrow_pkey"DETAIL:  键值"(number)=({b[0]})" 已经存在')
            else:
                PList1.clear()
                PList1.addItem('借书成功')
            cur.close()
            gConn.close()

    def ButtonDeleteHaveClicked(self, PList1, PEdit1, Username, Passward):
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")

        cur = gConn.cursor()
        str1 = PList1.currentItem().text()
        a = str1.split(',')

        cur.execute(f"""delete from borrow where "所借书的ISBN"='{a[0]}'""")
        cur.execute(f"""select * from borrow order by "所借书的ISBN" asc""")

        rows = cur.fetchall()
        print(rows)
        PList1.clear()
        for row in rows:
            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + "元")

        cur.close()
        gConn.close()

    def ButtonHave(self, PList1, PEdit1, Username, Passward, user):
        PList1.clear()
        gConn = psycopg2.connect(host="127.0.0.1", port="5432", user=Username, password=Passward, database="test")
        gConn.autocommit = 'Ture'
        if gConn:
            print("connected")
        cur = gConn.cursor()

        cur.execute(f"""select * from borrow where "借书人"='{Username}' order by "所借书的ISBN" asc""")

        rows = cur.fetchall()

        for row in rows:
            day = row[2].split('-')
            data = int(day[2])
            now = datetime.datetime.now()
            now1 = int(now.strftime('%d'))

            if user == '校内登录':
                a = str((now1 - data) * 1)
            else:
                a = str((now1 - data) * 3)

            PList1.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(a) + "元")
            cur.execute(
                f"""update borrow set "所需费用"='{a}' where "所借书的ISBN"='{row[0]}' and "借书人"='{Username}'""")

        cur.close()
        gConn.close()

    def ButtonQuitClicked(self, PList1, PEdit1):

        app1.quit()

    def __init__(self, username, passward, user, parent=None):
        super(User, self).__init__(parent)
        self.way = 0
        self.setWindowTitle('PyQT5使用')
        self.resize(400, 600)
        # 实例化表单布局
        flo = QFormLayout()

        # 创建4个文本输入框
        PNormalLineEdit = QLineEdit()
        PButtonSearch = QPushButton('查询已有')
        menu = QMenu(self)
        menu.addAction(QAction("查询所有", self))
        menu.addSeparator()
        menu.addAction("按ISBN查询")
        menu.addSeparator()
        menu.addAction("按书名查询")
        menu.addSeparator()
        menu.addAction("按出版社查询")
        menu.addSeparator()
        menu.addAction("按作者查询")
        menu.addSeparator()
        menu.addAction("按图书分类查询")
        menu.addSeparator()
        menu.addAction("按出版年份查询")
        PButtonSearch.setMenu(menu)

        menu.triggered[QAction].connect(self.processtrigger)
        menu.triggered.connect(lambda: self.ButtonSearchClicked(PList, PNormalLineEdit, username, passward, self.way))
        PButtonBorrow = QPushButton('借阅书籍')
        PButtonDeleteHave = QPushButton('还书')
        PButtonHave = QPushButton('查询借书情况')
        PButtonQuit = QPushButton('退出程序')

        PList = QListWidget()
        PList.setResizeMode(1)

        # PButtonSearch.clicked.connect(lambda: self.ButtonSearchClicked(PList, PNormalLineEdit, username, passward))
        PButtonBorrow.clicked.connect(
            lambda: self.PButtonBorrowClicked(PList, PNormalLineEdit, username, passward, user))
        PButtonDeleteHave.clicked.connect(
            lambda: self.ButtonDeleteHaveClicked(PList, PNormalLineEdit, username, passward))
        PButtonQuit.clicked.connect(lambda: self.ButtonQuitClicked(PList, PNormalLineEdit))
        PButtonHave.clicked.connect(lambda: self.ButtonHave(PList, PNormalLineEdit, username, passward, user))

        flo.addRow('', PNormalLineEdit)
        flo.addRow('', PButtonBorrow)
        flo.addRow('', PButtonSearch)
        flo.addRow('', PButtonHave)
        flo.addRow('', PButtonDeleteHave)
        flo.addRow('', PList)
        flo.addRow('', PButtonQuit)
        # 设置setPlaceholderText()文本框浮现的文字
        PNormalLineEdit.setPlaceholderText('')

        # setEchoMode()：设置显示效果

        # QLineEdit.Normal：正常显示所输入的字符，此为默认选项
        PNormalLineEdit.setEchoMode(QLineEdit.Normal)

        # 设置窗口的布局
        self.setLayout(flo)

        def resizeEvent(self, e):
            self.PList.height = self.flo.height - 20

    def processtrigger(self, q):
        self.way = q.text()


class landing(QWidget):
    def __init__(self, parent=None):
        super(landing, self).__init__(parent)

        self.setWindowTitle('登录')
        self.resize(360, 360)
        self.way = 0
        self.username = 0
        self.passward = 0
        # 实例化表单布局
        flo = QFormLayout()

        le1 = QLineEdit(self)
        le1.setGeometry(QtCore.QRect(0, 0, 160, 20))
        le1.move(100, 100)
        le1.setToolTip('请输入用户名')
        le1.setPlaceholderText('请输入用户名')

        le2 = QLineEdit(self)
        le2.setGeometry(QtCore.QRect(0, 0, 160, 20))
        le2.move(100, 150)
        le2.setEchoMode(QLineEdit.Password)  # 设置显示模式
        le2.setToolTip('请输入密码')  # 设置显示提示框
        le2.setPlaceholderText('请输入密码')  # 设置显示默认占位字符
        le2.setClearButtonEnabled(True)
        le1.returnPressed.connect(le2.setFocus)
        action = QAction(le2)

        def change():
            if le2.echoMode() == QLineEdit.Normal:
                le2.setEchoMode(QLineEdit.Password)
                action.setIcon(QIcon('0.png'))
            else:
                le2.setEchoMode(QLineEdit.Normal)
                action.setIcon(QIcon('1.png'))

        def have():
            if len(le2.text()) > 0 and le2.echoMode() == QLineEdit.Password:
                action.setIcon(QIcon('0.png'))
            # else:
            #     action.setIcon(QIcon('1.png'))

        le2.textChanged.connect(have)
        action.triggered.connect(change)
        le2.addAction(action, QLineEdit.TrailingPosition)
        # 添加操作行为END

        btnu = QPushButton(self)
        btnu.setGeometry(QtCore.QRect(0, 0, 80, 20))
        btnu.move(100, 200)
        btnu.setText('登陆方式')
        menu = QMenu(self)
        menu.addAction(QAction("校内登录", self))
        menu.addSeparator()
        menu.addAction("校外登录")
        menu.addSeparator()
        menu.addAction("管理登录")
        btnu.setMenu(menu)

        def change():
            btnu.setText(self.way)

        menu.triggered[QAction].connect(self.processtrigger)
        menu.triggered.connect(change)
        btn = QPushButton(self)
        btn.setGeometry(QtCore.QRect(0, 0, 60, 20))
        btn.move(200, 200)
        btn.setText('提交')
        btn.setEnabled(False)

        # 设置BUTTON的有效性START
        def en_dis():
            if len(le1.text()) > 0 and len(le2.text()) > 0:
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)

        le1.textChanged.connect(en_dis)
        le2.textChanged.connect(en_dis)

        # 设置BUTTON的有效性END
        def fuzhi():
            self.username = le1.text()
            self.passward = le2.text()

        btn.clicked.connect(fuzhi)
        btn.clicked.connect(lambda: self.seconds())

        self.setLayout(flo)

        def resizeEvent(self, e):
            self.PList.height = self.flo.height - 20

    def processtrigger(self, q):
        self.way = q.text()

    def seconds(self):
        if self.way == '管理登录':
            self.win = lineEditDemo(self.username, self.passward)
            self.win.show()

        else:
            self.win = User(self.username, self.passward, self.way)
            self.win.show()


if __name__ == '__main__':

    if not QApplication.instance():
        app1 = QApplication(sys.argv)
    else:
        app1 = QApplication.instance()
    win1 = landing()
    win1.show()
    sys.exit(app1.exec_())
