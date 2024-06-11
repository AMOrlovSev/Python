import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import re
import model
from main_window import Ui_MainWindow
import math
import DB as db
import ETL as etl

# для вкладки DB
# def create_bd():
#     c_db = ui.le_db.text()
#     etl.create_csv()
#     db.create_DB_and_Role(c_db)
#     db.connection_DB(c_db)
#     db.create_tables_DB(c_db)
#     db.filling_tables_DB(c_db)

def create_and_filling():
    c_db = ui.le_db.text()
    # db.create_DB_and_Role(c_db)
    # db.connection_DB(c_db)
    db.create_tables_DB(c_db)
    db.filling_tables_DB(c_db)

# для вкладки Markets
def connection_bd():
    c_mdb = ui.le_mdb.text()
    connection=db.connection_DB(c_mdb)
    connection.autocommit = True
    cursor = connection.cursor()
    ui.label_4.setText("Подключение открыто")
    return cursor

def sort_id():
    dict = model.all_markets()
    ui.label_4.setText("Всего строк: " + str(len(dict)))
    ui.tableWidget.setRowCount(len(dict))
    ui.tableWidget.setColumnCount(9)

    if ui.checkBox.isChecked():
        myKeys = list(dict.keys())
        myKeys.sort(reverse = True)
        dict = {i: dict[i] for i in myKeys}

    row = 0
    for key, value in dict.items():
        ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(key)))
        ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(value[0][0][0][0])))
        ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(value[0][0][0][1])))
        ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(value[0][0][0][2])))
        ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(value[0][0][0][3])))
        ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(value[0][0][0][4])))
        ui.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(value[0][0][0][5])))
        ui.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(value[0][1]).replace("[", "").replace("]", "").replace("\'", "")))
        ui.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(value[1])))
        row+=1

def sort_ss():
    tr_f = ui.checkBox.isChecked()
    sorted_state = model.sort_by_state_city(tr_f)
    ui.label_4.setText("Всего строк: " + str(len(sorted_state)))
    ui.tableWidget.setRowCount(len(sorted_state))
    ui.tableWidget.setColumnCount(9)
    row = 0
    for st in sorted_state:
    # print(f"{row[0]}\n{row[1][0][0][0]}\n{row[1][0][1]}\n{row[1][1][0]}\n")
        ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(st[0])))
        ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][0])))
        ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][1])))
        ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][2])))
        ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][3])))
        ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][4])))
        ui.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(st[1][0][0][0][5])))
        ui.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(st[1][0][1]).replace("[", "").replace("]", "").replace("\'", "")))
        ui.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(st[1][1][0])))
        row+=1

# для вкладки Market
def show_by_id():
    id = int(ui.le_mid.text())
    zip = model.market_by_id(id)
    ui.listWidget.clear()
    ui.listWidget.addItem(str(zip))

def show_by_cs():
    city = str(ui.le_mc.text())
    state = str(ui.le_ms.text())
    markets = model.id_by_location(city,state)
    ui.listWidget.clear()
    for row in markets:
        ui.listWidget.addItem(str(row))

def show_by_zd():
    zip = str(ui.le_mzip.text())
    distance = int(ui.le_mdist.text())
    markets = model.id_by_zip_and_distance(zip, distance)
    ui.listWidget.clear()
    for row in markets:
        ui.listWidget.addItem(str(row))

def new_user():
    fname = str(ui.le_mufn.text())
    lname = str(ui.le_muln.text())
    username = str(ui.le_muun.text())
    password = str(ui.le_mup.text())
    model.new_user(fname, lname, username, password)
    ui.listWidget.clear()
    model.cursor.execute("""SELECT * FROM users;""")
    users = model.cursor.fetchall()
    for row in users:
        ui.listWidget.addItem(str(row))

def new_review():
    user_id = int(ui.le_mru.text())
    market_id = int(ui.le_mrm.text())
    score = int(ui.le_mrs.text())
    review = str(ui.le_mrr.text())
    model.new_review(user_id, market_id, score, review)
    ui.listWidget.clear()
    model.cursor.execute("""SELECT * FROM reviews;""")
    reviews = model.cursor.fetchall()
    for row in reviews:
        ui.listWidget.addItem(str(row))

def del_review():
    review_id = int(ui.le_mrid.text())
    model.delete_review(review_id)
    ui.listWidget.clear()
    model.cursor.execute("""SELECT * FROM reviews;""")
    reviews = model.cursor.fetchall()
    for row in reviews:
        ui.listWidget.addItem(str(row))


# __name__ == "__main__":
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# вкладка DB
ui.b_csv.clicked.connect(etl.create_csv)
ui.b_db.clicked.connect(create_and_filling)

# вкладка Markets
ui.b_mdb.clicked.connect(connection_bd)
ui.b_id.clicked.connect(sort_id)
ui.b_ss.clicked.connect(sort_ss)

# вкладка Market
ui.b_mid.clicked.connect(show_by_id)
ui.b_mcs.clicked.connect(show_by_cs)
ui.b_mzd.clicked.connect(show_by_zd)

ui.b_mu.clicked.connect(new_user)
ui.b_mr.clicked.connect(new_review)
ui.b_mdr.clicked.connect(del_review)

sys.exit(app.exec())
