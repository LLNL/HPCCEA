from flux_restful_client.main import get_client
import json
from time import sleep

cli = get_client()

res = cli.submit(command='sleep 60')
if res and 'detail' not in res: # second clause of 'and' operator is when user is authenticated
    jobid = res['id']
    print('\n\n---------Current status of the sleep job---------\n\n')
    print(json.dumps(cli.jobs(jobid), indent=4))
    sleep(0.5)
    print('\n\n---------Start cancelling the job now---------\n\n')
    res = cli.cancel(jobid)    
    print(json.dumps(res, indent=4))
    print('\n\n---------Wait for 3 seconds for Flux to clean up the canceled job---------\n\n')
    sleep(5)
    res = cli.jobs(jobid) # check for job status
    # You'll see the status being "CANCELED"
    print(json.dumps(res, indent=4))