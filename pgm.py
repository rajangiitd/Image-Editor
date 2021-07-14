# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
			line += '\n'
			fout.write(line)

def averaging_filter(img):
	H=len(img)
	W=len(img[0])
	import copy
	ans=copy.deepcopy(img)
	if(H==1 or H==2 or W==1 or W==2):
		return img
	for i in range(1,H-1):
		for j in range(1,W-1):
			ans[i][j]=(img[i-1][j-1]+img[i-1][j]+img[i-1][j+1]+img[i][j-1]+img[i][j]+img[i][j+1]+img[i+1][j-1]+img[i+1][j]+img[i+1][j+1])//9
	writepgm(ans,"average.pgm")

def Edge_detection(img):
	H=len(img)
	W=len(img[0])
	import copy
	ans=copy.deepcopy(img)
	if(H==1 or W==1):
		return ans
	# Making the middle elements
	for i in range(1,H-1):
		for j in range(1,W-1):
			h= img[i-1][j-1]-img[i-1][j+1]+2*(img[i][j-1]-img[i][j+1])+(img[i+1][j-1]-img[i+1][j+1])
			v= img[i-1][j-1]-img[i+1][j-1]+2*(img[i-1][j]-img[i+1][j])+(img[i-1][j+1]-img[i+1][j+1])
			pixel=pow(pow(h,2)+pow(v,2),0.5)
			ans[i][j]=pixel

	# Horizontal boundaries assuming all outer pixels as 0
	for j in range(1,W-1):
		h = 2*(img[0][j-1]-img[0][j+1])+(img[1][j-1]-img[1][j+1])
		v = (img[1][j-1])+2*(img[1][j])+(img[1][j+1])
		pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
		ans[0][j] = pixel

	for j in range(1, W - 1):
		h = 2*(img[H-1][j-1] - img[H-1][j+1])+(img[H-2][j-1] - img[H-2][j+1])
		v = (img[H-2][j-1])+ 2*(img[H-2][j]) + (img[H-2][j+1])
		pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
		ans[H-1][j] = pixel

	# Making vertical boundaries by assuming all outer pixel value as 0
	for i in range(1,H-1):
		h= img[i-1][1]+2*(img[i][1])+img[i+1][1]
		v= 2*(img[i-1][0]-img[i+1][0])+img[i-1][1]-img[i+1][1]
		pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
		ans[i][0] = pixel

	for i in range(1, H - 1):
		h = img[i-1][W-2]+2*(img[i][W-2]) + img[i + 1][W-2]
		v = img[i-1][W-2]-img[i+1][W-2] + 2*(img[i-1][W-1]-img[i+1][W-1])
		pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
		ans[i][W-1] = pixel

	##now fixing 4 corners assuming outer pixels as 0"
	#top-left
	h=(0-img[1][1])+2*(0-img[0][1])
	v=2*(0-img[1][0])+(0-img[1][1])
	pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
	ans[0][0] = pixel
	#top-right
	h=2*(img[0][W-2])+img[1][W-2]
	v=(0-img[1][W-2])+2*(0-img[1][W-1])
	pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
	ans[0][W-1] = pixel
	#bottom-left
	h = (0-img[H-2][1])+2*(0-img[H-1][1])
	v = 2*(img[H-2][0])+img[H-2][1]
	pixel = pow(pow(h, 2) + pow(v, 2), 0.5)
	ans[H-1][0] = pixel
	#bottom-right
	h3 = img[H-2][W-2]+ 2*(img[H-1][W-2])
	v3 = img[H-2][W-2]+ 2*(img[H-2][W-1])
	pixel = pow(pow(h3, 2) + pow(v3, 2), 0.5)
	ans[H-1][W-1] = pixel
	normal=0
	for _ in ans:
		if(max(_)>normal):normal=max(_)

	normal=int(normal)+1
	n80=(80*normal)/100
	n60=(60*normal)/100
	n40= (40*normal)/100
	n20= (20*normal)/100
	n10= normal/10
	n5=(5*normal)/100
	for i in range(H):
		for j in range(W):
			if(ans[i][j]>=n80):
				ans[i][j]=255
			elif(ans[i][j]<n80 and ans[i][j]>=n60):
				ans[i][j]=190
			elif(ans[i][j]<n60 and ans[i][j]>n40):
				ans[i][j]=140
			elif(ans[i][j]<n40 and ans[i][j]>=n20):
				ans[i][j]=90
			elif(ans[i][j]<n20 and ans[i][j]>=n10):
				ans[i][j]=45
			elif(ans[i][j]<n10 and ans[i][j]>n5):
				ans[i][j]=15
			else:
				ans[i][j]=0
	return ans

def path_of_lowest_energy(img):
	H = len(img)
	W = len(img[0])

	z = Edge_detection(img)
	energy = Edge_detection(img)
	def ad_list(img, i, j):
		n = []
		H = len(img)
		W = len(img[0])
		if (i == 0):
			n.append(None)
			return n
		else:
			if (j == 0):
				n.append([i - 1, 0])
				n.append([i - 1, 1])
			elif (j == W - 1):
				n.append([i - 1, W - 2])
				n.append([i - 1, W - 1])
			else:
				n.append([i - 1, j - 1])
				n.append([i - 1, j])
				n.append([i - 1, j + 1])
		return n
	#making parent dictioanry
	parent = {}
	for j in range(W):
		parent[str(0) + "," + str(j)] = [None]
	for i in range(1, H):
		for j in range(W):
			parent[str(i) + "," + str(j)] = []
			p = ad_list(img, i, j)
			above = []
			for x in p:
				above.append(energy[x[0]][x[1]])
			X = min(above)
			energy[i][j] = z[i][j] + X
			for x in p:
				if (energy[x[0]][x[1]] == X):
					parent[str(i) + "," + str(j)].append([x[0], x[1]])

	my_min = min(energy[H - 1])  # length of shortest path
	#now process of brightening starts
	index = []
	for j in range(W):
		if (energy[H - 1][j] == my_min): index.append(j)
	i = H - 1
	while (True):
		next_index = []
		for column in index:
			img[i][column] = 255

		if (parent[str(i) + "," + str(index[0])] == [None]):
			break
		else:
			for column in index:
				for address in parent[str(i) + "," + str(column)]:
					next_index.append(address)
		index = []
		for item in next_index:
			if item[1] not in index:
				index.append(item[1])
		i = i-1
	return img

########## Function Calls ##########
x = readpgm('flower_gray.pgm')			# test.pgm is the image present in the same working directory
writepgm(x, 'test_o.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
averaging_filter(x)           #it automatic writes a image
writepgm(Edge_detection(x),"edge.pgm")
writepgm(path_of_lowest_energy(x),"energy.pgm") #made this image in path.pgm
