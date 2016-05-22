#Gregory Kehne

#This program returns the hyperbolic volume of a petal knot, given its 
#permutation. It does this by generating DT notation for the petal knot, then
#querying snappy for the volume of the knot that this DT notation describes. 
#It uses a few helper methods in order to accomplish this.

import snappy

def pName(perm):
	s=str(dtNote(perm))
	s="DT:[("+s[1:-1]+")]" #string trimming
	return snappy.Manifold(s).identify()

def uName(uber):
	s=str(udtNote(uber))
	s="DT:[("+s[1:-1]+")]" #string trimming
	return snappy.Manifold(s).identify()

#main method
#returns the volume of a PETAL knot, given a permutation.
def pVol(perm):
	#get s into snappy format
	s=str(dtNote(perm))
	s="DT:[("+s[1:-1]+")]" #string trimming
	return snappy.Manifold(s).volume()

#main method
#returns the volume of an UBER knot, given a permutation and tieup.
def uVol(uber):
	#get s into snappy format
	s=str(udtNote(uber))
	s="DT:[("+s[1:-1]+")]" #string trimming
	return snappy.Manifold(s).volume()



#returns the accuracy on the volume of a PETAL knot, given a permutation.
def pAcc(perm):
	#get s into snappy format
	s=str(dtNote(perm))
	s="DT:[("+s[1:-1]+")]" #string trimming
	a=snappy.Manifold(s).volume().accuracy
	return a

#retrrns the accuracy on the volume of an UBER knot, given a permutation.
def uAcc(uber):
	#get s into snappy format
	s=str(udtNote(uber))
	s="DT:[("+s[1:-1]+")]" #string trimming
	a=snappy.Manifold(s).volume().accuracy
	return a



#generates DT notation for a petal knot, given its permutation
def dtNote(perm):
	if len(perm)%2==0:
		print "WARNING: even length permutation!"
		return
	#make x-ing matrix given permutation order
	n=len(perm)
	#populate new matrix with crossing numbers (N is the numbering matrix)
	N=[[0 for x in range(n)] for x in range(n)]
	#xing counter
	counter=1
	sequence=[]
	for y in range(n):
		sequence.append((2*y+1)%n)
	#here we are tracing the ith strand (row)
	for i in range(n): #petal knot, so strands are traversed in order
		for j in range(n):
			#k is the order in which the ith strand crosses other strands
			#For i= strand 0, k follows the form 1,3,5, ... n-4, n-2, 2,4,6, ... n-3, n-1
			k=(i+sequence[j])%n 
			if N[i][k]!=0:
				print "ERROR: Repeat examination during crossing number assignment!"
			if k!=i:
				#assign an x-ing number for this crossing
				N[i][k]=counter
				counter=counter+1
				if (N[i][k])%2==0 and perm[i]-perm[k]>0: #it's an odd under-crossing
					N[i][k]=-N[i][k] #negate it
	#generate DT ordered pairs
	dt=[0 for x in range(n*(n-1)/2)]
	for i in range(n):
		for j in range(n):
			if i!=j and N[i][j]%2==1: #take odd crossing numbers
				#indexes starting at 0, even though numbers in crossings start at 1
				dt[(N[i][j]-1)/2]=N[j][i] #insert their symmetric (even entry) pairs in that spot
	return dt

#generates DT notation for an UBER KNOT, given its central permutation and 'tieup' information
def udtNote(uber):
	#preliminaries
	perm=uber[0]
	tieup=uber[1]
	n=len(perm)
	m=n
	odd=True
	if n%2==0: #handling the odd case is very gnarly
		m=n+1
		odd=False
	#populate new matrix with crossing numbers; N is this numbering matrix
	N=[[0 for x in range(n)] for x in range(n)]
	counter=1 #this will count the crossings as they are traversed
	strand=[0] #strand order and direction information, based on tieup
	for i in range(1,2*n): #this establishes the order in which the strands will be chased
		strand.append(tieup[(strand[i-1]+n)%(2*n)])
	for i in range(n): #current strand/traversal direction
		j=strand[i]
		#this section computes the order in which this jth strand crosses other strands
		#example: for strand j=0, forwards, n odd, order is [1,3,5, ... n-4, n-2, 2,4,6, ... n-3, n-1]
		sequence=[]
		for y in range(m):
			sequence.append((2*y+1)%m)
		parity=2*((j%n)%2)-1 #parity=1 if strand # is even, -1 if it's odd
		for x in range(m): #adjust sequence to account for current strand's index
			sequence[x]=(j%n+parity*sequence[x])%m
		if j>=n: #depending on j, traversal of the strand should happen backwards
			sequence.reverse()
		if not odd: #we've been pretending the n+1st strand is present, but now remove it
			sequence.remove(n)
		for k in range(n):
			l=sequence[k]%n
			if N[j%n][l]!=0:
				print "ERROR: Repeat examination during crossing number assignment!"
			if l!=j%n:
				#go down the k strand assigning xing numbers
				N[j%n][l]=counter
				counter=counter+1
				if (N[j%n][l])%2==0 and perm[j%n]<perm[l]:
					N[j%n][l]=-N[j%n][l]
	#generate DT ordered pairs
	dt=[0 for x in range(n*(n-1)/2)]
	for i in range(n):
		for j in range(n):
			if N[i][j]%2==1:
				dt[(N[i][j]-1)/2]=N[j][i] #indexes starting at 0, even though numbers in crossings start at 1
	return removeloops(dt)

#helper method for udtNote() (above)
#takes the DT code of a knot and returns DT code with any unigons removed
def removeloops(code):
	eliminating=True
	while eliminating:
		eliminating=False
		for j in range(len(code)):
			if j>=len(code):
				continue
			if abs(2*j+1-abs(code[j]))==1 or (j==0 and abs(code[j])==max([max(code),-min(code)])):
				eliminating=True
				code.remove(code[j])
				for k in range(len(code)):
					if abs(code[k])>2*j+1:
						if abs(code[k])==2:
							if code[k]<0:
								code[k]=-2*len(code)
							else:
								code[k]=2*len(code)
						else:
							if code[k]<0:
								code[k]=code[k]+2
							else:
								code[k]=code[k]-2					
	return code