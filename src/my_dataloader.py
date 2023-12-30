import asyncio
import time

from torch.utils.data import DataLoader




        

class MyAsyncIterableClass():
    def __init__(self, dataset):
        self.data = dataset
        self.next_item = None #holds the data 
        self.sampler = None # this is sampling strategy (how to sample, torch currently supports randomsampling)
        #we can just create a generator that is mimicking this sampler

    def __aiter__(self):
        # this thing returns an iterable. 
        #if we are having random sampling then we need to reinitialse the sampler with different seed
        print("aiter")
        # here itself we will load the next first data object in the ram, 
        return self

    async def __anext__(self):
        # This method is called during asynchronous iteration to get the next element
        # we will copy the next_item data in a local variable, and then start fetching next data point asynchronously and return the local variable
        pass

# Example usage:
async def main():
    my_async_iterable_instance = MyAsyncIterableClass([1, 2, 3, 4, 5])

    # Using an asynchronous for loop to iterate over the elements
    for _ in range(3):
        async for item in my_async_iterable_instance:

            print(item)
# Run the asynchronous event loop
start = time.time()
asyncio.run(main())
print(f"it took {time.time() - start} to finish the task")