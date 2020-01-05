from queue import Queue
class bookNode:
  ''' Main class for bookNode
  '''
  def __init__(self, bkId, availCount):
    ''' initializing values
    '''
    self.bookId = bkId
    self.avCntr = availCount
    self.chkCounter = 0
    self.left = None
    self.right = None
  
  def _readBookList(self, bookId, avCntr, cur_node):
    ''' inner function to read books list
    '''
    if bookId < cur_node.bookId:
      if cur_node.left is None:
        cur_node.left = bookNode(bookId, avCntr)
      else:
        self._readBookList(bookId, avCntr, cur_node.left)
    elif bookId >= cur_node.bookId:
      if cur_node.right is None:
        cur_node.right = bookNode(bookId, avCntr)
      else:
        self._readBookList(bookId, avCntr, cur_node.right)
  
  def _chkInChkOut(self, root, bkID, inOut):
    ''' Inner function
    '''
    if (root == None):
      return "Book id {} does not exist".format(bkID)
    q = Queue()
    q.put(root)
    while (q.empty() == False):
      node = q.queue[0]
      if (node.bookId == bkID):
        if inOut == "checkOut":
          if node.avCntr > 0:  
            node.avCntr -= 1
            node.chkCounter += 1
            return "entry updated"
          else:
            return "All copies of book id {} have been checked out".format(bkID)
        elif inOut == "checkIn":
          node.avCntr += 1
          return "entry updated"
      q.get() 
      if (node.left != None): 
        q.put(node.left)  
      if (node.right != None): 
        q.put(node.right) 
    return "Book id {} does not exist".format(bkID)

  def _findBook(self, root, x):
    ''' Inner function to find book
    '''
    output = open('outputPS6.txt', 'a+')
    q = Queue()
    q.put(root)  
    while (q.empty() == False): 
      node = q.queue[0]  
      if (node.bookId == x):
        if node.avCntr > 0:  
          output.write("Book id {} is available for checkout".format(x))
        else:
          output.write("All copies of book id {} have been checked out".format(x))  
      q.get() 
      if (node.left != None): 
        q.put(node.left)  
      if (node.right != None): 
        q.put(node.right) 
    output.write("Book id {} does not exist".format(x))
    output.close()

  def _notIssued(self, bkNode):
    ''' Inner function to get books which are not issued yet.
    '''
    output = open('outputPS6.txt', 'a+')
    output.write("\nList of books not issued:\n")
    q = Queue()
    q.put(bkNode)  
    while (q.empty() == False): 
      node = q.queue[0]  
      if (node.chkCounter == 0):
        output.write(str(node.bookId)+"\n")
      q.get()
      if (node.left != None):
        q.put(node.left)
      if (node.right != None):
        q.put(node.right)
    output.close()
  
  def _stockOut(self, eNode):
    ''' Inner function to get books which are out of stock
    '''
    output = open('outputPS6.txt', 'a+')
    output.write("\nAll available copies of the below books have been checked out:\n")
    q = Queue()
    q.put(eNode)  
    while (q.empty() == False): 
      node = q.queue[0]  
      if (node.avCntr == 0):
        output.writelines(node.bookId)
      q.get()
      if (node.left != None):
        q.put(node.left)
      if (node.right != None):
        q.put(node.right)
    output.close()
  
  def _getTopBooks(self, bkNode):
    ''' Inner function to get top 3 books
    '''
    q = Queue()
    q.put(bkNode)
    output = open('outputPS6.txt', 'a+')
    book1 = book2 = book3 = {"chkCounter": 0}
    while (q.empty() == False): 
      node = q.queue[0]
      if node.chkCounter > book1['chkCounter']:
        book3 = book2
        book2 = book1
        book1 = node.__dict__
      elif node.chkCounter > book2['chkCounter']:
        book2 = book1
        book2 = node.__dict__
      elif node.chkCounter > book3['chkCounter']:
        book3 = node.__dict__
      q.get() 
      if (node.left != None): 
        q.put(node.left)  
      if (node.right != None): 
        q.put(node.right)
    output.write("Top Books 1: "+str(book1['bookId'])+
    ","+str(book1['avCntr'])+"\n")
    output.write("Top Books 2: "+str(book2['bookId'])+
    ","+str(book2['avCntr'])+"\n")
    output.write("Top Books 3: "+str(book3['bookId'])+
    ","+str(book3['avCntr'])+"\n")
    output.close()

    
class BookIssueSystem:
  def __init__(self):
    ''' initializing...
    '''
    self.root = None

  def readBookList(self, bookId, avCntr):
    ''' inserting values in a tree
    '''
    if self.root is None:
      self.root = bookNode(bookId, avCntr)
    else:
      self.root._readBookList(bookId, avCntr, self.root)
  
  def chkInChkOut(self, root, bkID, inOut):
    ''' Outer function which call inner function
    '''
    return self.root._chkInChkOut(self.root, bkID, inOut)

  def findBook(self, root, x):
    ''' outer Function to find book which calls inner function
    '''
    if self.root:
      return self.root._findBook(self.root, x)
    else:
      return "Book id {} does not exist".format(x)
  
  def notIssued(self, root):
    ''' Outer function to get books which are not issued yet.
    '''
    return self.root._notIssued(self.root)
  
  def stockOut(self, root):
    ''' Outer function to get books which are not issued yet.
    '''
    return self.root._stockOut(self.root)
  
  def getTopBooks(self, root):
    '''Function writtens top 3 popular books
    '''
    return self.root._getTopBooks(self.root)

  def printBooks(self, bkNode):
    ''' Function prints the list of book ids and the available number of copies in the file outputPS6.txt
    '''
    traversal = ''
    if bkNode != None:
      traversal = self.inorder_print(bkNode.left, traversal)
      traversal += "{} {}\n".format(bkNode.bookId, bkNode.avCntr)
      traversal = self.inorder_print(bkNode.right, traversal)
    if bkNode == None:
      pass
    return traversal

  def inorder_print(self, start, traversal):
    ''' inorder tree traversal for 
        printing elements in ascending order
    '''
    if start != None:
      traversal = self.inorder_print(start.left, traversal)
      traversal += "{} {}\n".format(start.bookId, start.avCntr)
      traversal = self.inorder_print(start.right, traversal)
    if start == None:
      pass
    return traversal
  
bst = BookIssueSystem()
output = open('outputPS6.txt', 'w')
output.close()
InputFile = open('inputPS6.txt')
for line in InputFile:
  bkId, availCount =line.split(', ')
  bst.readBookList(int(bkId), int(availCount))
InputFile.close()
promptsPS6 = open('promptsPS6.txt')
for line in promptsPS6:
  val = line.split(': ')
  # print(val)
  if val[0] == 'checkOut':
    print(bst.chkInChkOut(bst.root, int(val[1]), val[0]))
  elif val[0] == 'checkIn':
    print(bst.chkInChkOut(bst.root, int(val[1]), val[0]))
  elif val[0] == 'ListTopBooks\n':
    bst.getTopBooks(bst.root)
  elif val[0] == 'BooksNotIssued\n':
    bst.notIssued(bst.root)
  elif val[0] == 'findBook':
    print(bst.findBook(bst.root,int(val[1])))
  elif val[0] == 'ListStockOut\n':
    bst.stockOut(bst.root)
  elif val[0] == 'printInventory':
    print("There are a total of xx book titles in the library. \n",bst.printBooks(bst.root))
  else:
    print("Wrong entry", val)
promptsPS6.close()
