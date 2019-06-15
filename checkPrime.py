import math, time
from multiprocessing import Process, Queue, cpu_count


def checkPrimalityWithRange(queue,possiblePrime,lowRange,highRange):
    isPrime = True
    for divisor in range(lowRange,highRange):
        if possiblePrime%divisor == 0:
            isPrime = False
            break
    queue.put(isPrime)


if __name__ == '__main__':

    MAX_NUMBER_OF_PROCESSES = cpu_count()
    primalityResults = []
    queue = Queue()

    print("Program start!")
    numberToCheckPrimality = int(input("Enter an integer number to check its primality: "))
    programStartTime = time.time()

    intervalPerProcess = (math.sqrt(numberToCheckPrimality)-1)/MAX_NUMBER_OF_PROCESSES
    processes = []
    currentIntervalStart = 2

    for i in range(MAX_NUMBER_OF_PROCESSES):
        currentProcess = Process(target=checkPrimalityWithRange, args=[queue,
                                                                        numberToCheckPrimality,
                                                                        round(currentIntervalStart),
                                                                        round(currentIntervalStart+intervalPerProcess)
                                                                        ])
        processes.append(currentProcess)
        currentProcess.start()
        currentIntervalStart = currentIntervalStart + intervalPerProcess

    for process in processes:
        process.join()

    while not queue.empty():
        primalityResults.append(queue.get())

    if False in primalityResults:
        print("The number is NOT prime.")
    else:
        print("The number IS prime.")
    print("Program executed in ",end="")
    print(time.time()-programStartTime," seconds.", end="", sep="")
