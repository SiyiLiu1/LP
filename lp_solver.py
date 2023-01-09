
"""
name: Siyi Liu
"""

import sys
from fractions import Fraction

UNREACH_BOUND = 99999999999999999999999999999999999999999999999999


def main():
    """
    Input a lP in standard form, and this solver will find the optimal solution for this LP 
    or detect wherether LP is infeasible or unbounded 
    """
    data = classify_nums(sys.stdin)
    dictionary = std_to_dictionary(data)
        
    min_p = min_coefficient_p(dictionary)
    min_b = dictionary['slack_value'][min_p][0]  # 0 repersent "b" position coefficient
    
    if min_b < 0:  # originally infeasible
        handle_infeaiable(dictionary)
           
    largest_coefficient(dictionary)
    print_output(dictionary)
      



def std_to_dictionary(stdform:list) -> dict:
    """
    Input a standard input, the function will translate standard input to 
    dictionary with lexicographic epsilons and return it
    """
    dictionary_form = {}
    dictionary_form['optimal'] = {}
    dictionary_form['optimal'][0] = 0
    dictionary_form['obj'] = {}
    dictionary_form['slack_value'] = {}
    dictionary_form['slack'] = {}
    
    epsilon = Fraction(1)
    for i in range(0,len(stdform[0])):
        dictionary_form['obj'][i+1] = stdform[0][i]
    
    dictionary_form['slack_value'] = {}
    for j in range(0,len(stdform[1])):
        dictionary_form['slack_value'][i+j+2] = {}
        dictionary_form['slack_value'][i+j+2][0] = stdform[1][j]
    
    
    for k in range(0,len(stdform[2])):
        dictionary_form['slack'][i+k+2]={}
        for g in range(0,len(stdform[0])):
            dictionary_form['slack'][i+k+2][g+1] = -stdform[2][k][g]
    
    for e in range(0, len(dictionary_form['slack'])):
        for f in range(0,len(dictionary_form['slack'])):
            dictionary_form['optimal'][i+e+2] = Fraction(0)
            if e == f:
                dictionary_form['slack_value'][i+f+2][i+e+2] = epsilon
            else:
                dictionary_form['slack_value'][i+f+2][i+e+2] = Fraction(0)
                
    return dictionary_form

    
def handle_infeaiable(dictionary:dict) -> None:
    """
    Input a infeasiable dictionary, use Auxiliary methond to solve it 
    """
    obj_num = {}
    for i in dictionary['obj']:
        obj_num[i] = dictionary['obj'][i]
  
    """"omega_position"""
    for i in dictionary['obj']:
        dictionary['obj'][i] = Fraction(0)
    omega_position = len(dictionary['obj'])+len(dictionary['slack'])+1
    dictionary['obj'][omega_position] = Fraction(-1)
    
    for i in dictionary['slack']:
        dictionary['slack'][i][omega_position] = Fraction(1)
        
    leaving = min_coefficient_p(dictionary)

    re_construct_dict(dictionary, omega_position, leaving)
    largest_coefficient(dictionary)
    
    """"detetmine whether lp is feasiable or not. 
    if feasiable, delete the omega colomn"""
    opt = dictionary['optimal'][0] # 0 repersent real optimal value
    if opt != 0:
        print('infeasible')
        exit()
    
    if omega_position in dictionary['obj']:
        del dictionary['obj'][omega_position]
        for i in dictionary['slack']:
            del dictionary['slack'][i][omega_position]
    else:
        if dictionary['slack_value'][omega_position][0] != 0: # [omega_position][0]'s 0 repersent "b" position coefficient
            print('infeasible')
            exit()
        else:
            key_l = sorted(dictionary['obj'])
            entering=dictionary['obj'][key_l[0]]
            for i in range(0,len(key_l)):
                if dictionary['obj'][key_l[i]] != 0:
                    entering = key_l[i]
                    break
            re_construct_dict(dictionary, entering, omega_position)
            del dictionary['obj'][omega_position]
            for i in dictionary['slack']:
                del dictionary['slack'][i][omega_position]
                
    """"pull back the orginal object line values to new objective line"""
    for i in obj_num:
        if i in dictionary['obj']:
            dictionary['obj'][i] += obj_num[i]
        if i in dictionary['slack']:
            for j in dictionary['optimal']:
                dictionary['optimal'][j] += obj_num[i]*dictionary['slack_value'][i][j]
            for j in dictionary['obj']:
                dictionary['obj'][j] += obj_num[i]*dictionary['slack'][i][j]
        

   
def print_output(dictionary:dict) -> None:
    """
    Input a dictionary,print the optimal standard output and original non-basis variable values 
    """
    print('optimal')
    print(float(dictionary['optimal'][0]))  # 0 repersent real optimal value
    output = ''
    sort_key = sorted(dictionary['slack_value'])
    for i in range(0,len(dictionary['obj'])):
        if i+1 in sort_key:
            output += str(float(dictionary['slack_value'][i+1][0])) + ' '  # 0 repersent "b" position coefficient
        else:
            output += '0' + ' '
    print(output)
    

    
def largest_coefficient(dictionary:dict) -> None:
    """
    Input a dictionary, run largest coefficient rule with lexicographic method
    to prevent cycling
    """
    signal = True
    while signal:
        obj_list = sorted(dictionary['obj'].keys())
        max_co = 0
        max_position = 0
        for element in obj_list:
            each = dictionary['obj'][element]
            if each > max_co:
                max_co = each
                max_position = element
                
        if max_co == 0:
            signal = False
        else:
            entering = max_position
            leaving = leaving_var(dictionary,entering)
            re_construct_dict(dictionary, entering, leaving)


