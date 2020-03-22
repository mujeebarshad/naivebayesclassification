import math

test = []
age = []
competition = []
type = []
profit = []
glist = []
tcount = 0
tree = []
names = ["cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment", "gill-spacing",
         "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring",
         "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type",
         "spore-print-color", "population", "habitat"
        ]


class Node(object):

    def __init__(self, children=None, attr=None, link1=None):
        if children is None:
            children = []
        self.children = children
        self.attribute = attr
        self.link = link1
        self.parent = None

    def __str__(self):
        return str(self.attribute)


root = Node()


def findEntropy(prof):
    countD = 0
    countU = 0
    tcount = len(glist[0])
    Entropy = 0
    for ele in prof:
        if ele == "p":
            countD+=1
        else:
            countU+=1
    p0 = countU/tcount
    p1 = countD/tcount
    if countD == 0 or countU == 0:
        Entropy = 0
    elif countU == countD:
        Entropy = 1
    else:
        Entropy = -p0 * (math.log2(p0)) - p1 * (math.log2(p1))
    #Entropy = -p0*(math.log2(p0))-p1*(math.log2(p1))
    return Entropy


def AttributedEntropy(col, GEnt, col_index):
    AEntroy = 0
    tcount = len(glist[0])
    attributes = []
    # for att in col:
    #     if att not in attributes:
    #         attributes.append(att)
    # print(attributes)
    f = open("agaricus-lepiota.data", "r")
    lines = f.readlines()
    result = []
    for x in lines:
        res = x.split(',')[col_index]
        if len(res) > 1:
            res = res[:-1]
        if res not in attributes and res != "?":
            attributes.append(res)
    f.close()
    #print(attributes)
    #print(col)
    for i in range(len(attributes)):
        countD = 0
        countU = 0
        count = 0
        for ele in col:
            if ele == attributes[0]:
                if glist[0][count] == "p":
                    countD += 1
                else:
                    countU += 1
            count += 1
        save_att = attributes[0]
        attributes.remove(attributes[0])
        if countD == 0 and countU == 0:
            p0 = 0
            p1 = 0
        else:
            p0 = countU / (countD+countU)
            p1 = countD / (countD+countU)
        # print(countD, " : ", countU, " -- ", save_att)
        Entropy = 0
        if countD == 0 or countU == 0:
            Entropy = 0
        elif countU == countD:
            Entropy = 1
        else:
            Entropy = -p0 * (math.log2(p0)) - p1 * (math.log2(p1))
        AEntroy += ((countU + countD)/tcount) * Entropy
    return GEnt - AEntroy


def reduceTable(col, child, col_index):
    used_att = []
    attributes = []
    # for att in col:
    #     if att not in attribute:
    #         attribute.append(att)
    # print(attribute)
    save_ele = None
    save_cor = None
    f = open("agaricus-lepiota.data", "r")
    lines = f.readlines()
    for x in lines:
        res = x.split(',')[col_index]
        if len(res) > 1:
            res = res[:-1]
        if res not in attributes and res != "?":
            attributes.append(res)
    f.close()
    rest = []
    f = open("agaricus-lepiota.data", "r")
    lines = f.readlines()
    for x in lines:
        res = x.split(',')[0]
        if len(res) > 1:
            res = res[:-1]
        rest.append(res)
    f.close()
    for i in range(len(attributes)):
        countD = 0
        countU = 0
        count = 0
        for ele1 in col:
            if ele1 == attributes[0]:
                if glist[0][count] == "p":
                    countD += 1
                else:
                    countU += 1
            count += 1
        if countD == 0 or countU == 0:
            count = 0
            for ele in col:
                if ele == attributes[0]:
                    for j in range(0, 23):
                        if glist[j][0] != "$":
                            glist[j][count] = "*"
                count += 1
        save_ele = attributes[0]
        attributes.remove(attributes[0])
        cu = 0
        nam = "edible"
        if countU == 0 and countD == 0:
            f = open("agaricus-lepiota.data", "r")
            lines = f.readlines()
            for x in lines:
                res = x.split(',')[col_index]
                if len(res) > 1:
                    res = res[:-1]
                if res == save_ele:
                    nam = rest[cu]
                cu += 1
            f.close()
            if nam == "e":
                nam = "edible"
            elif nam == "p":
                nam = "poisnous"
            new_node = Node(attr=nam)
            new_node.attribute = nam
            new_node.link = save_ele
            used_att.append(save_ele)
            child.children.append(new_node)
        elif countU == 0:
            #print(save_ele)
            new_node = Node(attr="poisnous")
            new_node.attribute = "poisnous"
            new_node.link = save_ele
            used_att.append(save_ele)
            child.children.append(new_node)
        elif countD == 0:
            #print(save_ele)
            new_node = Node(attr="edible")
            new_node.attribute = "edible"
            new_node.link = save_ele
            used_att.append(save_ele)
            child.children.append(new_node)
    while "*" in glist[0]:
        for j in range(0, 23):
            if glist[j][0] != "$":
                glist[j].remove("*")
    #print(used_att)
    f = open("agaricus-lepiota.data", "r")
    lines = f.readlines()
    for x in lines:
        res = x.split(',')[col_index]
        if len(res) > 1:
            res = res[:-1]
        if res not in attributes and res != "?":
            attributes.append(res)
    f.close()
    #print(attributes)
    for x in attributes:
        if x not in used_att:
            return x


