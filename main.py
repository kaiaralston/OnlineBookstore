import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMessageBox
import pandas as pd
from PyQt5.QtWidgets import *

##### welcome screen ######
class loginScreen(QMainWindow):
    def __init__(self):
        super(loginScreen, self).__init__()
        uic.loadUi("welcomePage.ui", self)
        self.AloginButton.clicked.connect(self.AdminLogin)
        self.loginButton.clicked.connect(self.UserLogin)
        self.signUpButton.clicked.connect(self.SignUp)

    def AdminLogin(self):
        login = AdminLoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def UserLogin(self):
        ulogin = UserLoginScreen()
        widget.addWidget(ulogin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def SignUp(self):
        signUp = SignUpScreen()
        widget.addWidget(signUp)
        widget.setCurrentIndex(widget.currentIndex()+1)

###### log in as admin ######
class AdminLoginScreen(QMainWindow):
    def __init__(self):
        super(AdminLoginScreen, self).__init__()
        uic.loadUi("AdminLogin.ui", self)
        self.ApassField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backFromAdmin.clicked.connect(self.backFunc)
        self.AdminLoginButton.clicked.connect(self.AdminLoginFunc)

    def backFunc(self):
        back = loginScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def AdminLoginFunc(self):
        Auser = self.AemailField.text()
        Apass = self.ApassField.text()

        if len(Auser) == 0 or len(Apass) == 0:
            self.invalid.setText("Please fill in required fields")
        elif Auser == str("ADMIN@ADMIN.com") and Apass == str("ADMIN"):
            #self.AdminLoginButton.clicked.connect(self.loggedIn)
            self.loggedIn()
        else:
            self.invalid.setText("Invalid username or password")
            self.invalid_2.setText("Must have Admin account to log in here.")

    def loggedIn(self):
        next = AdminMain()
        widget.addWidget(next)
        widget.setCurrentIndex(widget.currentIndex() + 1)


######## log in as User #########
class UserLoginScreen(QMainWindow):
    def __init__(self):
        super(UserLoginScreen, self).__init__()
        uic.loadUi("UserLogin.ui", self)
        self.passField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userLoginButton.clicked.connect(self.UserLoginFunc)
        self.backFromUser.clicked.connect(self.backFunc)
        #self.logins = pd.read_excel('final_project_excel.xlsx', sheet_name='users')
        self.df_users = pd.read_excel("logins.xlsx", sheet_name='users')

    def backFunc(self):
        back = loginScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def UserLoginFunc(self):
        user = self.emailField.text()
        userPass = self.passField.text()

        user_confirm = self.df_users[self.df_users['username'] == self.emailField.text()]

        if len(user) == 0 or len(userPass) == 0:
            self.invalid.setText("Please fill in required fields")
        elif user_confirm.empty or user_confirm.iloc[0]['password'] != self.passField.text():
            self.invalid.setText("Invalid username or password")
        elif user_confirm.iloc[0]['password'] == self.passField.text():
            self.loggedIn()

    def loggedIn(self):
        next = UserBooks()
        widget.addWidget(next)
        widget.setCurrentIndex(widget.currentIndex() + 1)



######### shopping as user #######
class clickedBook(QMainWindow):
    def __init__(self, parent, id):
        super(clickedBook, self).__init__()
        uic.loadUi("UserClickBook.ui", self)
        self.backButton.clicked.connect(self.backFunc)

        self.id = id
        self.parent = parent
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')
        self.orderNow.clicked.connect(self.add2Cart)

        self.book = self.df_books.loc[self.df_books.id == id].reset_index()

        self.titleDisp.setText(str(self.book.title[0]))
        self.authorDisp.setText(str(self.book.author[0]))
        self.stockDisp.setText(str(self.book.number[0]))
        self.priceDisp.setText(str(self.book.price[0]))

        self.cover_path = str(self.book.cover[0])
        self.book_photo.setPixmap(QPixmap(self.cover_path))

        self.show()

    def backFunc(self):
        back = UserBooks()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add2Cart(self):
        price = self.priceDisp.text()
        buy = ordering(self.id, price)
        widget.addWidget(buy)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ordering(QMainWindow):
    def __init__(self, id, price):
        super(ordering, self).__init__()
        uic.loadUi("orderNow.ui", self)
        self.df_orders = pd.read_excel('orders.xlsx', sheet_name='orders')

        self.price = price
        self.id = id

        self.backButton.clicked.connect(self.backFunc)
        self.placeOrder_btn.clicked.connect(self.placeOrder)

    def placeOrder(self):
        email = self.emailLe.text()
        date = self.dateLe.text()

        comfirm = QMessageBox()
        comfirm.setWindowTitle('Are you sure you want to order this book?')
        comfirm.setText('Order has been placed.')
        comfirm.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = comfirm.exec()
        if res == QMessageBox.Ok:
            self.df_orders.loc[len(self.df_orders.index)] = [self.df_orders.id.max() + 1, self.id, email, date, self.price]
            self.df_orders.to_excel('orders.xlsx', sheet_name='orders', index=False)
            self.backFunc()
        elif res == QMessageBox.Cancel:
            comfirm.close()


    def backFunc(self):
        back = UserBooks()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserBooks(QMainWindow):
    def __init__(self):
        super(UserBooks, self).__init__()
        uic.loadUi('UserBooks.ui', self)

        self.row_length = 7

        self.backButton.clicked.connect(self.signOutFunc)

        self.show()
        self.load_book_data()

    def load_book_data(self):
        while self.layout_books.count():
            self.layout_books.itemAt(0).widget().setParent(None)
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')
        # searchText = self.le_search.text()
        # self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        self.row_length = 6
        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            book = QLabel()
            #book.setPixmap(QPixmap(self.df_books.title[i]))
            book.setPixmap(QPixmap(self.df_books.cover[i]))
            #book.setText(str(self.df_books.title[i]))
            book.setScaledContents(True)
            book.setFixedWidth(200)
            book.setFixedHeight(250)
            book.mousePressEvent = lambda e, id=self.df_books.id[i]: self.show_book(id)
            self.layout_books.addWidget(book)

    def show_book(self, id):
        clicked = clickedBook(self, id)
        widget.addWidget(clicked)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def signOutFunc(self):
        signOut = UserLoginScreen()
        widget.addWidget(signOut)
        widget.setCurrentIndex(widget.currentIndex() + 1)

####### signing up #######
class SignUpScreen(QMainWindow):
    def __init__(self):
        super(SignUpScreen, self).__init__()
        uic.loadUi('SignUp.ui', self)
        self.backButton.clicked.connect(self.backFunc)
        self.SignUpButton.clicked.connect(self.Add)
        self.df_users = pd.read_excel('logins.xlsx', sheet_name='users')

    def Add(self):
        username = self.newUserEmail.text()
        password = self.newUserPass.text()
        password2 = self.pass2.text()

        if password != password2:
            self.error.setText('Passwords must match.')
        else:
            self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max() + 1, username, password]
            self.df_users.to_excel('logins.xlsx', sheet_name='users', index=False)
            self.backFunc()


    def backFunc(self):
        back = loginScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminMain(QMainWindow):
    def __init__(self):
        super(AdminMain, self).__init__()
        uic.loadUi("AdminMain.ui", self)
        self.userButton.clicked.connect(self.UserButton)
        self.bookButton.clicked.connect(self.BookButton)
        self.orderButton.clicked.connect(self.OrderButton)
        self.signOut_btn.clicked.connect(self.signingOut)

    def UserButton(self):
        pressed = ManageUsers()
        widget.addWidget(pressed)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def BookButton(self):
        pressed = ManageBooks()
        widget.addWidget(pressed)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def OrderButton(self):
        pressed = ManageOrders()
        widget.addWidget(pressed)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def signingOut(self):
        pressed = loginScreen()
        widget.addWidget(pressed)
        widget.setCurrentIndex(widget.currentIndex() + 1)


