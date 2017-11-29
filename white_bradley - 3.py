'''
Bradley White
Programming 3: Priority Inversion
CSCI-460: Operating Systems
December 2, 2017

Interpreter: Python 3.6.3
Inputs: None
Outputs: Writes to console
'''

import random

# Creates n random jobs in the form (arrival time, job type) and returns them as a list of tuples
def random_jobs(n):
    jobs = []

    for i in range(n):
        # Get a random job number
        job = random.randint(1, 3)
        # Get a random arrival time
        arrival = random.randint(1, 50)
        # Add the new tuple to the list of jobs
        jobs.append((arrival, job))

    # Sort the jobs in ascending arrival time
    jobs.sort()
    return jobs


def main():
    # Predefined job sequence
    jobs = [(1, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (26, 1)]
    print('Starting job sequence: {0}'.format(jobs))

    # Random job sequence
    rand_jobs = random_jobs(10)
    print(rand_jobs)

if __name__ == '__main__':
    main()
