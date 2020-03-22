import time

train_data = []
global test_data
test_data = []
global pno
pno = 6500
global correct
correct = 0
global incorrect
incorrect = 0


def getColumn(index, data):
    res_list = []
    for i in range(len(data)):
        res_list.append(data[i][index])
    return res_list


def getEachColumnProb(p_yes, p_no, tcount, col, train_data):
    attributes = []
    result = []
    #print(col)
    for att in col:
        if att not in attributes and att is not "?":
            attributes.append(att)
            result.append([0]*2)
    for i in range(len(attributes)):
        j = 0
        for ele in col:
            if ele == attributes[0]:
                if train_data[j][0] == "e":
                    result[i][0] += 1
                else:
                    result[i][1] += 1
            j += 1
        attributes.remove(attributes[0])
        result[i][0] = float(result[i][0] / p_yes)
        result[i][1] = float(result[i][1] / p_no)
    return result


def getAttributeNo(att, index, t_data):
    #col = getColumn(index, t_data)
    count = 0
    temp_lst = []
    for i in range(len(t_data)):
        if t_data[i][index] not in temp_lst and t_data[i][index] is not "?":
            temp_lst.append(t_data[i][index])
            if att == t_data[i][index]:
                break
    # for ele in col:
    #     if ele not in temp_lst and ele is not "?":
    #         temp_lst.append(ele)
    #print(temp_lst)
    flag = False
    for e in temp_lst:
        if att == e:
            flag = True
            break
        count += 1
    if flag:
        return count
    return -1

def checkAccuracy(p_yes, p_no, all_res, lst, t_data, lst_ind):
    #For P(yes)
    yresult = 1
    nresult = 1
    for i in range(0, len(lst)-1):
        if lst[i+1] is not "?":
            ind = lst_ind[i]
            if ind != -1:
                # print(i, " : ", ind, " : ", lst[i+1])
                # print(all_res[i][ind][0])
                res = all_res[i][ind][0]
                yresult *= res
                res1 = all_res[i][ind][1]
                nresult *= res1
    yresult *= p_yes
    nresult *= p_no
    #Result
    global pno
    global correct, incorrect
    fres = None
    #print(nresult, " : ", yresult)
    if nresult >= yresult:
        fres = "p"
    else:
        fres = "e"
    #print(nresult, " : ", yresult)
    if fres == lst[0]:
        print(pno, " Correct: ", fres, " --- ", lst[0])
        pno += 1
        correct += 1
    else:
        print(pno, " Incorrect: ", fres, " --- ", lst[0])
        pno += 1
        incorrect += 1


def main():
    p_yes = 0
    p_no = 0
    t_yes = 0
    t_no = 0
    size = 0
    train_data = []
    global test_data
    file = open("agaricus-lepiota.data", "r")
    for line in file:
        lst = line.split(",")
        lst[-1] = lst[-1][:-1]
        if size < 6499:
            train_data.append(lst)
        else:
            test_data.append(lst)
        size += 1
    for i in range(len(train_data)):
        if train_data[i][0] == "p":
            p_no += 1
        elif train_data[i][0] == "e":
            p_yes += 1
    t_yes = p_yes
    t_no = p_no
    p_yes = float(p_yes/len(train_data))
    p_no = float(p_no/len(train_data))
    all_res = []
    #print(len(train_data))
    for i in range(22):
        col = getColumn(i+1, train_data)
        #print(col)
        prob = getEachColumnProb(t_yes, t_no, len(train_data), col, train_data)
        all_res.append(prob)
    for i in range(len(test_data)-1):
        lst_ind = []
        for j in range(len(test_data[i])-1):
            lst_ind.append(getAttributeNo(test_data[i][j+1], j+1, train_data))
        checkAccuracy(p_yes, p_no, all_res, test_data[i], train_data, lst_ind)
    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    percent_correct = 100.0 * float(correct) / (float(correct) + float(incorrect))
    print('Percent correct: %s' % percent_correct)


if __name__ == "__main__":
    start = time.time()
    main()
    run_time = time.time() - start
    print('Runtime: %s' % run_time)
