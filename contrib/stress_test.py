#!/usr/bin/python
"""
This script will stress test the uniqueID server as a client.

This will help implementers determine if their deployment of the uniqueID
service is indeed producing uniqueIDs for every request.
"""
import Queue
import threading
import os
import requests


def main():
    """Main method to start the processing of work."""
    uniqueid_url = os.getenv('UNIQUEID_URL', 'http://localhost:8051')
    max_work = 4
    workqueue = Queue.Queue(max_work)
    respqueue = Queue.Queue(max_work)
    session = requests.session()
    retry_adapter = requests.adapters.HTTPAdapter(max_retries=5)
    session.mount('http://', retry_adapter)
    session.mount('https://', retry_adapter)

    def work():
        """
        The main worker thread.

        Pull the job from the workqueue and query the url.
        Then send the results to the response queue.
        """
        job = True
        while job:
            job = workqueue.get()
            if not job:
                workqueue.task_done()
                break
            resp = session.get('{}/getid?range=1&mode=test'.format(uniqueid_url))
            respqueue.put({'resp': resp.json()['endIndex'], 'job': job})
            workqueue.task_done()

    def respwork():
        """
        Response worker thread.

        Pull the responces off the response queue and save them to a file.
        """
        resp = True
        data_log = open('job_uniqueid.csv', 'w')
        bufsize = 1024*1024
        buf = ''
        while resp:
            resp = respqueue.get()
            if not resp:
                respqueue.task_done()
                break
            buf += '{resp},{job}\n'.format(**resp)
            if len(buf) > bufsize:
                data_log.write(buf)
                buf = ''
        data_log.close()

    # start the threads
    # pylint: disable=unused-variable
    for i in range(max_work):
        workt = threading.Thread(target=work)
        workt.daemon = True
        workt.start()
    # pylint: enable=unused-variable
    respt = threading.Thread(target=respwork)
    respt.daemon = True
    respt.start()

    # do the work
    for job_id in range(1000):
        workqueue.put(job_id)

    # end the work
    for i in range(max_work):
        workqueue.put(False)
    workqueue.join()
    respqueue.put(False)
    respqueue.join()


if __name__ == '__main__':
    main()
