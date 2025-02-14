import streamlit as st
import datetime
from PIL import Image
import json

# Configure the page
st.set_page_config(page_title="Luxury Car Rentals", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #5B21B6;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
        width: 100%;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        background-color: #F3F4F6;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sample car data
cars = {
    'Lamborghini Urus': {
        'price': 2500,
        'location': 'Dubai Marina',
        'category': 'Luxury',
        'available': True
    },
    'Range Rover Sport': {
        'price': 1800,
        'location': 'Dubai Marina',
        'category': 'SUV',
        'available': True
    },
    'Ferrari F8': {
        'price': 3000,
        'location': 'Dubai Marina',
        'category': 'Sports',
        'available': True
    }
}

def welcome_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Luxury Car Rentals")
        st.write("")
        if st.button("Login"):
            st.session_state.page = 'login'
        st.write("")
        if st.button("Create Account"):
            st.session_state.page = 'signup'

def login_page():
    st.title("Welcome Back")
    email = st.text_input("Email/Phone")
    password = st.text_input("Password", type="password")
    st.write("")
    
    if st.button("Login"):
        # Simulate login logic
        st.session_state.logged_in = True
        st.session_state.page = 'browse_cars'
        st.rerun()
    
    st.write("")
    if st.button("Forgot Password?"):
        st.session_state.page = 'reset_password'
        st.rerun()

def signup_page():
    st.title("Create Account")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Create Account"):
        if password == confirm_password:
            st.success("Account created successfully!")
            st.session_state.logged_in = True
            st.session_state.page = 'browse_cars'
            st.rerun()
        else:
            st.error("Passwords don't match!")

def reset_password_page():
    st.title("Reset Password")
    st.write("Enter your email to reset password")
    email = st.text_input("Email Address")
    
    if st.button("Send Reset Link"):
        st.success("Check your email for password reset instructions")
        st.session_state.page = 'login'
        st.rerun()

def browse_cars_page():
    st.title("Browse Cars")
    search = st.text_input("Search (e.g., 'Lamborghini')")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Luxury"):
            st.session_state.category = 'Luxury'
    with col2:
        if st.button("SUV"):
            st.session_state.category = 'SUV'
    with col3:
        if st.button("Sports"):
            st.session_state.category = 'Sports'
    
    st.subheader("Available Cars")
    for car, details in cars.items():
        if search.lower() in car.lower() and details['available']:
            with st.expander(car):
                st.write(f"Price: AED {details['price']}/day")
                st.write(f"Location: {details['location']}")
                if st.button(f"Select {car}"):
                    st.session_state.selected_car = car
                    st.session_state.page = 'car_details'
                    st.rerun()

def car_details_page():
    st.title("Car Details")
    car = st.session_state.selected_car
    details = cars[car]
    
    st.subheader(car)
    st.write(f"Price: AED {details['price']}/day")
    st.write(f"Location: {details['location']}")
    st.write("Available: Yes")
    
    if st.button("Book Now"):
        st.session_state.page = 'booking'
        st.rerun()

def booking_page():
    st.title("Book Car")
    car = st.session_state.selected_car
    details = cars[car]
    
    pickup_date = st.date_input("Pick-up Date")
    pickup_time = st.time_input("Pick-up Time")
    return_date = st.date_input("Return Date")
    return_time = st.time_input("Return Time")
    location = st.selectbox("Location", ["Dubai Marina", "Downtown Dubai", "Palm Jumeirah"])
    payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
    
    if st.button("Confirm Booking"):
        days = (return_date - pickup_date).days
        total = days * details['price']
        st.session_state.booking_details = {
            'car': car,
            'date': pickup_date.strftime("%b %d, %Y"),
            'location': location,
            'total': total
        }
        st.session_state.page = 'confirmation'
        st.rerun()

def confirmation_page():
    st.title("Booking Confirmed!")
    details = st.session_state.booking_details
    
    st.success("🎉 Booking Confirmed!")
    st.subheader("Booking Summary:")
    st.write(f"Car: {details['car']}")
    st.write(f"Date: {details['date']}")
    st.write(f"Location: {details['location']}")
    st.write(f"Total: AED {details['total']}")

# Main app logic
def main():
    if st.session_state.page == 'welcome':
        welcome_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'signup':
        signup_page()
    elif st.session_state.page == 'reset_password':
        reset_password_page()
    elif st.session_state.page == 'browse_cars':
        browse_cars_page()
    elif st.session_state.page == 'car_details':
        car_details_page()
    elif st.session_state.page == 'booking':
        booking_page()
    elif st.session_state.page == 'confirmation':
        confirmation_page()

if __name__ == "__main__":
    main()
