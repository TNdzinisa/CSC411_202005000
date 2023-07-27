import threading
import time
import random
import xml.etree.ElementTree as ET

sem = threading.Semaphore()

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.empty = threading.Semaphore(size)
        self.full = threading.Semaphore(0)
        self.mutex = threading.Lock()

    def put(self, item):
        self.empty.acquire()
        self.mutex.acquire()
        self.buffer.append(item)
        self.mutex.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.mutex.acquire()
        item = self.buffer.pop(0)
        self.mutex.release()
        self.empty.release()
        return item

class ITstudents:
    def __init__(self):
        self.name = ''.join(random.choices(['Thabo','Puu','Nozipho','Tandzile','Nipho','Lee','Nkosi','Samu','Mossi','Terrie']))
        self.id = random.randint(20230000, 20230011)
        self.programme = ''.join(random.choices(['BSc', 'BSc.IT', 'BSc Geographic Science'], weights=[3, 2, 1]))
        self.courses = {'CSC493': random.randint(50, 100), 'CSC405': random.randint(50, 100), 'CSC461': random.randint(50, 100), 'CSC433': random.randint(50, 100), 'CSC411': random.randint(50, 100), 'CSC400': random.randint(50, 100)}

    def to_xml(self):
        root = ET.Element('root')
        doc = ET.SubElement(root, 'doc')
        ET.SubElement(doc, 'name').text = self.name
        ET.SubElement(doc, 'id').text = str(self.id)
        ET.SubElement(doc, 'programme').text = self.programme
        courses_elem = ET.SubElement(doc, 'courses')
        for course_name, mark in self.courses.items():
            course_elem = ET.SubElement(courses_elem, 'course')
            ET.SubElement(course_elem, 'name').text = course_name
            ET.SubElement(course_elem, 'mark').text = str(mark)

        tree = ET.ElementTree(root)
        tree.write(f'student{random.randint(1, 10)}.xml')





def producer(buffer):
    print(f"PRODUCER  ==> producer running..................")

    while True:
        #Claim semaphore
        sem.acquire()

        #Action
        it_student = ITstudents()
        it_student.to_xml()
        buffer.put(it_student)

        #Release semaphore
        sem.release()
        time.sleep(1)

def consumer(buffer):
    print(f"CONSUMER  ==> Comsumer running..................")
    while True:

        
      
        #Claim semaphore
        sem.acquire()

        #Action
        it_student = buffer.get()

        average_mark = sum(it_student.courses.values()) / len(it_student.courses)
        
        if average_mark >= 50:
            pass_fail_info = "Pass"
        else:
            pass_fail_info = "Fail"

        print(f"CONSUMER  ==> Name: {it_student.name}, ID: {it_student.id}, Programme: {it_student.programme}, Courses and Marks: {it_student.courses}, Average Mark: {average_mark:.2f}, Pass/Fail: {pass_fail_info}")
        print("")
        #Release semaphore
        sem.release()
        time.sleep(1)
buffer_size = 10
buffer = BoundedBuffer(buffer_size)

producer_thread_1 = threading.Thread(target=producer, args=(buffer,))
##producer_thread_2 = threading.Thread(target=producer, args=(buffer,))
consumer_thread_1 = threading.Thread(target=consumer, args=(buffer,))
##consumer_thread_2 = threading.Thread(target=consumer, args=(buffer,))

producer_thread_1.start()
##producer_thread_2.start()
consumer_thread_1.start()
##consumer_thread_2.start()


