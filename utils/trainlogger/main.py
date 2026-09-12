import csv
import os
import discord

def hextodec(hexnum):
    decnum = int(str(hexnum), 16) 
    return decnum

def dectohex(decnum):
    hexnum = hex(decnum)
    return hexnum[2:].upper()

def is_hexadecimal(s):
   for char in s:
      if not char.isalnum(): # Check if the character is a valid hexadecimal digit
         return False
   return True

def addTrain(userid, username, set, date, train_type, line, start, end, note):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/{username}.csv"
    fileid = f"utils/trainlogger/userdata/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if set.endswith('-'):
        set = set[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',set, date,train_type, line, start, end, note])


    print(f"Data saved to {filename}")
    return id

# Tram version:
def addTram(userid, username, date, train_number, train_type, line, start, end, notes):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/tram/{username}.csv"
    fileid = f"utils/trainlogger/userdata/tram/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\tram')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/tram')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, notes])


    print(f"Data saved to {filename}")
    return id

def addSydneyTrain(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/sydney-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/sydney-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\sydney-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/sydney-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addBus(userid, username, date, train_number, train_type, line, start, end, operator, notes=None):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/bus/{username}.csv"
    fileid = f"utils/trainlogger/userdata/bus/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\bus')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/bus')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, operator, notes])


    print(f"Data saved to {filename}")
    return id
# B
def addFlight(userid, username, date, train_number, train_type, line, start, end, operator):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/flights/{username}.csv"
    fileid = f"utils/trainlogger/userdata/flights/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\flights')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/flights')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, operator])


    print(f"Data saved to {filename}")
    return id


def addSydneyTram(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/sydney-trams/{username}.csv"
    fileid = f"utils/trainlogger/userdata/sydney-trams/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\sydney-trams')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/sydney-trams')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addCanberraTram(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/canberra-trams/{username}.csv"
    fileid = f"utils/trainlogger/userdata/canberra-trams/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\canberra-trams')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/canberra-trams')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]

    id = dectohex(hextodec(id)+1)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addAdelaideTrain(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/adelaide-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/adelaide-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\adelaide-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/adelaide-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addAdelaideTram(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/adelaide-trams/{username}.csv"
    fileid = f"utils/trainlogger/userdata/adelaide-trams/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\adelaide-trams')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/adelaide-trams')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addPerthTrain(userid, username, date, train_number, train_type, line, start, end):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/perth-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/perth-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\perth-trains')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/perth-trains')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # file.write('\n')
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end])


    print(f"Data saved to {filename}")
    return id

def addFlight(userid, username, date, train_number, train_type, line, start, end, registration):

    # Create a CSV file named after the username
    filename = f"utils/trainlogger/userdata/flights/{username}.csv"
    fileid = f"utils/trainlogger/userdata/flights/{userid}.csv"
    
    if not os.path.exists(fileid):
        if not os.path.exists(filename):
            # Create the file if it does not exist
            with open(fileid, 'w') as file:
                file.write('')  
            print(f"File created: {fileid} (belonging to {username})")
            filename = fileid
        else:
            print(f"File already exists: {filename}")
    else:
        print(f"File already exists: {fileid} (belonging to {username})")
        filename = fileid
    
    if date.endswith('-'):
        date = date[:-1]

    id = None

    # Write the data to the CSV file
    try:
        os.listdir('utils\\trainlogger\\userdata\\flights')
    except FileNotFoundError:
        os.mkdir('utils/trainlogger/userdata/flights')
        id = 0

    with open(filename, 'r+', newline='') as file:
        data = file.readlines()
        if data == []:
            id = 0
        else:
            id = data[-1].split(',')[0][1:]
    
    id = dectohex(hextodec(id)+1)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f'#{id}',date, train_number,train_type, line, start, end, registration])


    print(f"Data saved to {filename}")
    return id

def readLogs(userid, username):


    filename = f"utils/trainlogger/userdata/{username}.csv"
    fileid = f"utils/trainlogger/userdata/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid

    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1] 
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
 
def readTramLogs(userid, username):

    filename = f"utils/trainlogger/userdata/tram/{username}.csv"
    fileid = f"utils/trainlogger/userdata/tram/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readSydneyTrainLogs(userid, username):

    filename = f"utils/trainlogger/userdata/sydney-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/sydney-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    
def readSydneyLightRailLogs(userid,username):

    filename = f"utils/trainlogger/userdata/sydney-trams/{username}.csv"
    fileid = f"utils/trainlogger/userdata/sydney-trams/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readBusLogs(userid, username):

    filename = f"utils/trainlogger/userdata/bus/{username}.csv"
    fileid = f"utils/trainlogger/userdata/bus/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readFlightlogs(userid, username):

    filename = f"utils/trainlogger/userdata/flights/{username}.csv"
    fileid = f"utils/trainlogger/userdata/flights/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readAdelaideLogs(userid, username):

    filename = f"utils/trainlogger/userdata/adelaide-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/adelaide-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def readAdelaideTramLogs(userid, username):

    filename = f"utils/trainlogger/userdata/adelaide-trams/{username}.csv"
    fileid = f"utils/trainlogger/userdata/adelaide-trams/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    
