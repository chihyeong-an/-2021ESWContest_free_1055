

def motor(name, x, y, z, w):
    val = [0,0,0,0,0]
    if name =='can':
        val[0] = 1
    elif name == 'pet':
        val[0] = 2
    elif name == 'glass':
        val[0] = 3
    val[1] = 2*(x-7)+1
    if y > 13 :
        val[2] = 100
    elif y > 12:
        val[2] = 95
    elif y > 11:
        val[2] = 90
    elif y > 10:
        val[2] = 85
    elif y > 9:
        val[2] = 80
    elif y > 8:
        val[2] = 75
    elif y > 7:
        val[2] = 70
    elif y > 6:
        val[2] = 65
    elif y > 5:
        val[2] = 60
    elif y > 4:
        val[2] = 55
    elif y > 3:
        val[2] = 50
    elif y > 2:
        val[2] = 45
    elif y > 1:
        val[2] = 40
    else:
        val[2] = 35
    val[3] = int(z)
    val[4] = int(w*0.0198)
    for i in range(0,5):
        int(val[i])
        #print(val[i])
    return val
#a = 'can'
#motor(a,10,4.6,10,5)
