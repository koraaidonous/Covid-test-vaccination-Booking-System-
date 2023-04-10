import pika
import pickle
import random

def book_vac(vac_task):
    # Acquire patient's hs number
    hs_num = vac_task["hs_num"]
    valid_booking = True
    #Open list of booked appointments
    with open("InfoApt.txt", "r+") as f:
        for line in f:
            book_info = line.split(" ")
            #Check if the patient has already booked an appointment
            if book_info[0] == hs_num:
                valid_booking = False
        #If the booking is valid, add to the list of appointments
        ''' if valid_booking:
            f.write("\n"+str(vac_task["hs_num"]+" "+vac_task["vac_type"] + " " + vac_task["date"]))'''
    f.close()
    return valid_booking


def book_test(test_task):
    hs_num = test_task["hs_num"]
    valid_booking = True
    # Open list of booked appointments
    with open("InfoApt.txt", "r+") as f:
        for line in f:
            book_info = line.split(" ")
            # Check if the patient has already booked an appointment
            if book_info[0] == hs_num:
                valid_booking = False
        # If the booking is valid, add to the list of appointments
        ''' if valid_booking:
            f.write("\n"+str(test_task["hs_num"])+" "+ test_task[" "])'''
    f.close()
    return valid_booking


def send_booking(booking_task):
    #Send successful booking to clinic
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Booking-Clinic-Queue')

    channel.basic_publish(exchange='', routing_key='Booking-Clinic-Queue', body=pickle.dumps(booking_task))
    print(" [x] Sending successful booking task to clinic.")

    # #Send booking successful message back to patient
    # channel.queue_declare(queue='Response-Queue')
    #
    # channel.basic_publish(exchange='', routing_key='Response-Queue', body='Booking was a success')

    connection.close()


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Booking-Queue')

    def callback(ch, method, properties, body):
        #store booking in database, send confirmation
        print(" [x] Received %r" % body)
        #Pickle parses the message
        booking_task = pickle.loads(body)
        # check type of booking and act accordingly
        if booking_task["book_type"] == "vaccine":
                print("booking vaccine")
                vacResponse = book_vac(booking_task)
                if vacResponse == True:
                    send_booking(booking_task)
                    message = "Vaccine booking approved."
        else:
                print("booking covid test")
                testResponse = book_test(booking_task)
                if testResponse == True:
                    send_booking(booking_task)
                    message = "Covid test booking approved."
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='Response-Queue')
        channel.basic_publish(exchange='', routing_key='Response-Queue', body=pickle.dumps(message))
        print(" [x] Sending successful booking task to patient.")
        connection.close()

    #Start consuming messages
    channel.basic_consume(queue='Booking-Queue', on_message_callback=callback, auto_ack=True)

    print("Listening for bookings")
    channel.start_consuming()


if __name__ == '__main__':
    main()