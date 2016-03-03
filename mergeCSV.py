import sys

fina = open(sys.argv[1], "r")
finb = open(sys.argv[2], "r")

dicA = {}
arrayC = []

for a in fina.readlines():
	# readlines() では末尾に改行コードが含まれるため、改行コードは除去する
	a = a.rstrip('\n')
	[p1, p2] = a.split(',')
	if p2 not in dicA:
		dicA[p2] = p1

for b in finb.readlines():
	b = b.rstrip('\n')
	[p1, p2, p3, p4] = b.split(',')
	if p1 in dicA:
		arrayC.append([dicA[p1], p1, p2, p3, p4])

for c in arrayC:
	print ",".join(c)

fina.close()
finb.close()
