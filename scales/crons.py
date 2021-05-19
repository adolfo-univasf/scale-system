from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['17:09']


    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'scales.my_cron_job'    # a unique code

    def do(self):
        print("Rodei")
        pass    # do your thing here