import sqlAlch
from datetime import  datetime
import MainWindow



if __name__ == '__main__':
    timeNow = datetime.now()
    sqlAlch.createDb()
    MainWindow.main()