###### editing users #######
class UserDetails(QMainWindow):
    def __init__(self, parent, id=None):
        super(UserDetails, self).__init__()
        uic.loadUi('AdminUsersPage.ui', self)
        self.id = id
        self.parent = parent
        self.df_users = pd.read_excel('logins.xlsx', sheet_name='users')

        if id:
            self.user = self.df_users.loc[self.df_users.id == id].reset_index()
            self.user_le.setText(str(self.user.username[0]))
            self.pass_le.setText(str(self.user.password[0]))

            self.delete_btn.setVisible(True)
            self.update_btn.setText('Update')
            self.cancel_btn.setText('Close')

            self.update_btn.clicked.connect(self.Update)
            self.delete_btn.clicked.connect(self.Delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add User')
            self.cancel_btn.setText('Cancel')

            self.update_btn.clicked.connect(self.Add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def Add(self):
        username = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()

        comfirm = QMessageBox()
        comfirm.setWindowTitle('Are You Sure?')
        comfirm.setText('New User has been be created.')
        comfirm.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = comfirm.exec()
        if res == QMessageBox.Ok:
            self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max() + 1, username, password]
            self.df_users.to_excel('logins.xlsx', sheet_name='users', index=False)
            self.parent.load_users_data()
            self.close()
        elif res == QMessageBox.Cancel:
            comfirm.close()

    def cancel(self):
        self.close()

    def Update(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('User has been updated.')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            username = self.emailLineEdit.text()
            password = self.passwordLineEdit.text()
            self.df_users.loc[self.df_users.id == self.id, ['username', 'password']] = [username, password]
            self.df_users.to_excel('logins.xlsx', sheet_name='users', index=False)
            self.parent.load_users_data()
            self.close()
        elif res == QMessageBox.Cancel:
            mb.close()

    def Delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('User is gone!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_users = self.df_users[self.df_users.id != self.id]
            self.df_users.to_excel('logins.xlsx', sheet_name='users', index=False)
            self.close()
            self.parent.load_users_data()
        elif res == QMessageBox.Cancel:
            mb.close()



class ManageUsers(QMainWindow):
    def __init__(self):
        super(ManageUsers, self).__init__()
        uic.loadUi('user_manage.ui', self)
        self.backButton.clicked.connect(self.backFunc)


        self.row_length = 10

        self.add_user_btn.clicked.connect(self.add_user)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()
        self.load_users_data()

    def load_users_data(self):
        while self.layout_user.count():
            self.layout_user.itemAt(0).widget().setParent(None)
        self.df_users = pd.read_excel('logins.xlsx', sheet_name='users')
        # searchText = self.le_search.text()
        # self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_users)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1


            user = QLabel()
            user.setPixmap(QPixmap(self.df_users.username[i]))
            user.setText(str(self.df_users.username[i]))
            user.setScaledContents(True)
            user.setFixedWidth(200)
            user.setFixedHeight(20)
            user.mousePressEvent = lambda e, id=self.df_users.id[i]: self.show_user(id)
            self.layout_user.addWidget(user, column_index, row_index)


    def show_user(self, id):
        self.user_details = UserDetails(self, id)

    def add_user(self):
        self.user_details = UserDetails(self)

    def cancel(self):
        self.main = AdminMain()
        self.close()

    def backFunc(self):
        back = AdminMain()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)



######## editing books ##########
class BookDetails(QMainWindow):
    def __init__(self, parent, id=None):
        super(BookDetails, self).__init__()
        uic.loadUi('AdminBooksPage.ui', self)
        self.id = id
        self.parent = parent
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')

        if id:
            self.book = self.df_books.loc[self.df_books.id == id].reset_index()

            self.titleDisp.setText(str(self.book.title[0]))
            self.authorDisp.setText(str(self.book.author[0]))
            self.stockDisp.setText(str(self.book.number[0]))
            self.priceDisp.setText(str(self.book.price[0]))

            self.cover_path = str(self.book.cover[0])
            self.book_photo.setPixmap(QPixmap(self.cover_path))

            self.update_btn.setText('Update this Book')
            self.cancel_btn.setText('Close')

            self.browse_btn.clicked.connect(self.browse)
            self.update_btn.clicked.connect(self.update)
            self.delete_btn.clicked.connect(self.delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add Book')
            self.cancel_btn.setText('Cancel')

            self.browse_btn.clicked.connect(self.browse)
            self.update_btn.clicked.connect(self.add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def cancel(self):
        self.close()
        self.parent.load_book_data()

    def add(self):
        try:
            title = self.titleLe.text()
            author = self.authorLe.text()
            stock = int(self.stockLe.text())
            price = float(self.priceLe.text())
            cover_photo = "images/default.png"
        except:
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('One or more entries need to be numerical.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close()
        else:
            if title == "" or author == "" or stock == "" or price == "":
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('One or more entries are still blank.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()
            elif author.isnumeric():
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('Author needs to be a name.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()
            else:
                mb = QMessageBox()
                mb.setWindowTitle('Are You Sure?')
                mb.setText('New Book will be created.')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                res = mb.exec()
                if res == QMessageBox.Ok:
                    self.df_books.loc[len(self.df_books.index)] = [self.df_books.id.max() + 1, title, author, stock,
                                                                   cover_photo, price]
                    self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)
                    self.parent.load_book_data()
                    self.close()
                elif res == QMessageBox.Cancel:
                    mb.close()

    def browse(self):
        file = QFileDialog.getOpenFileName(self, 'Chose an image', '', 'PNG Files (*.png),')
        if file[0]:
            self.cover_path = file[0]
            self.book_photo.setPixmap(QPixmap(self.cover_path))

    def update(self):
        try:
            title = self.titleLe.text()
            author = self.authorLe.text()
            stock = int(self.stockLe.text())
            price = float(self.priceLe.text())
        except:
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('One or more entries need to be numerical.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close()
        else:
            if title == "" or author == "" or stock == "" or price == "":
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('One or more entries are still blank.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()
            elif author.isnumeric():
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('Author needs to be a name.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()
            else:
                mb = QMessageBox()
                mb.setWindowTitle('Are You Sure?')
                mb.setText('Book will be updated.')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                res = mb.exec()
                if res == QMessageBox.Ok:
                    self.df_books.loc[self.df_books.id == self.id, ['title', 'author', 'number', 'cover', 'price']] = [
                        title, author, stock, self.cover_path, price]
                    self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)
                    self.parent.load_book_data()
                    self.close()
                elif res == QMessageBox.Cancel:
                    mb.close()

    def delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('The item will be removed!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_books = self.df_books[self.df_books.id != self.id]
            self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)
            self.close()
            self.parent.load_book_data()
        elif res == QMessageBox.Cancel:
            mb.close()


class ManageBooks(QMainWindow):
    def __init__(self):
        super(ManageBooks, self).__init__()
        uic.loadUi('book_manage.ui', self)

        self.row_length = 7

        self.add_book_btn.clicked.connect(self.add_book)
        self.cancel_btn.clicked.connect(self.cancel)
        self.backButton.clicked.connect(self.backFunc)

        self.show()
        self.load_book_data()

    def load_book_data(self):
        while self.layout_books.count():
            self.layout_books.itemAt(0).widget().setParent(None)
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')
        # searchText = self.le_search.text()
        # self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        self.row_length = 6
        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            book = QLabel()
            book.setPixmap(QPixmap(self.df_books.cover[i]))
            #book.setPixmap(QPixmap(self.df_books.title[i]))
            #book.setText(str(self.df_books.title[i]))
            book.setScaledContents(True)
            book.setFixedWidth(200)
            book.setFixedHeight(300)
            book.mousePressEvent = lambda e, id=self.df_books.id[i]: self.show_book(id)
            self.layout_books.addWidget(book, column_index)

    def show_book(self, id):
        self.bookDetails = BookDetails(self, id)

    def add_book(self):
        self.bookDetails = BookDetails(self)

    def cancel(self):
        self.Admin_Main = AdminMain()
        self.close()

    def backFunc(self):
        back = AdminMain()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)


###### now onto Orders ##########
class OrderDetails(QMainWindow):
    def __init__(self, parent, id=None):
        super(OrderDetails, self).__init__()
        uic.loadUi('AdminOrdersPage.ui', self)
        self.id = id
        self.parent = parent
        self.df_orders = pd.read_excel('orders.xlsx', sheet_name='orders')

        if id:
            self.order = self.df_orders.loc[self.df_orders.id == id].reset_index()

            self.idDisp.setText(str(self.order.user_id[0]))
            self.emailDisp.setText(str(self.order.customer_name[0]))
            self.dateDisp.setText(str(self.order.date[0]))
            self.priceDisp.setText(str(self.order.total_price[0]))

            self.delete_btn.setVisible(True)
            self.update_btn.setText('Update')
            self.cancel_btn.setText('Close')

            self.update_btn.clicked.connect(self.Update)
            self.delete_btn.clicked.connect(self.Delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add Order')
            self.cancel_btn.setText('Cancel')

            self.update_btn.clicked.connect(self.Add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def Add(self):
        userID = self.idLe.text()
        email = self.emailLe.text()
        date = self.dateLe.text()
        price = self.priceLe.text()

        comfirm = QMessageBox()
        comfirm.setWindowTitle('Are You Sure?')
        comfirm.setText('New Order has been be created.')
        comfirm.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = comfirm.exec()
        if res == QMessageBox.Ok:
            self.df_orders.loc[len(self.df_orders.index)] = [self.df_orders.id.max() + 1, userID, email, date, price]
            self.df_orders.to_excel('orders.xlsx', sheet_name='orders', index=False)
            self.parent.load_orders_data()
            self.close()
        elif res == QMessageBox.Cancel:
            comfirm.close()

    def cancel(self):
        self.close()

    def Update(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('Order has been updated.')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            userID = self.idLe.text()
            email = self.emailLe.text()
            date = self.dateLe.text()
            price = self.priceLe.text()
            if len(userID) == 0:
                userID = self.df_orders.loc[self.df_orders.id == self.id, ['user_id']]

            self.df_orders.loc[self.df_orders.id == self.id, ['user_id', 'customer_name', 'date', 'total_price' ]] = [userID, email, date, price]
            self.df_orders.to_excel('orders.xlsx', sheet_name='orders', index=False)
            self.parent.load_orders_data()
            self.close()
        elif res == QMessageBox.Cancel:
            mb.close()

    def Delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('Order is gone!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_orders = self.df_orders[self.df_orders.id != self.id]
            self.df_orders.to_excel('orders.xlsx', sheet_name='orders', index=False)
            self.close()
            self.parent.load_orders_data()
        elif res == QMessageBox.Cancel:
            mb.close()



class ManageOrders(QMainWindow):
    def __init__(self):
        super(ManageOrders, self).__init__()
        uic.loadUi('order_manage.ui', self)
        self.backButton.clicked.connect(self.backFunc)


        self.row_length = 10

        self.add_order_btn.clicked.connect(self.add_order)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()
        self.load_orders_data()

    def load_orders_data(self):
        while self.layout_orders.count():
            self.layout_orders.itemAt(0).widget().setParent(None)
        self.df_orders = pd.read_excel('orders.xlsx', sheet_name='orders')
        # searchText = self.le_search.text()
        # self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_orders)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            order = QLabel()
            order.setPixmap(QPixmap(self.df_orders.customer_name[i]))
            order.setText(str(self.df_orders.customer_name[i]))
            order.setScaledContents(True)
            order.setFixedWidth(200)
            order.setFixedHeight(30)
            order.mousePressEvent = lambda e, id=self.df_orders.id[i]: self.show_order(id)
            self.layout_orders.addWidget(order)


    def show_order(self, id):
        self.order_details = OrderDetails(self, id)

    def add_order(self):
        self.order_details = OrderDetails(self)

    def cancel(self):
        self.main = AdminMain()
        self.close()

    def backFunc(self):
        back = AdminMain()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() + 1)

















# main
app = QApplication(sys.argv)
begin = loginScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(begin)
widget.setFixedWidth(5000)
widget.setFixedHeight(2000)
widget.show()
sys.exit(app.exec_())
