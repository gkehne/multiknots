# Gregory Kehne

# These methods are for manipulating sequences of crossing-centered bipyramids.
# The bipSeq and unfoldBipSeq methods supplement the methods in bounds.py.
# The maxXing, concave, and sumdiff methods are just for exploring.

import math


# returns sequence of crossing centered bipyramid sizes given a permutation.
# 0th bipyramid is the top one.
def bipSeq(scramble):
	seq = [0 for x in range(len(scramble))]
	a = min(scramble[0], scramble[-1])
	b = max(scramble[0], scramble[-1])
	for i in range(a, b):
		seq[i] = seq[i] + 2

	for i in range(len(scramble) - 1):
		a = min(scramble[i], scramble[i + 1])
		b = max(scramble[i], scramble[i + 1])
		for i in range(a, b):
			seq[i] = seq[i] + 2
	return seq


# returns a list of x-ing centered bipyramid sizes from unfolding a petal
# knot p at index k. Unfolding happens just 'above' the k^th strand
# (strands indexed starting at 0), k=1 is prepetal.
def unfoldBipSeq(p, k):
	q1 = []
	q2 = []
	for i in range(len(p)):
		if p[i] < k:
			q1.append(p[i])
		else:
			q2.append(p[i] - k)
	return bipSeq(q1) + bipSeq(q2)


# checks if xing bips are maximally sized for the perm size
# dev is # of allowed deviations from max size.
def maxXing(p, dev):
	b = bipSeq(p)
	for i in range(len(b) / 2 - 1):
		if b[i] >= b[i + 1]:
			if dev > 0:
				dev = dev - 1
			else:
				return False
	for i in range(len(b) / 2, len(b) - 2):
		if b[i] <= b[i + 1]:
			if dev > 0:
				dev = dev - 1
			else:
				return False
	return True


# checks whether the xing bipyramid sequence for a knot is concave
def concave(p):
	b = bipSeq(p)
	for i in range(1, len(b) - 1):
		if b[i] < b[i - 1]:
			for j in range(-1, len(b) - 1):
				if b[j] > b[i]:
					return True
	return False


# given a list of integers, calculates the pairwise abs val sum.
# this is equal to the number of tetrahedra in face-centered bipyramids
# (less the outside face) for random permutations and large N, these seem
# to approach a normal distribution.
def sumdiff(a):
	summ = math.fabs(a[len(a) - 1] - a[0])
	for i in range(len(a) - 1):
		N = math.fabs(a[i] - a[i + 1])
		summ = summ + N
	return summ
