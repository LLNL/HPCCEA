import sys 
import json
import os
import requests
import glob
#import schedule 
import shutil
import time 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

#global variable to pass into respective functions, assume root directory
path = "~/"

def submit(job_file):
    global path
    header = {'X-SLURM-USER-NAME':os.environ['USER'],'X-SLURM-USER-TOKEN':os.environ['SLURM_JWT'],'Content-Type': 'application/json'}
    url = "http://192.168.95.1:5432/slurm/v0.0.36/job/submit"
    file = open(job_file).read()
    res = requests.post(url, headers=header,data=file)
    res_json = res.json()
    if (len(res_json.get("errors"))==0):
        print("Job Submitted: ")
        print("Job ID       : ", res_json.get("job_id"))
        return True
    else:
       print("Errors: ", res_json.get("errors"))


def main():
    #print(sys.argv)
    header = {'X-SLURM-USER-NAME':os.environ['USER'],'X-SLURM-USER-TOKEN':os.environ['SLURM_JWT'],'Content-Type': 'application/json'}

    if (sys.argv[1] == "submit"):
       return_code = submit(sys.argv[2])       

    if (sys.argv[1] == "delete"):
       print(url)
       res = requests.delete(url, headers=header)
       print(res.json())

    if (sys.argv[1] == "status"):
       url = "http://192.168.95.1:5432/slurm/v0.0.36/job/%s" % sys.argv[2]
       #print(url)
       res = requests.get(url, headers = header)
       #print(res.json())
       status = res.json().get("jobs")
       print("Job Name  : ", status.get("name"))
       print("Nodes     : ", status.get("nodes"))
       print("Job State : ", status.get("job_state"))
       print("Job ID    : ", status.get("job_id"))
       print("Cluster   : ", status.get("cluster")) 
       print("\n")
       

    if (sys.argv[1] == "jobs"):
       url = "http://192.168.95.1:5432/slurm/v0.0.36/jobs"
       res = requests.get(url, headers = header)
       
       #print(type(header))
       jobs = res.json().get("jobs")
       for x in jobs:
           print("Cluster:    ", x.get('cluster'))
           print("Batch Host: ", x.get('batch_host'))
           print("Job Flags:  ", x.get('flags'))
           print("Job State:  ", x.get('job_state'))
           print("Job Name:   ", x.get('name'))
           print("Nodes:      ", x.get('nodes'))
           print("Directory:  ", x.get('current_working_directory'))
           print("Time Limit: ", x.get('time_limit'), "\n")
       #print(res.json().get("jobs")[0])
       #print(type(res.json().get("jobs")[0]))

    if (sys.argv[1] == "diag"):
       print("retrieving diagnostics")
       url = "http://192.168.95.1:5432/slurm/v0.0.36/diag"
       res = requests.get(url, headers = header)
       stats = res.json().get("statistics")
       print("Jobs Submitted: ", stats.get("jobs_submitted"))       
       print("Jobs Started  : ", stats.get("jobs_started"))
       print("Jobs Completed: ", stats.get("jobs_completed"))
       print("Jobs Cancelled: ", stats.get("jobs_cancelled"))
       print("Jobs Failed   : ", stats.get("jobs_failed"))
       print("Jobs Pending  : ", stats.get("jobs_pending"))
       print("Jobs Running  : ", stats.get("jobs_running"), "\n")

    if (sys.argv[1] == "nodes"):
       print("")
       url = "http://192.168.95.1:5432/slurm/v0.0.36/nodes"
       res = requests.get(url, headers = header)
       print(res.json())
       nodes = res.json().get("nodes")
       for x in nodes: 
           print("Name   : ", x.get("name"))
           print("Address: ", x.get("address"))
           print("State  : ", x.get("state"), "\n")

    if (sys.argv[1] == "node"):
       print("retrieving information on node %:" % sys.argv[2])
       url = "http://192.168.95.1:5432/slurm/v0.0.36/node/%s" %sys.argv[2]
       res = requests.get(url, headers = header)
       print(res.json())
       node = res.json().get("nodes")
       print("Name   : ", x.get("name"))
       print("Address: ", x.get("address"))
       print("State  : ", x.get("state"), "\n")


    if (sys.argv[1] == "partitions"):
       print("retrieving all partitions")
       url = "http://192.168.95.1:5432/slurm/v0.0.36/partitions"
       res = requests.get(url, headers = header)
       print(res.json())
       partitions = res.json().get("partitions")
       for x in partitions:
           print("Name   :", x.get("name"))
           print("Nodes  :", x.get("nodes"), "\n")

    if (sys.argv[1] == "partition"):
       print("retrieving partition %s" %sys.argv[2])
       url = "http://192.168.95.1:5432/slurm/v0.0.36/partition/%s" %sys.argv[2]
       res = requests.get(url, headers = header)
       print(res.json())   
       partitions = res.json().get("partitions")
       print("Name   :", x.get("name"))
       print("Nodes  :", x.get("nodes"), "\n")

    def test_job():
       print("hello")
 
    def routine_check():
       global path
       print("Routine check")
       url = "http://192.168.95.1:5432/slurm/v0.0.36/jobs"
       res = requests.get(url, headers = header)
       jobs = res.json().get("jobs")

       folder = [] 
       for file in os.listdir(path):
           if file.endswith(".json"):
              folder.append(file)
       print(folder)
       if (len(jobs) ==0):
          print("No more jobs in queue")
          if (len(folder) > 0):
              job_file = folder.pop(0)
              print("Submitting job: %s" %job_file)
              return_code = submit(job_file)
              if (return_code == True):
                  #Move file to compelted folder
                  shutil.move(path + job_file, "completed_jobs")
                  folder_c = []
                  for file in os.listdir("completed_jobs"):
                      folder_c.append(file)
                  print("Completed Jobs/Already Submitted")
                  print(folder_c)
                  print("\n")
              else: 
                  print("Error in submitting job") 
          else: 
              scheduler.shutdown()
       else: 
          #slurm naturally holds completed jobs for a small period after 
          #completion, it is necessary to iterate over the jobs to confirm 
          #that they are all completed and/or there isn't a job still running
          active_job = False
          for job in jobs: 
              if (job.get("job_state") != "COMPLETED"):
                 output = "Job still in progress: %s" % job.get("job_id")
                 print(output)
                 active_job = True
          if (not active_job):
              if (len(folder) > 0):
                  job_file = folder.pop(0)
                  print("Submitting job: %s" %job_file)
                  return_code = submit(job_file)
                  if (return_code == True):
                      #Move file to compelted folder
                      shutil.move(path + job_file, "completed_jobs")
                      folder_c = []
                      for file in os.listdir("completed_jobs"):
                          folder_c.append(file)
                      print("Completed Jobs/Already Submitted")
                      print(folder_c)
                  else:
                      print("Error in submitting job")

    if (sys.argv[1] == "batch"):
       #print("Running jobs located in: %s" %sys.argv[2])
       global path
       path = sys.argv[2]
       #print(path)
       #for file in os.listdir(sys.argv[2]):
           #if file.endswith(".json"):
              #print(file)       

       #check for existence of completed job folder, create if absent
       if not os.path.exists("completed_jobs"):
          os.mkdir("completed_jobs")

       #shutil.move(sys.argv[2] + 'test.json', 'completed_jobs')
       scheduler = BlockingScheduler()
       #scheduler.add_job(test_job, 'interval', seconds=5)
       scheduler.add_job(routine_check ,'interval', seconds=5)

       #schedulerBack = BackgroundScheduler()
       #schedulerBack.add_job(routine_check(sys.arg[v]), 'interval', minutes=30)

       try:
           print(os.getpid())
           while True:
               scheduler.start()
               #schedulerBack.start()
       except(KeyboardInterrupt, SystemExit):
           scheduler.shutdown()
           #schedulerBack.shutdown()



if __name__ == "__main__":
   main()
