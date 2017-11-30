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


class Job():
    def __init__(self, type, arrival_time, buffer):
        self.type = type
        self.priority = self.set_priority(type)
        self.finished = False
        self.arrival_time = arrival_time
        self.buffer = buffer
        self.buffer_pos = 0
        self.t2_status = ''

    def set_priority(self, type):
        if type == 1:
            return 3
        elif type == 2:
            return 2
        elif type == 3:
            return 1

    def update(self):
        if self.type == 1:
            self.buffer[self.buffer_pos] = 1
            self.buffer_pos += 1
        elif self.type == 2:
            self.t2_status += 'N'
        elif self.type == 3:
            self.buffer[self.buffer_pos] = 3
            self.buffer_pos += 1

        if self.buffer_pos == 3 or len(self.t2_status) == 10:
            self.finished = True

    def print_buffer(self):
        if self.type == 1 or self.type == 3:
            temp = ''.join(str(x) for x in self.buffer)
            print("T{0} {1} T{0}".format(self.type, temp))
        else:
            print("T{0} {1} T{0}".format(self.type, self.t2_status))


# Creates n random jobs in the form (arrival time, job type) and returns them as a list of tuples
def random_jobs(n, max_arrival):
    jobs = []
    # Use sampling so we cannot have two jobs arrive at the same time
    arrivals = random.sample(range(1, max_arrival), k=n)

    for i in range(n):
        # Get a random job number
        job = random.randint(1, 3)
        # Get a random arrival time
        arrival = arrivals[i]
        # Add the new tuple to the list of jobs
        jobs.append((arrival, job))

    # Sort the jobs in ascending arrival time
    jobs.sort()
    return jobs


def process_jobs(jobs):
    # T1 and T3 buffer
    buffer = [0, 0, 0]
    job_stack = []  # type: list[Job]
    preempt_stack = []  # type: list[Job]
    arrival_queue = []  # type: list[Job]

    # Create a job object for each job
    for job in jobs:
        job_stack.append(Job(job[1], job[0], buffer))

    # Reverse them so it becomes a stack
    job_stack.sort(key=lambda x: x.arrival_time, reverse=True)
    # for thing in job_stack:
    #    print(thing.arrival_time, thing.type)

    # Skip to the first job
    current_job = job_stack.pop()
    time = current_job.arrival_time

    # Make sure all jobs are completed
    while len(job_stack) > 0 or len(preempt_stack) > 0 or len(arrival_queue) > 0:
        # Handle a new job if it arrived
        if len(job_stack) > 0 and time == job_stack[len(job_stack) - 1].arrival_time:
            # Temporarily keep the arrived job available
            arrived_job = job_stack.pop()
            # Check if the arrived job can preempt the current job
            if check_preempt(arrived_job, current_job):
                # Print the current buffer before preempting
                print("Time {0}, Preempting T{1} with T{2}, Buffer: ".format(time, current_job.type, arrived_job.type),
                      end='')
                current_job.print_buffer()
                # Switch the jobs
                preempt_stack.append(current_job)
                current_job = arrived_job
            # Otherwise put it in a priority queue
            else:
                arrival_queue.append(arrived_job)
                arrival_queue.sort(key=lambda x: x.priority)

        current_job.update()
        time += 1
        if current_job.finished:
            print("Time{0}, ".format(time - 1), end='')
            current_job.print_buffer()
            if len(preempt_stack) > 0:
                current_job = preempt_stack.pop()
            elif len(arrival_queue) > 0:
                current_job = arrival_queue.pop()
            else:
                current_job = job_stack.pop()
                time = current_job.arrival_time


def check_preempt(arrival, current):
    if arrival.type == 1 and current.type == 2:
        return True
    elif arrival.type == 2 and current.type == 3:
        return True
    else:
        return False


def main():
    # Predefined job sequence
    jobs = [(1, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (26, 1)]
    print('Starting job sequence: {0}'.format(jobs))
    process_jobs(jobs)

    # Random job sequence
    jobs = random_jobs(10, 20)
    print('\nStarting random job sequence: {0}'.format(jobs))
    process_jobs(jobs)


if __name__ == '__main__':
    main()
