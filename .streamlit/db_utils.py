import json
import os
from datetime import datetime

class DBHandler:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.bookings_file = 'data/bookings.json'
        self._init_db()
    
    def _init_db(self):
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Initialize users file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        # Initialize bookings file if it doesn't exist
        if not os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'w') as f:
                json.dump([], f)
    
    def get_user(self, email):
        with open(self.users_file, 'r') as f:
            users = json.load(f)
            return users.get(email)
    
    def add_user(self, email, password, name, phone):
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        users[email] = {
            'password': password,  # In production, this should be hashed
            'name': name,
            'phone': phone,
            'created_at': datetime.now().isoformat()
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f)
    
    def verify_login(self, email, password):
        user = self.get_user(email)
        if user and user['password'] == password:
            return True
        return False
    
    def add_booking(self, email, booking_details):
        with open(self.bookings_file, 'r') as f:
            bookings = json.load(f)
        
        booking_details['email'] = email
        booking_details['booking_date'] = datetime.now().isoformat()
        bookings.append(booking_details)
        
        with open(self.bookings_file, 'w') as f:
            json.dump(bookings, f)
    
    def get_user_bookings(self, email):
        with open(self.bookings_file, 'r') as f:
            bookings = json.load(f)
            return [b for b in bookings if b['email'] == email]