def main():
    file = open("agaricus-lepiota.data","r")
    size = 0
    for i in range(23):
        glist.append([])
        test.append([])
    for line in file:
        lst = line.split(",")
        if "." not in lst:
            if size < 6499: #4515 #6599
                for i in range(23):
                    if len(lst[i]) > 1:
                        lst[i] = lst[i][:-1]
                    glist[i].append(lst[i])
            else:
                for i in range(23):
                    if len(lst[i]) > 1:
                        lst[i] = lst[i][:-1]
                    test[i].append(lst[i])
            size += 1
    save_ele = None
    count = 0
    #print(len(glist[0]))
    while len(glist[0]) > 0:
        #print(len(glist[0]))
        GEntropy = (findEntropy(glist[0]))
        max_arr = []
        for i in range(1, 23):
            if glist[i][0] == "$":
                max_arr.append(-3)
            else:
                max_arr.append(AttributedEntropy(glist[i], GEntropy, i))
        val = max(max_arr)
        #print(val)
        for i in range(0, len(max_arr)):
            if val == max_arr[i]:
                if count == 0:
                    root.attribute = names[i]
                    child = root
                else:
                    new_node = Node(attr=names[i])
                    new_node.attribute = names[i]
                    new_node.link = save_ele
                    child.children.append(new_node)
                    child = new_node
               #print(glist[i + 1])
                save_ele = reduceTable(glist[i+1], child, i+1)
                del glist[i+1][:]
                glist[i+1].append("$")
                break
        del max_arr[:]
        count += 1


def showTable():
    print('')
    print(root.attribute)
    for i in root.children:
        print('\t\t--', i.link)
        print('\t\t\t%s' % i.attribute)
        for j in i.children:
            print('\t\t\t\t--', j.link, "--\t\t\t\t")
            print('\t\t\t\t%s' % j.attribute)
            for k in j.children:
                print('\t\t\t\t\t\t--', k.link, "--\t\t\t\t\t\t")
                print('\t\t\t\t\t\t%s' % k.attribute)
                for l in k.children:
                    print('\t\t\t\t\t\t\t\t--', l.link, "--\t\t\t\t\t\t\t\t")
                    print('\t\t\t\t\t\t\t\t%s' % l.attribute)
                    for m in l.children:
                        print('\t\t\t\t\t\t\t\t\t\t--', m.link, "--\t\t\t\t\t\t\t\t\t\t")
                        print('\t\t\t\t\t\t\t\t\t\t%s' % m.attribute)


def checkValue(lst, cor, inc, count):
    for i in root.children:
        if lst[1] == i.link:
            if i.attribute[0] == lst[0]:
                print(count, "correct : ", i.attribute, " -- ", lst[0])
                cor += 1
                count += 1
            elif i.attribute != "poisnous" and i.attribute != "edible":
                for j in i.children:
                    if lst[2] == j.link:
                        if j.attribute[0] == lst[0]:
                            print(count, "correct : ", j.attribute, " -- ", lst[0])
                            cor += 1
                            count += 1
                        elif j.attribute != "poisnous" and j.attribute != "edible":
                            for k in j.children:
                                if lst[3] == k.link:
                                    if k.attribute[0] == lst[0]:
                                        print(count, "correct : ", k.attribute, " -- ", lst[0])
                                        cor += 1
                                        count += 1
                                    elif k.attribute != "poisnous" and k.attribute != "edible":
                                        for x in k.children:
                                            if lst[4] == x.link:
                                                if x.attribute[0] == lst[0]:
                                                    print(count, "correct : ", x.attribute, " -- ", lst[0])
                                                    cor += 1
                                                    count += 1
                                                else:
                                                    print(count,"incorrect : ", x.attribute, " -- ", lst[0])
                                                    inc += 1
                                                    count += 1
                                    else:
                                        print(count, "incorrect : ", k.attribute, " -- ", lst[0])
                                        inc += 1
                                        count += 1
                        else:
                            print(count, "incorrect : ", j.attribute, " -- ", lst[0])
                            inc += 1
                            count += 1
            else:
                print(count, "incorrect : ", i.attribute, " -- ", lst[0])
                inc += 1
                count += 1
    return cor, inc, count


if __name__ == "__main__":
    main()
    cor = 0
    inc = 0
    count = 6500
    showTable()
    for i in range(0, len(test[0])):
        lst = []
        lst.append(test[0][i])
        lst.append(test[5][i])
        lst.append(test[20][i])
        lst.append(test[22][i])
        lst.append(test[3][i])
        cor, inc, count = checkValue(lst, cor, inc, count)
        del lst[:]

    print("Correct : ", cor)
    print("Incorrect : ", inc)
    percent_correct = 100.0 * float(cor) / (float(cor) + float(inc))
    print('Percent correct: %s' % percent_correct)
