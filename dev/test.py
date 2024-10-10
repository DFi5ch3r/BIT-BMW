
import functions_test
import server_code.IO as IO
from server_code import serverGlobals
import os
import numpy as np


path = '/home/dfischer/12-Projects/09-BMW-BIT/01-originalMatlabTool/BMW_BIT_TUB/BMW_Phase2_txtonly_BackUp'
IO.create_database(path)
#db = serverGlobals.DB

IO.filter_database('Baureihe', ['KR1'], sourceFullDB = True)
#db2 = serverGlobals.selectedData

IO.readData(selectedData=False)
