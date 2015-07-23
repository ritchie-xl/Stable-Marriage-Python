__author__ = 'ritchie'
def score(c_skill, j_skill):

    ret = c_skill['H'] * j_skill['H'] + \
        c_skill['E'] * j_skill['E'] + \
        c_skill['P'] * j_skill['P']

    return ret

def find_min_key(c_pref):
    min_val = min(c_pref.values())
    for i in c_pref:
        if c_pref[i] == min_val:
            return i


def read_data(path):
    file = open(path,'r')
    c_list = []
    j_list = []
    c_skill={}
    j_skill={}
    j_pref={}

    for line in file:
        if line != '\r\n' and line != '\n':
            patterns = line.strip().split(' ')

            class_name = patterns[0]
            name = patterns[1]
            skills = dict()
            for i in patterns[2:5]:
                skill, rank = i.split(":")
                skills[skill] = int(rank)

            if class_name == 'C':
                c_list.append(name)
                c_skill[name] = skills
            else:
                pref_list = patterns[5].split(',')
                j_list.append(name)
                j_skill[name] = skills
                j_pref[name] = pref_list

    file.close()
    return c_list,j_list,c_skill,j_skill,j_pref

def main():
    c_list,j_list,c_skill,j_skill,j_pref = read_data('./jugglefest.txt')


    nums = len(j_list) / len(c_list)

    j_matched = []
    c_matched = {}

    rd = 0
    while len(j_matched) < len(j_list) :
        rd = rd + 1
        print '\nThis is round: ', str(rd)
        print 'Matched Jugglers:', len(j_matched)
        print 'Matched Circles:', len(c_matched.keys())
        for juggler in j_list: # juggler
            if juggler not in j_matched: # Not matched
                if len(j_pref[juggler]) == 0:
                    continue;
                else:
                    circle = j_pref[juggler][0] # Circle
                print '\n',juggler, 'proposing to ', circle
                print juggler,'has' ,j_pref[juggler], 'in its list'
                fitness = score(c_skill[circle], j_skill[juggler])
                print 'The score is :', fitness
                if  not c_matched.has_key(circle):
                    c_matched[circle] = dict()
                    c_matched[circle][juggler] = fitness
                    j_matched.append(juggler)
                    print 'No juggler in this circle,', juggler, 'added to:', circle
                    print 'Accepted!'
                else:
                    if len(c_matched[circle]) < nums:
                        c_matched[circle][juggler] = fitness
                        j_matched.append(juggler)
                        print 'Accepted!'
                    else:
                        min_key = find_min_key(c_matched[circle])
                        min_fitness = c_matched[circle][min_key]
                        if min_fitness <= fitness:
                            c_matched[circle].pop(min_key)
                            c_matched[circle][juggler] = fitness
                            j_matched.remove(min_key)
                            j_matched.append(juggler)
                            print 'accepted!'
                        else:
                            print 'Rejected!'

                j_pref[juggler].remove(circle)
                print 'Now',circle ,':', c_matched[circle]

    # for item in c_matched.items():
    #     print item

if __name__ == '__main__':
    main()
