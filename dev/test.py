import functions_IO
import functions_test
import server_code.IO as IO


path = '/home/dfischer/12-Projects/09-BMW-BIT/01-originalMatlabTool/BMW_BIT_TUB'
db = functions_IO.create_database(path)
#functions_test.display_unique_attributes(db)

#db = IO.create_database(path)
#db = IO.addActiveFlag(db)


