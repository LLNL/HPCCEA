import pdb
def store():
#    pdb.set_trace()
    pss = input("Enter mysql password: ")
    file_object = open('passW.txt', 'w')
    file_object.write(pss)
    file_object.close()

