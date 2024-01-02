import asyncio
import time

from torch.utils.data import DataLoader




        

class MyAsyncIterableClass():
    def __init__(self, dataset):
        self.data = dataset
        self.next_item = None #holds the data 
        self.sampler = None # this is sampling strategy (how to sample, torch currently supports randomsampling)
        self.current_index=0        
        #we can just create a generator that is mimicking this sampler

    def __aiter__(self):
        # this thing returns an iterable. 
        #if we are having random sampling then we need to reinitialse the sampler with different seed
        self.current_index = 0
        self.task = asyncio.create_task(self.load_next_item())        
        print("started aiter")
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
        self.next_item = self.data[self.current_index]
        # asyncio.sleep(3)
        self.current_index+=1
        print(f"curr index : {self.current_index}")
        print("done with next item")


# Example usage:
async def main():
    my_async_iterable_instance = MyAsyncIterableClass([1, 2, 3, 4, 5])
    idx =0
    # Using an asynchronous for loop to iterate over the elements
    for _ in range(1):
        async for item in my_async_iterable_instance:
            print(f'we are in a loop right now with {idx}')
            idx+=1
            time.sleep(3)
            print(item)
            print("finished the loop")
# Run the asynchronous event loop
start = time.time()
asyncio.run(main())
print(f"it took {time.time() - start} to finish the task")