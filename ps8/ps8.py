# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time
import operator

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    dic = {}
    inputFile = open(filename)
    for line in inputFile:
        a,b,c = line.split(',')
        dic[str(a)] = [int(b), int(c)]
    return dic



def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res




def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2


def greedyAdvisor(subjects, maxWork, comparator):
    schedule_list = subjects.keys()
    for i in range(1, len(schedule_list)) :
        value = schedule_list[i]
        j = i - 1
        done = False
        while not done:
            if comparator(subjects[value], subjects[schedule_list[j]]):
                schedule_list[j+1] = schedule_list[j]
                j -= 1
                if j < 0 :
                    done = True
            else :
                done = True
        schedule_list[j+1] = value
    recommended_schedule = {}
    courseLoad = 0
    done = False
    for course in schedule_list:
        if subjects[course][1] <= maxWork - courseLoad:
            recommended_schedule[course] = subjects[course]
            courseLoad += subjects[course][1]
    return recommended_schedule



def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = subjects.keys()
    tupleList = subjects.values()
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime(sub):
    for i in range(1,15):
        start_time = time.time()
        bruteForceAdvisor(sub, i+5)
        print str(i+5) + " " + str(time.time()-start_time)


def dpAdvisor(subjects, maxWork):
    rec_dict = {}
    m = {}
        
    work_list = []
    value_list = []
    key_list = []
    for each in subjects:
        work_list.append(subjects[each][1])
        value_list.append(subjects[each][0])
        key_list.append(each)
    
    value, rec_list = dpTree(work_list,value_list,len(work_list)-1,maxWork,m)
    
    for each in rec_list:
        rec_dict[key_list[each]] = (value_list[each],work_list[each])
    return rec_dict

def dpTree(w,v,i,aW,m):
    
    try: return m[(i,aW)]
    except KeyError:
        if i == 0:
            if w[i] < aW:
                m[(i,aW)] = v[i], [i]
                return v[i],[i]
            else:
                m[(i,aW)] = 0, []
                return 0,[]
    
    without_i, course_list = dpTree(w, v, i-1, aW, m)
    if w[i] > aW:
        m[(i,aW)] = without_i, course_list
        return without_i, course_list
    else:
        with_i, course_list_temp = dpTree(w, v, i-1, aW - w[i], m)
        with_i += v[i]
    
    if with_i > without_i:
        i_value = with_i
        course_list = [i] + course_list_temp
    else:
        i_value = without_i
    
    m[(i,aW)] = i_value, course_list
    return i_value, course_list


    

#
# Problem 5: Performance Comparison
#
def dpTime(sub):
    for i in range(1,15):
        start_time = time.time()
        dpAdvisor(sub, i+5)
        print str(i+5) + " " + str(time.time()-start_time)

# Problem 5 Observations
# ======================
#
# 6 0.00606298446655
# 7 0.00536894798279
# 8 0.00684309005737
# 9 0.0100619792938
# 10 0.010360956192
# 11 0.0104031562805
# 12 0.0120661258698
# 13 0.0111398696899
# 14 0.0131788253784
# 15 0.0108029842377
# 16 0.0167860984802
# 17 0.0179488658905
# 18 0.0161209106445
# 19 0.0239119529724
# 6 0.534515857697
# 7 1.40870380402
# 8 3.83683109283
# 9 10.1752700806

# brute force is garbage
# how its performance compares to that of bruteForceAdvisor.


subjects = loadSubjects(SUBJECT_FILENAME)
# dpTime()

#print subjects
#print "Course Catalog"
#printSubjects(loadSubjects(SUBJECT_FILENAME))

# print 'greedy(cmpValue):'
# printSubjects(greedyAdvisor(subjects, 15, cmpValue))
# 
# print '\ngreedy(cmpWork):'
# printSubjects(greedyAdvisor(subjects, 15, cmpWork))
# 
# print '\ngreedy(cmpRatio)'
# printSubjects(greedyAdvisor(subjects, 15, cmpRatio))

# printSubjects(bruteForceAdvisor(subjects,15))
# 
print '-----Tree-----'
dpTime(subjects)
print
print '-----Brute Force------'
bruteForceTime(subjects)

# print dpAdvisor(subjects, 15)