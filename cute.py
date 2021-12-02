import sys
import argparse
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from clickhouse_driver import Client

import paramiko


STRING_LIST = ['3', '4','6', '8', '10', '12', '24']

def makeComboboxModel():
    model = QStringListModel()
    model.setStringList(STRING_LIST)
    return model

def loadMetadata():
    filename = QFileDialog.getOpenFileName()
    if filename == ('', ''):
        return
    print(filename)

    cut, ok = QInputDialog.getInt(mw, "Удаление хвостов", "Номер первого круга в хвосте")
    if ok:
        print(cut)
    else:
        return


    d = QInputDialog(mw)
    d.setWindowTitle("Умножить данные")
    d.setLabelText("Итоговое количество часов")
    d.setComboBoxItems(STRING_LIST)
    if d.exec() == QDialog.Accepted:
        print(d.textValue())
    else:
        return
    if args.local_pipe:
        head, tail = os.path.split(filename[0])
        os.system(f"time ./execpipeline.sh {filename[0]} {cut} {int(d.textValue())} {tail.split('.')[0]}")
        return
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(args.host, username='ec2-user', key_filename=args.ssh_key)
    # stdin, stdout, stderr = ssh.exec_command('ls')
    # print(stdout.readlines())
    # ssh.close()
    rsa = paramiko.RSAKey.from_private_key_file(args.ssh_key)
    # Open a transport
    host,port = args.host,22
    transport = paramiko.Transport((host,port))

    # Auth    
    username,password = "bar","foo"
    transport.connect(None,'ec2-user',None,pkey=rsa)

    # Go!    
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Download
    # sftp.get(filepath,localpath)

    # Upload
    head, tail = os.path.split(filename[0])
    filepath = "/home/ec2-user/" + tail
    localpath = filename[0]
    sftp.put(localpath,filepath)

    # Close
    if sftp: sftp.close()
    if transport: transport.close()

def setMetadataHeaders(clickclient, model):
    headers = [i[0] for i in clickclient.execute("desc raceanalysis.racemetadata")]
    for i in range(len(headers)):
        model.setHeaderData(i, Qt.Horizontal, headers[i])

def updateModel(model, seconds):
    model.clear()
    for row in client.execute(f'select DISTINCT uuid, track, vehicleclass, vehiclename, driver, racedate, racetime from ('
                                'SELECT'
                                '    raceid,'
                                '    max(timepoint) as T'
                                ' FROM raceanalysis.racedata'
                                ' GROUP BY raceid'
                              ') as tabl'
                              ' join raceanalysis.racemetadata as meta on tabl.raceid = meta.uuid'
                              f' WHERE T + 300 < {seconds + 500} and T + 500 > {seconds}'):
        checkable = True
        items = []
        for it in row:
            item = QStandardItem(str(it))
            if checkable:
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
                checkable = False
            items.append(item)
        model.appendRow(items)
    setMetadataHeaders(client, model)

def submitComparison(model):
    print(model)
    print(model.rowCount())
    ids = []
    for i in range(model.rowCount()):
        print(i)
        item = model.index(i, 0)
        if item.data(Qt.CheckStateRole) == QVariant(Qt.Checked):
            print(item.data(Qt.DisplayRole))
            ids.append({"uuid": item.data(Qt.DisplayRole)})
    client.execute("alter table raceanalysis.comparison delete where 1=1")
    client.execute("insert into raceanalysis.comparison(uuid) values", ids)
    


if __name__ == '__main__':

    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='Process data')
    parser.add_argument('--host', type=str, default='localhost', help='Input data')
    parser.add_argument('--ssh-key', type=str, default='localhost', help='Input data')
    parser.add_argument('--local-pipe', type=bool, default=False, help='Input data')

    args = parser.parse_args()

    client = Client(host=args.host)

    mw = QMainWindow()
    mw.setWindowTitle("Клиент к базе")
    mw.resize(1280, 720)
    w = QWidget()

    model = QStandardItemModel()
    
    t = QTableView()
    th = t.horizontalHeader()
    th.setSectionResizeMode(QHeaderView.Stretch)

    t.setModel(model)

    cb = QComboBox()
    cb.setModel(makeComboboxModel())
    cb.currentTextChanged.connect(lambda text: updateModel(model, int(text) * 3600))

    updateBtn = QPushButton()
    updateBtn.setText("Обновить метаданные")
    updateBtn.clicked.connect(lambda: updateModel(model, int(cb.currentText()) * 3600))

    f = QFormLayout()

    f.addRow("Длительность гонки", cb)
    
    hbox  = QHBoxLayout()
    hbox.addWidget(t)
    hbox.addLayout(f)

    lbox = QVBoxLayout()
    lbox.addWidget(updateBtn)
    lbox.addLayout(hbox)

    w.setLayout(lbox)

    mb = QMenuBar()
    loadMetadataAction = QAction("Загрузить отрезок")
    loadMetadataAction.triggered.connect(loadMetadata)
    mb.addAction(loadMetadataAction)

    comparisonAction = QAction("Создать сравнение")
    comparisonAction.triggered.connect(lambda: submitComparison(model))
    mb.addAction(comparisonAction)

    mw.setCentralWidget(w)
    mw.setMenuBar(mb)
    mw.show()
    updateModel(model, int(cb.currentText()) * 3600)

    sys.exit(app.exec_())