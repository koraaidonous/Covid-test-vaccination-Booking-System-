import grpc
import pika

import clinic_control_pb2
import clinic_control_pb2_grpc
from concurrent import futures
import datetime
from threading import Thread
import pickle


class ClinicCtrl(clinic_control_pb2_grpc.ClinicCtrlServicer):

    def getVacHistory(self, request, context):
        vac_hs = []
        with open("InfoVacc.txt", "r") as f:
            for line in f:
                vac_info = line.split(" ")
                if int(vac_info[0]) == request.hs_num:
                    r = line.strip()
                    vac_hs.append(r)
        return clinic_control_pb2.vacFile(vaccines=vac_hs)

    def getAppointment(self, request, context):
        # Retrieves the most recent appointment
        appt = ""
        with open("InfoApt.txt", "r") as f:
            for line in f:
                vac_info = line.split(" ")
                #print(vac_info)
                if int(vac_info[0]) == request.hs_num:
                    appt = line.strip()
        return clinic_control_pb2.appointmentFile(appointment=appt)

    def getCovidResults(self, request, context):
        #Retrieves Covid Results
        with open("InfoTest.txt", "r") as f:
            for line in f:
                test_info = line.split(" ")
                if int(test_info[0]) == request.hs_num:
                    test = int(test_info[1].strip())

        return clinic_control_pb2.resultsFile(results=test)


def getBooking():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Booking-Clinic-Queue')

    def callback(ch, method, properties, body):
        print(" [x] Received booking %r" % body)
        booking = pickle.loads(body)
        #Save appointment to InfoApt.txt
        toWrite = str(booking["hs_num"])+" "+booking["clinic"]+" "+booking["date"]
        with open("InfoApt.txt","w") as aptf:
            aptf.write(toWrite+"\n")
        aptf.close()

    channel.basic_consume(queue='Booking-Clinic-Queue', on_message_callback=callback, auto_ack=True)
    print(" [x] Waiting for booking messages.")
    channel.start_consuming()


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    clinic_control_pb2_grpc.add_ClinicCtrlServicer_to_server(ClinicCtrl(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    thread1 = Thread(target=run)
    thread2 = Thread(target=getBooking)
    print("run server threads")
    thread1.start()
    thread2.start()