def re_construct_dict(dictionary:dict, entering:int, leaving:int) -> None:
    """
    Input a dictionary, entering and leaving variable
    the function will do the piving process to re-construct dictionary
    """
    multiplier = -1/dictionary['slack'][leaving][entering]
    
    """leaving line"""
    for i in dictionary['slack'][leaving]:
        dictionary['slack'][leaving][i] *= multiplier 
    for i in dictionary['slack_value'][leaving]:
        dictionary['slack_value'][leaving][i] *= multiplier
    dictionary['slack_value'][entering] = dictionary['slack_value'].pop(leaving)
    dictionary['slack'][entering] = dictionary['slack'].pop(leaving)
    dictionary['slack'][entering][leaving] = dictionary['slack'][entering].pop(entering)
    dictionary['slack'][entering][leaving] =-multiplier
    
    """non-basis line"""
    for i in dictionary['optimal']:
        dictionary['optimal'][i] += dictionary['slack_value'][entering][i]*dictionary['obj'][entering]

    for i in dictionary['obj']:
        for j in dictionary['slack'][entering]:
            if i==j:
                dictionary['obj'][i] += dictionary['obj'][entering]*dictionary['slack'][entering][j]
    dictionary['obj'][entering] *= -multiplier
    dictionary['obj'][leaving] = dictionary['obj'].pop(entering)
    
    
    """other slack line"""
    for i in dictionary['slack']:
        if i != entering:
            for j in dictionary['slack_value'][i]:
                dictionary['slack_value'][i][j]+=dictionary['slack'][i][entering]*dictionary['slack_value'][entering][j]
            for j in dictionary['slack'][i]:
                if j != entering:
                    dictionary['slack'][i][j] += dictionary['slack'][entering][j]* dictionary['slack'][i][entering]
                  
            dictionary['slack'][i][entering] *=  dictionary['slack'][entering][leaving]
            dictionary['slack'][i][leaving] = dictionary['slack'][i].pop(entering)
            
            
def leaving_var(dictionary:dict, entering:int) -> int:
    """
    Imput a dictionary and a position of entering variable
    Return a position of leaving variable
    """ 
    bound = UNREACH_BOUND
    keys_list = sorted(dictionary['slack_value'].keys())
    bounded = False
    for i in range(0,len(keys_list)):
        if dictionary['slack'][keys_list[i]][entering] < 0:
            bounded = True
            slack_val = dictionary['slack_value'][keys_list[i]][0]  # 0 repersent "b" position coefficient
            cur = slack_val/(-dictionary['slack'][keys_list[i]][entering])
            if cur < bound:
                bound = cur
                tight_var = [keys_list[i]]
            elif cur == bound:
                tight_var.append(keys_list[i])
    if not bounded:
        print('unbounded')
        exit()
        
    if len(tight_var) != 1:
        return find_leaving(dictionary, tight_var,entering)
    return tight_var[0]


def find_leaving(dictionary:dict, t_list:list, entering:int)-> int:
    """
    Imput a dictionary, a list with possible leaving variable 
    and position of entering variable
    Return a position of leaving variable belong
    """ 
    e_list = sorted(dictionary['slack_value'][t_list[0]].keys()) 
    max_to_min = [] 
    min_to_max = []
    for i in range(1, len(e_list)):
        for j in t_list:
            each = dictionary['slack_value'][j][e_list[i]]/(-dictionary['slack'][j][entering])
            
            if each < 0 and j not in min_to_max and j not in max_to_min:
                min_to_max.append(j)
                
            elif each > 0 and j not in max_to_min and j not in min_to_max:
                max_to_min.append(j)

    if len(min_to_max) != 0:
        return min_to_max[0]  # return smallest negative coefficient leaving variable position

    return max_to_min[-1] # return smallest positive coefficient leaving variable position
    
   
def classify_nums(stand_in:str) -> list:
    """
    Input a str which users pump in as standard input
    Return A list with [objective function,constrain val and constrain matrix].
    """
    obj = str_to_list(input().split())   
    begin = True
    nums = []
    while begin:
        line = sys.stdin.readline().strip()
        if line:
            nums.append(str_to_list(line.split()))
        else:
            begin = False
    for line in nums:
        line = str_to_list(line)
        
    slack = []
    val= []
    for num in nums:
        varible = []
        for i in range(0,len(num)-1):
            varible.append(num[i])
        val.append(num[-1])
        slack.append(varible)

    return [obj,val,slack]
            
    
   
def str_to_list(line:list)->list:
    """
    Input a list of string, return a list of Fractions
    """
    for i in range (0,len(line)):
        line[i] = Fraction(line[i])
    return line


def min_coefficient_p(dictionary:dict)-> int:
    """
    Input a dictionary, find the minimum b value
    and return this minimum b value's index.
    """
    min_c = UNREACH_BOUND
    w_list = sorted(dictionary["slack_value"].keys())
    min_set = []
    for i in w_list:
        each = dictionary["slack_value"][i][0] # 0 repersent "b" position coefficient
        if each < min_c:
            min_c = each
            min_set = [i]
        elif each == min_c:
            min_set.append(i)
    
    if len(min_set) != 1:
        return max(min_set)
    
    return(min_set[0])
    

if __name__=='__main__':
    main()