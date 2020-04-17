'''
Solution:
1.  Create a new array filled with 1s and make a two time traversal, once from left to right
    and the other from right to left.
2.  When traversing from left to right, if current element is greater than previous, increment 
    candies array's current element by 1 and otherwise leave 1 as is.
3.  Do the same while traversing from right to left and take max of both the traversals for a 
    particular index. Sum all indices.

Time Complexity:    O(N)    |   Space:  O(1)
--- Passed all testcases successfully on leetcode.
'''


class Solution:
    def candy(self, ratings: List[int]) -> int:
        
        #   edge case check
        if (ratings == None or len(ratings) == 0):
            return 0
        
        #   fill candies array with 1
        candies = [1 for i in range(len(ratings))]
        
        #   left traversal
        for i in range(1, len(ratings)):
            if (ratings[i] > ratings[i - 1]):
                candies[i] = candies[i - 1] + 1
        
        #   initialize total sum
        total = candies[len(ratings) - 1]
        
        #   right traversal and parallel sum computation
        for i in range(len(ratings) - 2, -1, -1):
            if (ratings[i] > ratings[i + 1]):
                candies[i] = max(candies[i], candies[i + 1] + 1)
            total += candies[i]
         
        #   return total sum   
        return total