import pika
import pickle

def book_vac(vac_task):
    # Acquire patient's hs number
    hs_num = vac_task["hs_num"]
    valid_booking = True
    #Open list of booked appointments
    with open("InfoVacc.txt", "r+") as f:
        for line in f:
            book_info = line.split(" ")
            #Check if the patient has already booked an appointment
            if book_info[0] == hs_num:
                valid_booking = False
        #If the booking is valid, add to the list of appointments
        if valid_booking:
            f.write(vac_task["hs_num":"appointment"])

    f.close()
    return valid_booking


def book_test(test_task):
    hs_num = test_task["hs_num"]
    valid_booking = True
    # Open list of booked appointments
    with open("InfoTest.txt", "r+") as f:
        for line in f:
            book_info = line.split(" ")
            # Check if the patient has already booked an appointment
            if book_info[0] == hs_num:
                valid_booking = False
        # If the booking is valid, add to the list of appointments
        if valid_booking:
            f.write(test_task["hs_num":"appointment"])

    f.close()
    return valid_booking


def send_booking(booking_task):
    #Send successful booking to clinic
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Booking-Clinic-Queue')

    channel.basic_publish(exchange='', routing_key='Booking-Clinic-Queue', body=pickle.dumps(booking_task))
    print(" [x] Sending successful booking task to clinic.")

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
                vacResponse = book_vac(booking_task)
                if vacResponse == True:
                    send_booking(booking_task)
        else:
                testResponse = book_test(booking_task)
                if testResponse == True:
                    send_booking(booking_task)

    #Start consuming messages
    channel.basic_consume(queue='Booking-Queue', on_message_callback=callback, auto_ack=True)

    print("Listening for bookings")
    channel.start_consuming()


if __name__ == '__main__':
    main()