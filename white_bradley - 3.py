'''
Bradley White
Programming 3: Priority Inversion
CSCI-460: Operating Systems
December 2, 2017

Interpreter: Python 3.6.3
Inputs: None
Outputs: Console
'''

import random


# Class which handles a priority job system
class Job():
    def __init__(self, type, arrival_time, buffer):
        # The jobs type, can be 1,2,3
        self.type = type
        # A jobs priority, can be 3,2,1
        self.priority = self.set_priority(type)
        # Keep track if this job has finished
        self.finished = False
        # When this job will arrive
        self.arrival_time = arrival_time
        # Shared buffer reference between type 1 and 3 jobs
        self.buffer = buffer
        # This jobs current position in the buffer
        self.buffer_pos = 0
        # Current status if this is a type 2 job
        self.t2_status = ''

    # Helper to set the correct priority based on a jobs type
    def set_priority(self, type):
        if type == 1:
            return 3
        elif type == 2:
            return 2
        elif type == 3:
            return 1

    # Update the buffer or status depending on the job type
    def update(self):
        if self.type == 1:
            self.buffer[self.buffer_pos] = 1
            self.buffer_pos += 1
        elif self.type == 2:
            self.t2_status += 'N'
        elif self.type == 3:
            self.buffer[self.buffer_pos] = 3
            self.buffer_pos += 1

        # If we reached the end of the buffer or checking all status' this job is finished
        if self.buffer_pos == 3 or len(self.t2_status) == 10:
            self.finished = True

    # Join the buffer into a string and print its current value
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


# Algorithm to handle processing jobs based on priority, preempts if necessary
def process_jobs(jobs):
    # T1 and T3 buffer
    buffer = [0, 0, 0]
    # Keep track of the status of the buffer
    buffer_lock = False
    # Beginning stack of all jobs, the type: comment below is for IDE code completion
    job_stack = []  # type: list[Job]
    # Jobs which are preempt are pushed onto this stack
    preempt_stack = []  # type: list[Job]
    # Jobs which are lower priority than the current job are pushed into the queue, sorted by priority
    arrival_queue = []  # type: list[Job]

    # Create a job object for each job
    for job in jobs:
        job_stack.append(Job(job[1], job[0], buffer))

    # Reverse them so it becomes a stack
    job_stack.sort(key=lambda x: x.arrival_time, reverse=True)

    # Skip to the first job's arrival time
    current_job = job_stack.pop()
    time = current_job.arrival_time
    if current_job.type == 1 or current_job.type == 3:
        buffer_lock = True

    # Make sure all jobs are completed before exiting
    while len(job_stack) > 0 or len(preempt_stack) > 0 or len(arrival_queue) > 0:
        # Handle a new job if it arrived
        if len(job_stack) > 0 and time == job_stack[len(job_stack) - 1].arrival_time:
            # Temporarily keep the arrived job available
            arrived_job = job_stack.pop()
            # Check if the arrived job can preempt the current job
            if check_preempt(arrived_job, current_job, buffer_lock):
                # Print the current buffer before preempting
                print("Time {0}, Preempting T{1} with T{2}, Buffer: ".format(time, current_job.type, arrived_job.type),
                      end='')
                current_job.print_buffer()
                # Switch the jobs and put the old job on a separate stack
                preempt_stack.append(current_job)
                current_job = arrived_job
            # Otherwise put it in a priority queue
            else:
                arrival_queue.append(arrived_job)
                # Sort again to maintain priority
                arrival_queue.sort(key=lambda x: x.priority)

        # Update the buffer for the current job, and increment time
        current_job.update()

        # If the job finished, find the next one with the following priority: previously preempt,
        # priority from arrival queue, or lastly skipping time to the next arriving job
        if current_job.finished:
            print("Time {0}, ".format(time), end='')
            current_job.print_buffer()
            if len(preempt_stack) > 0:
                current_job = preempt_stack.pop()
                print("Time {0}, Resuming Preempt T{1}".format(time, current_job.type))
            elif len(arrival_queue) > 0:
                current_job = arrival_queue.pop()
            else:
                current_job = job_stack.pop()
                time = current_job.arrival_time

            if current_job.type == 1 or current_job.type == 3:
                buffer_lock = True
            else:
                buffer_lock = False

        time += 1


# Check if a job can preempt another
def check_preempt(arrival, current, buffer_lock):
    # Type 1 jobs can preempt type 2
    if arrival.type == 1 and current.type == 2 and buffer_lock == False:
        return True
    # Type 2 jobs can preempt type 3
    elif arrival.type == 2 and current.type == 3:
        return True
    # Otherwise, let the current job continue
    else:
        return False


# Create some jobs to process
def main():
    # Predefined job sequence
    jobs = [(1, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (26, 1)]
    print('Starting predefined job sequence: {0}'.format(jobs))
    process_jobs(jobs)

    # Random job sequence
    jobs = random_jobs(10, 20)
    print('\nStarting random job sequence: {0}'.format(jobs))
    process_jobs(jobs)


if __name__ == '__main__':
    main()
