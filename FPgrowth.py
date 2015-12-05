__author__ = 'shuchenwu'
import operator
import timeit
class node(object):
    def __init__(self,name,parent,count):
        self.name = name
        self.child = {}#dictionary to store child, with key the name
        self.parent = parent
        self.count = count
        self.link = None#link to headertable

    def increment(self):
        self.count = self.count+1



#input: supportthreshold, data
#output: a dictionary of frequent 1 itemsets
def find_frequent_1_itemsets(supportcount, data_list):
    # print(data_list)
    pattern = {}

    for list in data_list:
     for item in list:
         if item in pattern.keys():
             pattern[item] = pattern[item] + 1
         else:
             pattern[item] = 1
    # print(pattern)
    if '?' in pattern:
      pattern.pop('?')
      # print(pattern)

    L1 = dict(pattern)
    for k in L1.keys():  #remove items not meeting minSup
        # print(L1.get(k))
        if L1.get(k) < supportcount:
            pattern.pop(k, None)

    pattern = sorted(pattern.items(), key=operator.itemgetter(1), reverse=True)
    # pattern = dict(pattern)
    return (pattern)

#make sure filter through data containing unknown '?'
def load(file):
    f = open(file, 'r')
    data = f.read()

    # print(data)
    mystring = data
    mylist = mystring.splitlines()
    datalist = []
    #Split comma
    for list in mylist:
        list= list.split(',')
        datalist.append(list)
    # print(datalist)

    #clean data into ordinal variables
    processed_list = []
    for i in range(0,datalist.__len__()):
        age = int(datalist[i][0])
        newlist = []#contained modified info
        if age<20:
            newlist.append(['teenager'])
            # print('hello')
            # print(newlist)
            # print('lol')
        elif (age>=20 & age <60):
            newlist.append(['middle age'])
            # print(newlist)

        else:
            newlist.append(['senior'])
            # print(newlist)
        newlist.append([datalist[i][1],datalist[i][3]])
        newlist.append(datalist[i][5:10])
        newlist.append(datalist[i][13:15])
        # print(newlist)
        flattened  = [val for sublist in newlist for val in sublist]
        # print(flattened)
        processed_list.append(flattened)

        # processed_list.append(newlist)
    # print(processed_list)
    f.close()

    return processed_list

def maketree(D,supportcount):
    L = find_frequent_1_itemsets(supportcount,D)# frequent 1 itemset
    #b is successfully excluded
    L = dict(L)#L is the frequent itemset


    headertable = {}#dictionary of headertable
    for k in L:
        headertable[k] = [L[k], None]

    newtree = node('Null', None,1)
    for trans in D:
            P = {}
            for item in trans:
                if item in headertable:

                    # print(headertable[item])
                    #the frequent items in trans
                    P[item] = headertable[item][0]#copy dictionary element frequency
                    # print(P)
            if len(P) > 0:
                #items that appears in L as well as local transaction
                #sort the frequent items in trans according to the order of L
                P_item = sortToList(P,1,None)
                # headertable = dict()
                insert_tree(P_item, newtree, L,headertable)#populate tree with ordered freq itemset


    return newtree, headertable

#returns list converted from input dictionary
def sortToList(item_dict,item,noreverse):
    # print(item)
    if noreverse == True:
        k = sorted(item_dict.items(), key=operator.itemgetter(item),reverse = False)
        newlist =  [freq[0] for freq in k]#local itemset as a list

    else:
        k = sorted(item_dict.items(), key=operator.itemgetter(item), reverse=True)
        newlist = [freq[0] for freq in k]#local itemset as a list
    # print(k)


    return newlist



def insert_tree(P_item, tree, L,headertable):#INSERT FROM THE MOST FREQUENT TO THE LEAST FREQUENT
    # print(P_item[0])

    if P_item[0] in tree.child:#if already in child, increment childnode
        tree.child[P_item[0]].increment()
    else:
        tree.child[P_item[0]] = node(P_item[0],tree,1)
        if headertable[P_item[0]][1] == None:
            headertable[P_item[0]][1] = tree.child[P_item[0]]
        else:
            updateHeader(headertable[P_item[0]][1], tree.child[P_item[0]])
    if len(P_item) > 1:#call updateTree() with remaining ordered items
        insert_tree(P_item[1::], tree.child[P_item[0]], L, headertable)

def updateHeader(startnode,endnode):#link headertable to the last children of that node
    while startnode.link!=None:
        startnode = startnode.link
    startnode.link = endnode
    return 0

def getpath(treeNode): #treeNode comes from header table, extract list containing items to form new tree
    condPats = []
    while treeNode != None:
        prefixPath = []
        traverseNode(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats.append(prefixPath[1:])
        treeNode = treeNode.link
    return condPats

def traverseNode(node, path):
    if node.parent!=None:
        path.append(node.name)
        traverseNode(node.parent,path)



def StrongOrder(headertable):
    toBeSorted = []
    for key in headertable:
        toBeSorted.append([key,headertable[key][0]])
    sortedlist = sorted(toBeSorted,key=lambda l:l[1])
    print(sortedlist)
    return sortedlist

#{'a': [8, <__main__.node object at 0x1049ad860>], 'b': [7, <__main__.node object at 0x1049ad898>], 'c': [6, <__main__.node object at 0x1049ad908>], 'd': [5, <__main__.node object at 0x1049ad940>], 'e': [3, <__main__.node object at 0x1049ad9e8>]}
def FPgrowth(tree,headertable,preFix,supportcount,freqpattern):
    # order = sortToList(headertable,0,True)#sort headertable from least frequent to the most

    order = StrongOrder(headertable)# an order that nothing goes wrong
    # print(order)
    # print(order)
    # print(headertable)
    for i in range(0,order.__len__()):
        item = order[i]
        element = item[0]
        # print(element)
        # L = find_frequent_1_itemsets(supportcount, condipat)

        newFreqSet = preFix.copy()
        newFreqSet.add(element)
        freqpattern.append([newFreqSet,headertable[element][0]])

        # print(newFreqSet)
        # print(freqpattern)

        #generate bottomup trees from element
        condPattBases = getpath(headertable[element][1])
        # since element is in headertable it has to be frequent,
        #construct the conditional fptree

        myCondTree, myHead = maketree(condPattBases,supportcount)
        #print 'head from conditional tree: ', myHead
        if myHead != None:  # go through every item in header
            # print('move on')
            FPgrowth(myCondTree, myHead, newFreqSet, supportcount, freqpattern)
            # print("FPgrowth terminate lower layer")


def getsubtree(postfix,Node):
    pattern = []
    while Node!=None:
        path = []
        traverseNode(Node,path)









D=load('adult_data.txt')
start_time = timeit.default_timer()
D1 = [['a','b'],
      ['b','c','d'],
      ['a','c','d','e'],
      ['a','d','e'],
      ['a','b','c'],
      ['a','b','c','d'],
      ['a'],
      ['a','b','c'],
      ['a','b','d'],
      ['b','c','e','?']]
supportcount = 300
# tree = node('null',None,1)
tree, headertable = maketree(D,supportcount)



print('maketreedone')
freqpattern = []
freqset = set([])


FPgrowth(tree, headertable,freqset,supportcount,freqpattern)# returns and prints frequent pattern

print('start printing frequent pattern')
print(freqpattern)

elapsed = timeit.default_timer() - start_time

print('elapsed time is \n',elapsed)




