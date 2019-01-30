#import sensor_sim
import time

f = open('sim.csv', 'r')
task_count = 1
for line in f:
    line = line.rstrip('\n').split(',')

    spot_id = line[0]
    task_id = line[1]
    user_id = line[2]
    delay   = float(line[3])

    print("Task Number: %d\nDelay = %f" % (task_count,delay))
    task_count = task_count + 1
    time.sleep(delay)
    if(task_id == 'takespot'):
        print("Task: %s\nUser: %s\nSpot: %s\n" % (task_id,user_id,spot_id))
    else:
        print("Task: %s\nUser: %s\nSpot: %s\n" % (task_id,user_id,spot_id))

