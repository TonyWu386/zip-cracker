# -----------------------------------------------------------------------------
# File name: zip_cracker.py                                                   #
# Date created: 3/22/2015                                                     #
# Date last modified: 3/24/2015                                               #
#                                                                             #
# Author: Tony Wu (Xiangbo)                                                   #
# Email: xb.wu@mail.utoronto.ca                                               #
#                                                                             #
# Python version: 3.4                                                         #
# Dependencies: None                                                          #
#                                                                             #
# License: GNU GPL v2.0                                                       #
#                                                                             #
# Copyright (c) 2014-2015 [Tony Wu], All Right Reserved                       #
# -----------------------------------------------------------------------------


class cZipCrack:

    # This class contains two methods for cracking ZIP files
    # zipcrack - single-threaded algorithm
    # multithreadzc - multi-threaded algorithm

    def zipcrack(Filename, Dictionary):
        '''(str, str) -> str
        The first str parameter is the filename of an encrypted ZIP file.
        The second str parameter is the filename of a txt dictionary file.

        Prints the execution time.
        Returns a string either containing the password or
        "NOT FOUND IN DICTIONARY" if password is not contained in
        the dictionary.

        >>> zipcrack('zip1.zip', 'dictionary.txt')
        'Execution time is: 0.002998828887939453'
        'abc123'
        '''

        import time as tm
        import zipfile as zp

        start = tm.time()

        a = open(Dictionary, "r")
        file = zp.ZipFile(Filename, "r")
        c = "NOT FOUND IN DICTIONARY"

        for line in a:
            line = line[:-1]
            try:
                b = bytes(line, 'utf-8')
                file.extractall(None, None, b)
                c = line
                break
            except:
                pass

        end = tm.time()
        totaltime = end - start
        print("Execution time is: " + str(totaltime))
        a.close()
        return str(c)

    def mthelper(file, pwd, q1):
        '''(file, bytes, queue) -> NoneType
        This is a helper method for cZipCrack.multithreadzc
        '''

        import zipfile as zp

        try:
            file.extractall(None, None, pwd)
            q1.put((pwd).decode("utf-8"))
        except:
            pass

    def multithreadzc(Filename, Dictionary):
        '''(str, str) -> str
        The first str parameter is the filename of an encrypted ZIP file.
        The second str parameter is the filename of a txt dictionary file.

        This function uses a multithreaded algorithm.
        Prints the execution time.
        Returns a string either containing the password or
        "NOT FOUND IN DICTIONARY" is password is not contained in the
        dictionary.

        >>> multithreadzc('zip1.zip', 'dictionary.txt')
        'Execution time is: 0.002998828887939453'
        'abc123'
        '''

        import time as tm
        import queue as Qu
        from threading import Thread
        import zipfile as zp

        start = tm.time()

        a = open(Dictionary, "r")
        file = zp.ZipFile(Filename, "r")

        q1 = Qu.Queue()

        for line in a:
            line = line[:-1]
            b = bytes(line, 'utf-8')
            t = Thread(target=cZipCrack.mthelper, args=(file, b, q1))
            t.start()
            t.join()

        end = tm.time()
        totaltime = end - start
        print("Execution time is: " + str(totaltime))
        a.close()
        if q1.empty():
            retVal = "NOT FOUND IN DICTIONARY"
        else:
            retVal = str(q1.get())
        return retVal
