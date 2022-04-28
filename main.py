import sqlAlch
from datetime import  datetime
import MainWindow
import MapMaker



if __name__ == '__main__':
    MapMaker.makeMap()
    timeNow = datetime.now()
    sqlAlch.createDb()
    MainWindow.main()



