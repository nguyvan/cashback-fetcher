from cronjob import job

if __name__ == "__main__":
    # Schedule the job to run every day at a specific time
    print("Scheduling job...")
    job()
    print("finished scheduling job.")