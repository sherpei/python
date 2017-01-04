import os

class CleanDiskC:

    total=0;
    countFiles=0;
    countFolders=0;
    fileNotFoundError=list()
    permissionError=list()
    files=list()

    def __init__(self, bigSize=50, state=True):
        self.bigSize=bigSize
        self.stateless=state

    def printRow(self, size, path):
        size=str(size)+'Mb'
        while(len(size)<8):
            size+=' '
        print('|| '+size+'|| '+path)
    
    def findBigFiles(self, path):
        if not self.stateless:
            print('Progress: |', end='')
        self.searchBigFiles(path)       
        if not self.stateless:
            if len(self.fileNotFoundError)>0:
                print('\n\nCan\'t find files:')
                print('----------------------------')
                for elem in self.fileNotFoundError:
                    print(elem)
                print('----------------------------')
                print('Total: '+str(len(self.fileNotFoundError))+' elements\n')
            if len(self.permissionError)>0:
                print('\n\nDon\'t have pernission to access folder:')
                print('----------------------------')
                for elem in self.permissionError:
                    print(elem)
                print('----------------------------')
                print('Total: '+str(len(self.permissionError))+' folders\n')
            print('\nFiles with size more then '+str(self.bigSize)+'Mb:')
            print('----------------------------')
            self.files.sort(key=lambda x: x['size'], reverse=True)
            for elem in self.files:
                self.printRow(elem['size'], elem['path'])
        print('----------------------------')
        print('Total big files store: '+str(round(self.total/1024,1))+'Gb')
        print('Total cheched: '+str(self.countFiles)+' files')
        print('Total checked: '+str(self.countFolders)+' folders')
            
        
    def searchBigFiles(self, path):
        self.countFolders+=1        
        try:
            folder=os.listdir(path)
            if path=='\\':
                path=''
            for element in folder:
                if os.path.isfile(path+'\\'+element):
                    self.countFiles+=1
                    if not self.stateless:
                        if self.countFiles%10000==0:
                            print(str(self.countFiles)+'|',end='')
                    statinfo=os.stat(path+'\\'+element)
                    if(statinfo.st_size>1024*1024*self.bigSize):
                        size=round(statinfo.st_size/(1024*1024),1)
                        self.total+=size
                        if self.stateless:
                            self.printRow(size, path+'\\'+element)
                        else:
                            self.files.append({'size':size, 'path':path+'\\'+element})
                elif os.path.isdir(path+'\\'+element):           
                        self.searchBigFiles(path+'\\'+element)
        except PermissionError:
            if self.stateless:
                print('no access to folder: '+path)
            else:
                self.permissionError.append(path)
        except FileNotFoundError:
            if self.stateless:
                print('folder doesn\'t exist: '+path)
            else:
                self.fileNotFoundError.append(path)

#bigSize: default=50Mb
#stateless: default=True
            
do=CleanDiskC(50, False)
do.findBigFiles('\\')
