import csv

def save_to_csv(jobs, filename):
    file = open(filename, 'w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link', 'description'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return