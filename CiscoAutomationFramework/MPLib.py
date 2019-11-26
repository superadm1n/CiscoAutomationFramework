from multiprocessing import cpu_count, Process, Queue, Event
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from inspect import signature
from types import FunctionType

class ParameterError(Exception):
    pass

class NetThread(Thread):
    '''
    This is the thread that will be spun up by the worker process to execute the
    function
    '''

    def __init__(self, job, job_args,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = job
        self.job_args = job_args
        self.output = None
        self.start_time = datetime.now()

    def run(self):
        self.output = self.job(*self.job_args)

class ClearToStop:
    '''
    Class that represents the stop command for a worker process

    Pass this class into the queue and when it processes it, the worker will shut down
    '''
    pass

class Job:
    '''Class that is designed to act as a job object for the worker process below'''

    def __init__(self, target, *args):
        self.target = target
        self.arguments = args
        self.output = None


class WorkerProcess(Process):
    '''General Purpose Process that is able to take a function + arguments
    as its input, explode that function, and put its output in an output buffer'''

    def __init__(self, worker_thread_timeout, num_of_threads=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_queue = Queue()
        self.output_buffer = Queue()
        self.running_jobs = []
        self.num_of_threads = num_of_threads
        self.worker_thread_timeout = worker_thread_timeout

        self.exit = Event()

    def shutdown_worker(self):
        '''Call this method to shut down the process'''
        self.exit.set()

    def submit_job(self, job):
        '''Call this method to submit a job to the process'''
        self.job_queue.put(job)

    def get_completed_jobs(self):
        '''Call this method to get all of the completed jobs from the output buffer'''
        data = []
        while not self.output_buffer.empty():
            data.append(self.output_buffer.get())
        return data

    def _grab_and_start_job(self):
        '''Grabs a job from the input queue and starts it in its new thread.

        :return:
        '''

        # grab job from queue
        job = self.job_queue.get(timeout=1)
        # validate type is job
        if type(job) is ClearToStop:
            self.exit.set()

        if type(job) is not Job:
            return
        # Start thread that executes job
        thread = NetThread(job=job.target, job_args=job.arguments)
        thread.start()
        # Add job and thread to our list to keep track
        self.running_jobs.append({'job': job, 'thread': thread})

    def _prune_jobs(self):
        '''Method to check if a thread has returned data, if it has grab
        the data, place it in the output buffer, and remove it from the
        running_jobs tracking list

        :return:
        '''
        for thd in self.running_jobs:
            # If thread has data Grab output from executed thread and put it into the jobs output attribute
            # put the job in the output queue and remove the job from out running_jobs tracking list
            if thd['thread'].output is not None:
                thd['job'].output = thd['thread'].output
                self.output_buffer.put(thd['job'])
                self.running_jobs.remove(thd)

            # If the thread has been running longer than expected. Kill it off
            if (datetime.now() - thd['thread'].start_time) > timedelta(seconds=self.worker_thread_timeout):
                thd['thread'].kill()
                self.running_jobs.remove(thd)

    def run(self):

        while not self.exit.is_set():
            sleep(1)
            if len(self.running_jobs) >= self.num_of_threads:
                # Only run 10 threads
                continue
            if self.job_queue.empty():
                # If there are no jobs pending there is no reason to process further
                continue

            self._grab_and_start_job()
            self._prune_jobs()

        while len(self.running_jobs) != 0:
            self._prune_jobs()
            sleep(.01)


def init_workers(list_of_jobs, worker_thread_timeout, num_processes=(cpu_count() - 1), num_threads_per_proc=20):
    '''Starts the worker processes and loads the jobs into them.

    :param list_of_jobs: List of job objects
    :param num_processes: Number of processes (default num of procs-1)
    :param num_threads_per_proc:
    :return:
    '''

    # Start worker processes
    workers = []
    for x in range(num_processes):
        wkr = WorkerProcess(num_of_threads=num_threads_per_proc, worker_thread_timeout=worker_thread_timeout)
        wkr.start()
        workers.append(wkr)

    # load jobs into each of the workers
    count = 0
    for job in list_of_jobs:
        workers[count].job_queue.put(job)
        count += 1
        if count == len(workers):
            count = 0

    # Send signal to stop processes at end of the queue
    for worker in workers:
        sig = ClearToStop()
        worker.job_queue.put(sig)

    return workers


def parallel_process(list_of_jobs, num_processes=(cpu_count() - 1), num_threads_per_proc=20, data_handler=None, worker_thread_timeout=60):
    '''Accepts a list of job objects, starts the worker processes, load them with the jobs and handles gathering
    the data from each of those jobs.

    You can also pass in a data_handler so you can handle each of the processes data as it is returned vs
    waiting til they all return

    :param list_of_jobs: List of unexecuted functions that are to be carried out by the worker processes
    :param num_processes: Total number of worker process to run, this should most often be left at default (total cpu count - 1)
    :param num_threads_per_proc: Number of threads each process should spin up to share the processing power of that core
    :param data_handler: Unexecuted function that is a callback to handle the data as it is returned from each process
    :return:
    '''

    if data_handler:
        if type(data_handler) != FunctionType:
            raise TypeError('Data handler must be a function')
        if len(signature(data_handler).parameters) != 1:
            raise ParameterError('Data Handler Must accept 1 parameter')

    workers = init_workers(list_of_jobs, worker_thread_timeout, num_processes, num_threads_per_proc)
    data_to_return = []
    while True:
        if len(workers) == 0:
            break

        for worker in workers:
            if not worker.is_alive():
                workers.remove(worker)
                if len(workers) == 0:
                    # break out of for loop if there are no workers left
                    break
                continue

            if worker.output_buffer.empty():
                continue

            data = worker.output_buffer.get().output
            if data is not None:
                if data_handler:
                    data_handler(data)
                data_to_return.append(data)
    return data_to_return

