import socket
import threading

# Fun runs data
fun_runs = {
    '001': {'name': 'Pier to Pier', 'area': 'NorthEast', 'distance': 7, 'time': 'Fast', 'price_per_runner': 10, 'max_capacity': 50, 'registered_runners': 0},
    '002': {'name': 'York 10KM', 'area': 'York', 'distance': 10, 'time': 'Slow', 'price_per_runner': 5, 'max_capacity': 100, 'registered_runners': 0},
    # Add more runs here...
}

# Lock for thread safety
lock = threading.Lock()

# Function to recommend fun runs based on criteria
def recommend_runs(criteria):
    recommended_runs = []
    for run_id, run_data in fun_runs.items():
        if run_data['area'] == criteria['area'] and \
                criteria['min_length'] <= run_data['distance'] <= criteria['max_length'] and \
                run_data['time'] == criteria['time']:
            recommended_runs.append((run_data['name'], run_data['price_per_runner'], run_id))
    return recommended_runs

# Function to register runners for a run
def register_runners(run_id, quantity):
    with lock:
        if fun_runs[run_id]['registered_runners'] + quantity <= fun_runs[run_id]['max_capacity']:
            fun_runs[run_id]['registered_runners'] += quantity
            return quantity * fun_runs[run_id]['price_per_runner']
        else:
            return 0  # No space available

# Function to handle client requests
def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            parts = data.split()
            if parts[0] == 'RECOMMEND':
                criteria = {
                    'area': parts[1],
                    'min_length': int(parts[2]),
                    'max_length': int(parts[3]),
                    'time': parts[4]
                }
                recommended_runs = recommend_runs(criteria)
                response = '\n'.join([f"{name}, £{price}, {run_id}" for name, price, run_id in recommended_runs])
                client_socket.send(response.encode('utf-8'))
            elif parts[0] == 'REGISTER':
                secretary_name = parts[1]
                orders = parts[2:]
                total_cost = 0
                order_info = []
                for i in range(0, len(orders), 2):
                    run_id = orders[i]
                    quantity = int(orders[i+1])
                    cost = register_runners(run_id, quantity)
                    total_cost += cost
                    order_info.append((run_id, quantity))
                if total_cost > 50:
                    total_cost *= 0.9  # Apply discount
                client_socket.send(f"Total cost: £{total_cost:.2f}".encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

# Main function to start the server
def main():
    host = '127.0.0.1'
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