def readPerthLogs(userid, username):

    filename = f"utils/trainlogger/userdata/perth-trains/{username}.csv"
    fileid = f"utils/trainlogger/userdata/perth-trains/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

# use this instead for future
def universalReadLogs(userid, username, mode):

    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
        
    user_data = []

    try:

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            user_data = list(reader)
            # data = file.readlines()
            # print(data)
            if user_data == []:
                return 'no data'
        

        if len(user_data) > 0:
            return user_data[::-1]
        else:
            return []
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

# same as one above but only reads the row you put in   
def readRow(userid, username, logid):
    try:
        os.listdir('utils\\trainlogger\\userdata')
    except FileNotFoundError:
        return 'no data at all'
    

    filename = f"utils/trainlogger/userdata/{username}.csv"
    fileid = f"utils/trainlogger/userdata/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    

    # Open the CSV file and read the data
    with open(filename, 'r', newline='') as file:
        data = file.readlines()

        if data == []:
            return 'no data for user'
        else:
            if logid == 'LAST':
                id = data[-1].split(',')[0][1:]
            else:
                id = logid
            row = None
            for r in data:
                if r.split(',')[0] == f'#{id}':
                    row = r
                    break
            if row == None:
                return 'invalid id did not show up'
            else:
                return row

# same as the other but it works for all modes
def universalReadRow(userid, username, logid, mode):
    try:
        os.listdir('utils\\trainlogger\\userdata')
    except FileNotFoundError:
        return 'no data at all'
    

    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    

    # Open the CSV file and read the data
    with open(filename, 'r', newline='') as file:
        data = file.readlines()

        if data == []:
            return 'no data for user'
        else:
            if logid == 'LAST':
                id = data[-1].split(',')[0][1:]
            else:
                id = logid
            row = None
            for r in data:
                if r.split(',')[0] == f'#{id}':
                    row = r
                    break
            if row == None:
                return 'invalid id did not show up'
            else:
                return row
        
def deleteRow(userid, username, logid, mode):

    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    
        
    # Open the CSV file and read the data
    with open(filename, 'r+', newline='') as file:
        data = file.readlines()

        if logid == 'LAST':
            id = data[-1].split(',')[0][1:]
        else:
            id = logid
        
        file.truncate(0)
        file.seek(0)
        
        for r in data:
            if r.split(',')[0] != f'#{id}':
                file.write(r)
                
        return id
    
def editRow(userid, username, logid, mode, line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', traintype:str='auto', notes:str='nochange'):
    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    

    # Open the CSV file and read the data
    with open(filename, 'r+', newline='') as file:
        data = file.readlines()

        # Find the row to edit
        row_index = None
        for i, row in enumerate(data):
            if row.split(',')[0] == f'#{logid}':
                row_index = i
                break

        if row_index is not None:
            # Split the row into fields
            fields = data[row_index].strip().split(',')

            # Update fields that aren't 'nochange'
            if line != 'nochange':
                fields[4] = line
            if number != 'nochange':
                fields[1] = number
            if start != 'nochange':
                fields[5] = start
            if end != 'nochange':
                fields[6] = end
            if date != 'nochange':
                fields[3] = date
            if traintype != 'auto':
                fields[2] = traintype
            if notes != 'nochange':
                fields[7] = notes

            # Reconstruct the row
            data[row_index] = ','.join(fields) + '\n'

            # Write all data back to file
            file.seek(0)
            file.truncate()
            file.writelines(data)

            return data[row_index]
        
        return 'invalid id did not show up'
    
def editRowBus(userid, username, logid, mode, line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', traintype:str='auto',operator:str='nochange', notes:str='nochange'):
    if mode == 'train':
        filename = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filename = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filename}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filename = fileid
    

    # Open the CSV file and read the data
    with open(filename, 'r+', newline='') as file:
        data = file.readlines()

        # Find the row to edit
        row_index = None
        for i, row in enumerate(data):
            if row.split(',')[0] == f'#{logid}':
                row_index = i
                break

        if row_index is not None:
            # Split the row into fields
            fields = data[row_index].strip().split(',')

            # Update fields that aren't 'nochange'
            if line != 'nochange':
                fields[4] = line
            if number != 'nochange':
                fields[1] = number
            if start != 'nochange':
                fields[5] = start
            if end != 'nochange':
                fields[6] = end
            if date != 'nochange':
                fields[3] = date
            if traintype != 'auto':
                fields[2] = traintype
            if notes != 'nochange':
                fields[8] = notes
            if operator != 'nochange':
                fields[7] = operator

            # Reconstruct the row
            data[row_index] = ','.join(fields) + '\n'

            # Write all data back to file
            file.seek(0)
            file.truncate()
            file.writelines(data)

            return data[row_index]
        
        return 'invalid id did not show up'



