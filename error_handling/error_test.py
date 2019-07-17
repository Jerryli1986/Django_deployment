from merry import Merry
merry = Merry()

@merry._except(NameError,ValueError,IOError)
def handle_error(e):
    print('Error: ' +str(e))

@merry._except(Exception)
def catch_all(e):
    print ('Unexpected error: ' + str(e))