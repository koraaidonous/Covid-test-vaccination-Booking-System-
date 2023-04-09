from enum import Enum
from fastapi import FastAPI, HTTPException, Response
import grpc
import clinic_control_pb2
import clinic_control_pb2_grpc
import pika
import pickle
from pydantic import BaseModel

app = FastAPI()

class cStat(Enum):
        #Negative tests set to -1
        Neg = -1
        ToTest = 0
        #Positive tests set to 1
        Pos = 1

class logIn (BaseModel):
        hs_num: int
        name: str
        password: str
        dob: str
        cov_status: str

login_Store = []
global curPatient

@app.get('/')
async def root():
        return {"message": "Welcome to the Hospital Management System"}

@app.post('/book/vac')
def book_vac(vac_type: str, clinic: str, date: str, time: str):
        curPatient.book_vaccine(vac_type, clinic, date, time)

@app.post('/book/test')
def book_test(clinic: str, date: str, time: str):
        curPatient.book_covid_test(clinic, date, time)

@app.get('/view/vac')
def view_vac():
        curPatient.getVaccineHistory()

@app.get('/view/test')
def view_test():
        curPatient.getCovidResults()

@app.get('/Login')
def log_in(name:str, password:str):
        # global curPatient
        foundP = False
        for i in login_Store:
                if login_Store[i].name == name:
                        if login_Store[i].password == password:
                                foundP = True
                                curPatient = Patient(login_Store[i].hs_num,name,password,login_Store[i].dob,login_Store[i].cov_status)
                        else:
                                raise HTTPException(status_code=404, detail=f"Wrong password.")
        if not foundP:
                raise HTTPException(status_code=404, detail=f"The user {name} cannot be found.")



@app.put('/SignUp')
def sign_up(name:str, password:str, hs_num:str, dob:str, stat:str):
        createUser = True
        for i in login_Store:
                if login_Store[i].hs_num == hs_num:
                        createUser = False
                        raise HTTPException(status_code=404, detail=f"User already exists.")
                
        if createUser:
                login_Store.append(Patient(hs_num, name, password, dob, stat))
                curPatient = Patient(hs_num, name, password, dob, stat)


class Patient:
        def __init__(self, hs_num, name, password, dob, stat):
                self.hs_num = hs_num
                self.name = name
                self.password = password
                self.dob = dob
                self.cvd_status = stat
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
                self.cvd_status = cStat.ToTest.value
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
        c = Patient(123,"Anna","123", "11/22/1999", "Negative")
        print("GRPC\n Get Vac History")
        c.getVaccineHistory()
        print("Get Appointment")
        c.get_appointment()
        print("Get Test")
        c.getCovidResults()
        print("\nRabbitMQ")
        print("Book Vaccine")
        c.book_vaccine("VacType","Clinic1","MM/DD/YYYY","9am")


if __name__ == '__main__':
        run()