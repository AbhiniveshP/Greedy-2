'''
Solution:
1.  Using Max Heap, all tasks with their frequencies are put in Heap and until cooldown,
    top elements are taken out from Heap, and if cooldown time still is left, then place
    those top elements in another Buffer array and just pass the time.
2.  Using another approaach, calculate number of partitions using max frequency, empty slots
    remaining, pending slots and idle tasks remaining from previous info. The total time
    taken would be total tasks + idle tasks.

Time (Approach 1):   O(N + 2Nlog26) ~ O(3N) => O(N)
Space (Approach 1):   O(26k) => O(1)

Time (Approach 2):  O(N)
Space (Approach 2): O(26) => O(1)
where N is the number of tasks

--- Passed all testcases successfully on leetcode.
'''


from heapq import heappush as insert
from heapq import heappop as remove

class FrequencyMap:
    
    #   class with character and corresponding frequency
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        
    #   custom <, >, = operators to put in Max Heap
    def __lt__(self, other):
        if (self.freq == other.freq):
            return ord(self.char) > ord(other.char)
        return self.freq > other.freq
    
    def __gt__(self, other):
        if (self.freq == other.freq):
            return ord(self.char) < ord(other.char)
        return self.freq < other.freq 
    
    def __eq__(self, other):
        return (self.char == other.char and self.freq == other.freq)

class TaskSchedulerHeap:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        
        #   initializations
        frequencyMap = {}
        T = len(tasks)
        maxHeap = []
        time = 0
        
        #   fill frequency map
        for task in tasks:
            if task in frequencyMap:
                frequencyMap[task] += 1
            else:
                frequencyMap[task] = 1
         
        #   insert all frequency map info into the Heap       
        for char in frequencyMap:
            charFreq = FrequencyMap(char, frequencyMap[char])
            insert(maxHeap, charFreq)
        
        #   iterate until nothing is left in Heap    
        while (len(maxHeap) > 0):
            
            #   to calculate cooldown time
            tempTime = 0
            bufferList = []
            
            #   iterate cooldown time ends
            while (tempTime <= n):
                
                #   If any element in Heap
                if (len(maxHeap) > 0):
                    maxCharFreq = maxHeap[0]
                    if (maxCharFreq.freq > 1):          #   if frequency > 1
                        maxCharFreq.freq -= 1
                        bufferList.append(maxCharFreq)  #   add to buffer list
                    remove(maxHeap)                     #   remove max element anyway
                
                time += 1                               #   increment overall time
                
                #   if nothing exists in both Heap and buffer list => we're done
                if (len(maxHeap) == 0 and len(bufferList) == 0):
                    break
                 
                #   increment twmp time until <= cooldown time   
                tempTime += 1
            
            #   now after cooldown, add each entry from Buffer list to Max Heap   
            for eachEntry in bufferList:
                insert(maxHeap, eachEntry)
        
        #   return overall time        
        return time
        
        
class TaskSchedulerNormal:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        
        #   initializations
        frequencyMap = {}
        maxFreq = 0
        maxFreqCount = 0
        N = len(tasks)
        
        #   fill frequency map and get max occurrence frequency in parallel
        for task in tasks:
            if task in frequencyMap:
                frequencyMap[task] += 1
            else:
                frequencyMap[task] = 1
                
            if frequencyMap[task] > maxFreq:
                maxFreq = frequencyMap[task]
                maxFreqCount = 1
            
            elif frequencyMap[task] == maxFreq:
                maxFreqCount += 1
        
        #   calculate number of partitions possible using max frequency       
        partitionsCount = maxFreq - 1
        
        #   calculate empty slots using partitions, cooldown period and max freq occurrence count
        emptySlots = partitionsCount * (n - (maxFreqCount - 1))
        
        #   calculate pending tasks from total tasks, max frequency and number of times it occurred
        pendingTasks = N - (maxFreq * maxFreqCount)
        
        #   calculate idle slots from empty slots and pending tasks
        idleSlots = max(0, emptySlots - pendingTasks)
        
        #   total time would be idle tsaks + total tasks
        return N + idleSlots