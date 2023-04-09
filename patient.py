from enum import Enum

import grpc
import clinic_control_pb2
import clinic_control_pb2_grpc
import pika
import pickle

#client connection to the server

class cStat(Enum):
        Neg = -1
        ToTest = 0
        Pos = 1


class Patient:
        def __init__(self, hs_num, name, dob):
                self.hs_num = hs_num
                self.name = name
                self.dob = dob
                self.cvd_status = cStat.Neg.value
                self.vac_history = []

        '''def rcv_book_res(self):
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='Response-Queue')

                def callback(ch, method, properties, body):
                        print(" [x] Received %r" % body)
                        book_response = pickle.loads(body)

                channel.basic_consume(queue='Response-Queue', on_message_callback=callback, auto_ack=True)
                print(" [x] Waiting for response to booking.")
                channel.start_consuming() '''



        def book_vaccine(self, vac_type, clinic, date, time):
                # Send to Booking queue of Booking
                book_vac_task = {
                        "book_type": "vaccine",
                        "vac_type": vac_type,
                        "hs_num": self.hs_num,
                        "name": self.name,
                        "dob": self.dob,
                        "clinic": clinic,
                        "date": date,
                        "time": time
                }

                connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='Booking-Queue')

                channel.basic_publish(exchange='', routing_key='Booking-Queue', body=pickle.dumps(book_vac_task))
                print(" [x] Sending book vaccine task.")
                connection.close()

        def book_covid_test(self, clinic, date, time):
                # Send to Booking queue of Booking
                book_test_task = {
                        "book_type": "covid test",
                        "hs_num": self.hs_num,
                        "name": self.name,
                        "dob": self.dob,
                        "clinic": clinic,
                        "date": date,
                        "time": time
                }

                connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='Booking-Queue')

                channel.basic_publish(exchange='', routing_key='Booking-Queue', body=pickle.dumps(book_test_task))
                print(" [x] Sending book vaccine task.")
                connection.close()


        def get_appointment(self):
                # Get appointment from GRPC of Clinic
                with grpc.insecure_channel("localhost:50051", options=(('grpc.enable_http_proxy', 0),)) as channel:
                        stub = clinic_control_pb2_grpc.ClinicCtrlStub(channel)
                        appointment = stub.getAppointment(
                                clinic_control_pb2.appointmentRequest(name=self.name, hs_num=self.hs_num))
                print(appointment.appointment)
                channel.close()

        def getVaccineHistory(self):
                # Get Vaccine History from GRPC of Clinic
                with grpc.insecure_channel("localhost:50051", options=(('grpc.enable_http_proxy', 0),)) as channel:
                        stub = clinic_control_pb2_grpc.ClinicCtrlStub(channel)
                        vac_History = stub.getVacHistory(
                                clinic_control_pb2.vacRequest(name=self.name, hs_num=self.hs_num))
                results = vac_History.vaccines
                for i in range(len(results)):
                        self.vac_history.append(results[i])
                        print(results[i])
                channel.close()


        def getCovidResults(self):
            # Get covid results from GRPC of Clinic
                with grpc.insecure_channel("localhost:50051", options=(('grpc.enable_http_proxy', 0),)) as channel:
                        stub = clinic_control_pb2_grpc.ClinicCtrlStub(channel)
                        covid_Results = stub.getCovidResults(
                                clinic_control_pb2.resultsRequest(name=self.name, hs_num=self.hs_num))
                self.cvd_status = covid_Results.results
                channel.close()
                print(covid_Results.results)




  
def run():
        c = Patient(123,"Anna","11/22/1999")
        c.getVaccineHistory()
        print("Get appt")
        c.get_appointment()
        print("Get Test")
        c.getCovidResults()

if __name__ == '__main__':
        run()