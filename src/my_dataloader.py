import asyncio
import time

from torch.utils.data import DataLoader
import random


def sampler(n):
    numbers = list(range(n))
    
    while True:
        random.shuffle(numbers)
        yield numbers

class MyAsyncIterableClass():
    def __init__(self, dataset, sampler=sampler):
        self.data = dataset
        self.next_item = None #holds the data 
        self.sampler = sampler(len(dataset)) # this is sampling strategy (how to sample, torch currently supports randomsampling)
        self.current_index=0        
        #we can just create a generator that is mimicking this sampler

    def __aiter__(self):
        # this thing returns an iterable. 

        self.current_index = 0
        self.sample = None
        self.sampler = next(self.sampler)
        self.task = asyncio.create_task(self.load_next_item())        
        
        # here itself we will load the next first data object in the ram, 
        return self

    async def __anext__(self):
        if self.current_index>= len(self.data)-1:
            raise StopAsyncIteration
        # This method is called during asynchronous iteration to get the next element
        # we will copy the next_item data in a local variable, and then start fetching next data point asynchronously and return the local variable
        await self.task
        data = self.next_item
        self.task = asyncio.create_task(self.load_next_item())        
        return data

    async def load_next_item(self):
        print('loading next item')
        self.next_item = self.data[self.sampler[self.current_index]]
        self.current_index+=1
        print(f"curr index : {self.current_index}")
        print("done with next item")
