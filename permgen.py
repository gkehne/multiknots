#Gregory Kehne

#These methods generate random permutations for petal and uber knots.

import random
import math
import itertools

#this transitions from a petal permutation to the permutation of the petal from one 'roll'
def rotate(p):
	for i in range(len(p)):
		if p[i]==0:
			p[i]=len(p)-1
		else:
			p[i]=p[i]-1
	return p

#rolls the petal projection n times, rather than just once.
def nrotate(p,n):
	for i in range(n%len(p)):
		p=rotate(p)
	return p

#generates a random ubercrossing knot
#random permutation on [n], then ranodm parenthezation assignment on [2*n]
#NOTE: would also need to write uber DT generator, vol bounder
def ugener(n):
	crossing=gener(n)
	identification=tieupknot(n)
	return [crossing, identification]

#HELPER TO UGENER. Feasable up to about n=75 (around 8 seconds) (but it's a geometric random variable).
#returns a means of tying up strands into an uber KNOT
def tieupknot(n):
	knot=False
	cand=[]
	while not knot:
		cand=tieup(n)
		start=0
		current=cand[n]
		strandcounter=1
		while current!=start:
			current=cand[(current+n)%(2*n)]
			strandcounter=strandcounter+1
		if strandcounter==n:
			knot=True
	return cand
	
#HELPER TO UGENER through TIEUPKNOT. Recursively generates a parenthezation on 2*n elements
def tieup(n):
	if n<0:
		print "ERROR: tieup(n) called on invalid n"
	if n==1:
		return [1,0]
	if n==0:
		return []
	#(ELSE, general case)
	r=2*random.randint(0,n-1)+1 #first random swap
	first=tieup((r-1)/2)
	second=tieup((2*n-r-1)/2)
	for j in range(len(first)):
		first[j]=first[j]+1
	for k in range(len(second)):
		second[k]=second[k]+r+1
	candidate=[r]+first+[0]+second
	#not sure if this shifting is necessary, but for full randomness probably
	s=random.randint(0,2*n-1) #shift amount
	for i in range(2*n):
		candidate[i]=(candidate[i]-s)%(2*n)
	return candidate[s:2*n]+candidate[0:s]


#generates a random permutation on n integers
def gener(n):
	ground=range(n)
	g=[]
	while len(ground)>0:
		r=random.randint(0,len(ground)-1)
		g.append(ground[r])
		ground.remove(ground[r])
	return g

#experimental method
#nonrandom knot generator--goes for bigger spacing
def generv(n):
	ground=range(1,n)
	g=[0]
	last=0
	while len(ground)>0:
		#current=choose next unrandomly
		s=0
		for i in ground:
			s=s+(i-last)**2
		r=random.randint(0,s)
		j=0
		while r>0:
			r=r-(ground[j]-last)**2
			j=j+1
		current=ground[j-1]
		g.append(current)
		ground.remove(current)
		last=current
	return g

#experimental method
#nonrandom knot generator--goes for bigger spacing. x^4 instead of x^2 weights
def genervv(n):
	ground=range(1,n)
	g=[0]
	last=0
	while len(ground)>0:
		#current=choose next unrandomly
		s=0
		for i in ground:
			s=s+(i-last)**4
		r=random.randint(0,s)
		j=0
		while r>0:
			r=r-(ground[j]-last)**4
			j=j+1
		current=ground[j-1]
		g.append(current)
		ground.remove(current)
		last=current
	return g