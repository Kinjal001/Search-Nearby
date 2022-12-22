#defining Node class to use in the construction of data structure PointDatabase
class Node:

    def __init__(self, key):
        self.key = key
        self.elementx=key[0]
        self.elementy=key[1]
        self.left = None
        self.right = None
        self.ytreeattr=None

#Tree(range tree) construction according to y coordinates
def YTree(arr):
    #input list is already sorted according to y
    if len(arr)==1:             #base case of length 1 return Node 
        v=Node(arr[0])
    else:
        leftsub,rightsub=[],[]                  #list divide into two sublists for subtrees
        midi=(len(arr)-1)//2                    #middle index of list
        leftsub=arr[:midi+1]
        rightsub=arr[midi+1:]
        v_left=YTree(leftsub)                   #left subtree 
        v_right=YTree(rightsub)                 #right subtree
        v=Node(arr[midi])                       
        v.left=v_left                           #connecting node to subtrees
        v.right=v_right

    return v

def sortY(list,i):  
    #function to sort list according to i th index - 0(x) or 1(y)            
    return sorted(list,key=lambda a:a[i])

def is_leaf(node):
    #return true if node is a leaf else return false
    if node.left==None and node.right==None:
        return True
    return False

def split_node(root,v1,v2,i):
    #return the split node for v1,v2 in root according to i th index of point(x,y)

    if root==None:                  #base case if root is None
        return None
    elif root.key[i]==v1 and v1!=v2:                        #root's i th index itself is the lower bound
        return root
    elif root.left==None and root.right==None:              #if root is a leaf
        if root.key[i]>=v1 and root.key[i]<v2:              #return root if in range
            return root
    else:
        if root.key[i]>=v1 and root.key[i]>=v2:             
            root=root.left
            return split_node(root,v1,v2,i)
        
        if root.key[i]>=v1 and root.key[i]<v2:
            return root

        if root.key[i]<v1 and root.key[i]<v2:
            root=root.right
            return split_node(root,v1,v2,i)
    return None

def returnleaves(root):
    #return all the leaves of the given tree head
    answer=[]
    if root==None:                              #base case
        return []
    if root.left==None and root.right==None:    #if root is leaf return root's value
        return [root.key]
    else:
        answer+=returnleaves(root.left)
        answer+=returnleaves(root.right)
    return answer


def YQuery(root,y1,y2):
    ans=[]
    
    if root.left==None and root.right==None:                #if root is a leaf return root's value if in range
        if root.elementy>=y1 and root.elementy<=y2:
            return [root.key]

    else:

        vsplit=split_node(root,y1,y2,1)                     #store split node
        if vsplit==None:                                    #base case when there is no split node
            return []

        if vsplit.left==None and vsplit.right==None:        #if split node is a leaf return it's value if in range
            if vsplit.elementy>=y1 and vsplit.elementy<=y2:
                ans.append(vsplit.key)

        else:
            v=vsplit.left                                   #checking left subtree of split node

            while not (v.left==None and v.right==None):     #until leaf is encountered check for range
                if v.elementy>=y1:
                    ans+=returnleaves(v.right)               #add all leaves of right subtree of v
                    v=v.left
                else:
                    v=v.right
                
            if v.elementy>=y1 and v.elementy<=y2:             #check for leaf v if in range append it
                ans.append(v.key)
            
            v=vsplit.right                                   #similarly checking for right subtree of split node

            while not (v.left==None and v.right==None):
                if v.elementy<y2:
                    ans+=returnleaves(v.left)
                    v=v.right
                else:
                    v=v.left
                
            if v.elementy>=y1 and v.elementy<=y2:
                ans.append(v.key)
    
    #return final answer list
    return ans

def point_in_pointlist(point,v):
    #returns true if point is present in v
    if v is None:                           #no head given
        return False

    else:
        while not(v.left==None and v.right==None):      #while v is not a leaf traverse by comparing for x coordinate
            if v.key[0]>=point[0]:                      
                v=v.left
            else:
                v=v.right

        if v.key==point:                                #if the leaf contains the given point return True
            return True
        else:
            return False                   

def merge(arr1,arr2,i):
    #function that merge and then sort two arrays accorging to i th index of points(x,y) of list
    arr3 =arr1+arr2
    return sorted(arr3,key=lambda a:a[i])


####class definition for the created data structure PointDatabase####
class PointDatabase():

    def TreeHelper(self,arr):
        #function to create a tree(range tree) according to x coordinate with each node having a link to associate ytree 
        #which is a range tree in y containing all nodes in the subtrees of this node and this node

        ytree=None

        if len(arr)==1:         #base case of length 1
            v=Node(arr[0])
            ytree=Node(arr[0])
            v.ytreeattr=ytree
            
        else:        
            leftsub,rightsub=[],[]                          #list divide into two sublists for subtrees                    
            xmid=(arr[0][0] + arr[-1][0])//2
            for i in range(len(arr)):
                if arr[i][0]<=xmid:
                    leftsub.append(arr[i])
                else:
                    rightsub.append(arr[i])       
            
            v_left=self.TreeHelper(leftsub)
            v_right=self.TreeHelper(rightsub)
            v=Node((xmid,0))
            v.left=v_left
            v.right=v_right
            v.ytreeattr=YTree(merge(leftsub,rightsub,1))            #connecting associater ytree to node
            
        return v

    def __init__(self,pointlist):
        if len(pointlist)!=0:
            p=sortY(pointlist,1)
            self.head = self.TreeHelper(p)
        else:
            self.head=None
        

    def searchNearby(self, q, d):

        qx,qy=q[0],q[1]
        x1,x2=qx-d,qx+d
        y1,y2=qy-d,qy+d
        output=[]

        if self.head==None:
            return []

        if d==0:
            if point_in_pointlist(q,self.head):
                output.append(q)

        else:
            vsplit=split_node(self.head,x1,x2,0)
            if vsplit==None:
                return []

            if vsplit.left==None and vsplit.right==None:
                if vsplit.elementx>=x1 and vsplit.elementx<=x2:
                    if vsplit.elementy>=y1 and vsplit.elementy<=y2:
                        output.append(vsplit.key)
            
            else:
                v=vsplit.left
                
                while not(v.left==None and v.right==None):
                    if v.elementx>=x1 :
                        output+=YQuery(v.right.ytreeattr,y1,y2)
                        v=v.left

                    else:
                        v=v.right

                if v.elementx>=x1 and v.elementx<=x2:
                    if v.elementy>=y1 and v.elementy<=y2:
                        output.append(v.key)  

                v=vsplit.right
                
                while not(v.left==None and v.right==None):
                    if v.elementx<x2 :
                        output+=YQuery(v.left.ytreeattr,y1,y2)
                        v=v.right
                    
                    else:
                        v=v.left

                if v.elementx>=x1 and v.elementx<=x2:
                    if v.elementy>=y1 and v.elementy<=y2:
                        output.append(v.key)  

        return output  