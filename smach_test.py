import rospy
import smach
import smach_ros
from std_msgs.msg import String

def snag(i):
    a = ["objectFound", "objectRight", "routeClear"]
    rospy.loginfo("dir: " + a[i])
    return a[i]

#functions to set up subscriber node
def callback(data):
    rospy.loginfo("direction: " + data.data)
    

def listener():
    rospy.init_node('listner', anonymous=True)
    rospy.Subscriber('topic', String, callback)
    rospy.loginfo(String)
    #rospy.spin()
    #return String#rospy.loginfo('state: ' + data.data)
   # rospy.spin()

#default state
class Scanning(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['objectFound', 'exit'], 
                             input_keys=['counter_in'], 
                             output_keys = ['counter_out'])

    def execute(self, userdata):
        rospy.loginfo('executing state SCANNING')
        if userdata.counter_in < 3:
            state = snag(userdata.counter_in)
        else:
            state = "exit"
        userdata.counter_out = userdata.counter_in + 1
        return state
        #return test_listen()
#        return listener()
#Object has been found...where do we go?
class Deciding(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['objectRight', 'objectLeft', 'objectFound', 'exit'], 
                             input_keys=['counter_in'], 
                             output_keys = ['counter_out'])

    def execute(self, userdata):
        rospy.loginfo('executing state DECIDING')
        if userdata.counter_in < 3:
            state = snag(userdata.counter_in)
        else:
            state = "exit"
        userdata.counter_in = userdata.counter_out + 1
        return state
        

class TurningRight(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['routeClear', 'exit'], 
                             input_keys=['counter_in'], 
                             output_keys = ['counter_out'])

    def execute(self, userdata):
        rospy.loginfo('executing state TURNING RIGHT')
        if userdata.counter_in < 3:
            state = snag(userdata.counter_in)
        else:
            state = "exit"
        userdata.counter_out = userdata.counter_out + 1            
        return state

class TurningLeft(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['routeClear', 'exit'], 
                             input_keys=['counter_in'], 
                             output_keys = ['counter_out'])

    def execute(self, userdata):
        rospy.loginfo('executing state TURNING LEFT')
        #implement
        if userdata.counter_in < 3:
            state = snag(userdata.counter_in)
            
        else:
            state = "exit"
        userdata.counter_out = userdata.counter_in + 1    
        return state
        
def main():

    rospy.init_node('smach__state_machine')
    #create top level SMACH state machine
    sm = smach.StateMachine(outcomes=['last_outcome'])
    #open the container !
    sm.userdata.counter = 0
    with sm:
    #    listener()
        
        #Add states to the container
        smach.StateMachine.add('SCANNING', Scanning(),
                               transitions={'objectFound':'DECIDING', 
                                            'exit':'last_outcome'}, 
                               remapping = {'counter_in':'counter', 
                                            'counter_out':'counter'})

    


        smach.StateMachine.add('DECIDING', Deciding(),
                               transitions={'objectRight':'TURNINGLEFT',
                                            'objectLeft':'TURNINGRIGHT', 
                                            'objectFound':'SCANNING', 
                                            'exit':'last_outcome'}, 
                               remapping = {'counter_in':'counter', 
                                            'counter_out':'counter'}) 
    

        smach.StateMachine.add('TURNINGRIGHT', TurningRight(),
                               transitions={'routeClear':'SCANNING',
                                            'exit':'last_outcome'}, 
                               remapping = {'counter_in':'counter', 
                                            'counter_out':'counter'})

        smach.StateMachine.add('TURNINGLEFT', TurningRight(),
                               transitions={'routeClear':'SCANNING', 
                                            'exit':'last_outcome'}, 
                               remapping = {'counter_in':'counter', 
                                            'counter_out':'counter'})

    outcome = sm.execute()

if __name__ == '__main__':
    main()
