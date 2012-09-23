'''
Created on Aug 18, 2012

@author: Praveen Senathi
'''
PATH="D:\\Data Mining"
FILE="para.txt"
LOCATIONMIS=PATH+"\\"+FILE
SEQ="data.txt"
LOCATIONSEQ=PATH+"\\"+SEQ

#if __name__ == '__main__':
 #   print ('praveen')
    
def read_file(location):
    fHandler=open(location,'r')
    #print fHandler
    fileContent=fHandler.read()
    fHandler.close()
    return fileContent
    
    
def fileContentstolist(content):
    return content.split("\n")


def getOrderedList(lstValues):    
    dictRaw={}
    #print (misLines)
    for str in lstValues:
        #print(str.find("(",0))
        if "(" and ")" in str:
            item=str[str.index("(")+1:str.index(")")]
            value=str[str.index("=")+1:]
            dictRaw[item]=value
        
   # print (dictSorted)
    OrderedDict=sorted(dictRaw.items(), key=lambda t: t[1])
    return OrderedDict,dictRaw
    #print(OrderedDict[0])
        

def scanData(seqList,misOrderedList): 
    #print(seqList)
    #print(misOrderedList)
    misSupportCount={}
    import re
    regex = re.compile(r'\s+')
    
    #print (misOrderedList[0][0])
    for val in misOrderedList:
        #print (val)
        count=0
        #print (val[0])
        for seq in seqList: 
            #print(val)
           # print(len(val[0]))
            seqNoSpace=regex.sub('',seq)
            #print(seqNoSpace)
            while seqNoSpace.find(val[0])!= -1 :
                """ first part to handle occurances of 12 when we search for 1 and second part to handle 22 when we search for 2 """
                if (seqNoSpace[seqNoSpace.find(val[0])+len(val[0])]=='}' or seqNoSpace[seqNoSpace.find(val[0])+len(val[0])]==',') and (seqNoSpace[seqNoSpace.find(val[0])-1]=='{' or seqNoSpace[seqNoSpace.find(val[0])-1]==','):
                    count=count+1
                    break
                else:
                    seqNoSpace=seqNoSpace[seqNoSpace.find(val[0])+1:]
            
            
        misSupportCount[val[0]]=count
    return misSupportCount
            
            
    
def initpass(misOrderedList,supportcount):
    L=[]
    minMISValue=0
    for str in misOrderedList:
        #print(str)
        countVal=supportcount[str[0]]
        #print(str[0])
        #print(countVal)
        #print(countVal/71)
        #print(str[1])
        if len(L)==0: 
            if float(countVal/71) >= float(str[1]):
                L.append(str[0])
                minMISValue=str[1]
        else:
            if float(countVal/71) >= float(minMISValue):
                L.append(str[0])
    return L
            

def  getFrequent1Itemset(L,misDict,supportcount):
    F1=[]
    #print(L)
    #print(misDict) 
    #print(supportcount)  
    for item in L:
        if  float(supportcount[item]/71) >= float(misDict[item]):
            F1.append(item)
    return F1
               
               
def level2_candidate_gen(L,pi,supportcount,misDict):
    c2=[]
    finalc2=[]
    #print(supportcount)
    
    #print(misDict)
    #print(L)
    for item in L:
        if float(supportcount[item]/71) >= float(misDict[item]):
            temp=L[L.index(item)+1:]
            for tmpItem in temp:
                if float(supportcount[tmpItem]/71) >= float(misDict[item]) and abs(float(supportcount[item]/71)-float(supportcount[tmpItem]/71))<=0.05 :
                    c2.append([item,tmpItem])
    for element in c2:
        finalc2.append(element)
        finalc2.append([[element[0]],[element[1]]])
    return finalc2
                    
                    
  
def lines9to16(seqList,C2,misDict):
    retList=[]
    tempList=[]
    temp=""
    #print(C2)
    #print(seqList)
    
    #seqList=['<{25,37,47}{48}>']
    for list in seqList:
        import re
        regex = re.compile(r'\s+')
        list=regex.sub('',list)
        count=1
        temp1List=[]
        #print(list)
        while count < len(list)-1:
            if list[count]=="{":
                #print(count)
                while list[count]!="}":
                    #print (list[count])
                    if list[count]!="," and list[count]!="}" and list[count]!="{":
                        temp+=list[count]
                        #print(temp)
                       
                    else:
                        #print(temp)
                        if temp != "":
                            tempList.append(temp)
                        #print(tempList)
                        temp=""
                    count=count+1
                tempList.append(temp)
                temp=""
                count=count+1
            else:
                count=count+1
            #print(tempList)    
            temp1List.append(tempList)
            tempList=[]
        retList.append(temp1List)
    #print(C2)  
    #print (retList) 
    #return retList
    finaloutput=[]
    for sublst in C2:
        count=0
        hasList=listsOnly(sublst)
        lenlst=len(sublst)
        #print(lenlst)
        countofitem=0
        min=999999.00
        #print (hasList)
        for sequence in retList:
            #count=0
            countofitem=0
            for indivSequence in sequence:
                if hasList== False:
                    
                    min=defMinMisVal(sublst,misDict)
                    #print(min)
                    
                    if set(sublst).issubset(set(indivSequence)):
                        #print(sublst)
                        #print(indivSequence)
                       
                        count=count+1
                        #print(count)
                        break;
                else:
                    
                    if countofitem<lenlst:
                        #print(countofitem)
                        #print(lenlst)
                        if set(sublst[countofitem]).issubset(set(indivSequence)):
                            #print("test")
                            if float(defMinMisVal(sublst[countofitem],misDict))< float(min):
                                min=defMinMisVal(sublst[countofitem],misDict)
                            #print(indivSequence)    
                            #print(sublst[countofitem])
                            #print(count)
                            
                                #print(min)
                            countofitem=countofitem+1
                    if countofitem==(lenlst):
                        
                        #print(lenlst)
                        #print(indivSequence)
                        count=count+1
                        countofitem=0
                        break
        #print(sublst,count)
        if count/71 >= float(min):
            #print(len(C2))
            finaloutput.append(sublst)
            
    return finaloutput
                        



def defMinMisVal(lst,misDict):
    #print (lst)
    min=misDict[lst[0]]
    for item in lst:
        if float(misDict[item])< float(min):
            min=misDict[item]
    #print(min)
    return min

        
         
                            
                            

     
     

def listsOnly(list):
    import types
    return len(list) == len([x for x in list if isinstance(x,type(list))])     
     

    
        
            
    
     
                            
    
     
                        
    
         
   
    
  
    
    
    
          
      
        
        
        
misFileContent=read_file(LOCATIONMIS)
misOrderedList,misDict=getOrderedList(fileContentstolist(misFileContent))

seqList=fileContentstolist(read_file(LOCATIONSEQ))
#print(seqList)
""" Line 2.1 to get the support count of each item"""
supportcount=scanData(seqList,misOrderedList)
#print(supportcount)
""" Line 2.2 the final step to add elements to L"""
L=initpass(misOrderedList,supportcount)
#print(L)

""" Line 3 to add Frequent 1 item set  """

F1=getFrequent1Itemset(L,misDict,supportcount)
#print(F1)

C2=level2_candidate_gen(L,0.05,supportcount,misDict)


#print(C2)

F2=lines9to16(seqList,C2,misDict)

#F2=getList(seqList,C2)
print(F2)

    






