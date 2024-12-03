"""
name: Siyi Liu

"""


1.    Run my code using (Thins example:my input "netlib_afiro.txt" is in file "test_LPs_volume1/input"):
python3 lp_solver.py<test_LPs_volume1/input/netlib_afiro.txt


2.    I use Largest coefficient rule with lexicographic method to implentmented, so it prevent cycling
If dictionary is initially-infeasible, I use the Auxiliary method to create a new non-basis variable omega in object row with "-" sign, and all other omega in this coloum is "+" sign.
Then, I pivioting omega with the lowest b's row (omega entering, lowest b leaving). 

Then run Largest coefficient rule with lexicographic method:

if optimal value is not 0: infeasiable distionary

Otherwise deteminte whether omega is in objective row:
1) If omega is in objective row, del the whole omega column
2) If omega is not in objective row, find omega in b row, determine wherther omega's b is 0 or not
   2.1) if omega's b is 0, degenerated omega with first non-zero non-basis variable, then del the whole omega column
   2.2) if omega's b is not 0, infeasiable distionary

if distionary can become feasiable distionary(1 or 2.1):
Determine if orginal object valuses is in new object:
	If so, add the orginal object in dictionary obj line

Then find all remaining orginal object valuses in slack variable, and multiply orginal object valuse and co-responding slack variable each object valuse together, then add them in to objective valuse row.

Then, run Largest coefficient rule with lexicographic method as usual

for boundness:
	everytime when run Largest coefficient rule with lexicographic method pivioting, in function "leaving_var", will determine boundness.



3.   Extra feature:  use "lexicographic" to prevent cycling caused by Largest coefficient rule.

I add epsilons have same number with slack variable to my "optimal" dictionary, with keys same as slack values's keys.  

General structure for my dictionary:
'optimal' is a {}, which includes real optimal value and all lexicographic made valuses
    
    Assume standard input first line have variables, which are length of x
    
    labals of non-basis variables 'obj' here is labal from 1 to x
    basic varables 'slack_value' and 'slack' label from x+1 to x+1+len(basic varables)
    
    
    'slack_value' includes b and all extrammly small lexicographic made variable
    b and lexicographic made variables are {},  they are labals from x+1 to x+1+len(basic varables) == slack variable
    'slack_value' is a square, row and column all labals from from x+1 to len(basic varables)
    
    each 'slack' line is a {}, which include each line's valuse not includes b
    every single slack value will labals in 'obj' labal (from 1 to x)
    'slack' rows labals as 1 to x,      column labals as x+1 to x+1+len(basic varables)

every operation will change many epsilon's coefficient like operation in each slack variable

if many leaving variable have the same value in constrain coloum "b" , then program will compare all epsilon's coefficients, 
   if b > 0, pick smallest
            1. if have negative coefficients, pick the smallest epsilon's index one which has negative coefficient.
            2. if all coefficients are positive, pick smallest coefficient between lagest epsilon's index
   index:      3  4  5  6     pick 4         index:      3  4  5  6        pick 6
   slack:   3  1                             slack:   3  1   
            4     -1                                  4     .3
            5        1                                5        0.1
            6           1                             6           1
           

   index:      3  4  5  6     pick 4
   slack:   3  .01        
            4     -1
            5        1
            6      1      1

