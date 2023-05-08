ls = []
for i in range(5, 30):
	ls.append(i)
print(ls)
ten_perc = (int)(0.1 * len(ls))
print(ls[(len(ls)-ten_perc):])
