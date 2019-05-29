import math, time
from multiprocessing import Process, Queue

NUMBER_OF_PROCESSES = multiprocessing.cpu_count()

def verifyPrime(queue,lowRange,highRange,number):
    prime = True
    for divisor in range(lowRange,highRange):
        if number%divisor == 0:
            prime = False
            break
    queue.put(prime)


if __name__ == '__main__':
    primes = []
    queue = Queue()
    print("Program start!")
    number = int(input("Enter an integer number to check its primality: "))
    startTime = time.time()
    interval = (math.sqrt(number)-1)/NUMBER_OF_PROCESSES
    processes = []
    currentRangeStart = 2

    for i in range(NUMBER_OF_PROCESSES):
        process = Process(target=verifyPrime,args=[queue,round(currentRangeStart),round(currentRangeStart+interval),number])
        processes.append(process)
        process.start()
        currentRangeStart = currentRangeStart + interval

    antes = time.time()
    for process in processes:
        process.join()

    while not queue.empty():
        primes.append(queue.get())

    if False in primes:
        print("The number is NOT prime.")
    else:
        print("The number IS prime.")
    print("Program executed in ",end="")
    print(time.time()-startTime," seconds.", end="", sep="")
