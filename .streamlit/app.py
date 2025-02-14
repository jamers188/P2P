import streamlit as st
import datetime
from PIL import Image
import json

# Configure the page
st.set_page_config(page_title="Luxury Car Rentals", layout="wide")

# Initialize all session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = None
if 'booking_details' not in st.session_state:
    st.session_state.booking_details = None
if 'category' not in st.session_state:
    st.session_state.category = None

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main container */
    .main > div {
        padding: 2rem 3rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #593CFB;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        width: 100%;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #4930E3;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stDateInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 0.75rem;
        background-color: white;
    }
    
    /* Cards */
    .car-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample car data
cars = {
    'Lamborghini Urus': {
        'price': 2500,
        'location': 'Dubai Marina',
        'category': 'Luxury',
        'available': True,
        'description': 'Ultra-luxury SUV with supercar performance',
        'specs': {'Power': '650 HP', 'Speed': '0-60 mph in 3.6s', 'Seats': '5'}
    },
    'Range Rover Sport': {
        'price': 1800,
        'location': 'Dubai Marina',
        'category': 'SUV',
        'available': True,
        'description': 'Luxury SUV combining comfort and capability',
        'specs': {'Power': '523 HP', 'Speed': '0-60 mph in 4.3s', 'Seats': '5'}
    },
    'Ferrari F8': {
        'price': 3000,
        'location': 'Dubai Marina',
        'category': 'Sports',
        'available': True,
        'description': 'Mid-engine sports car with incredible performance',
        'specs': {'Power': '710 HP', 'Speed': '0-60 mph in 2.9s', 'Seats': '2'}
    }
}

def welcome_page():
    st.markdown("<h1 style='text-align: center;'>Luxury Car Rentals</h1>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login", key="login_main"):
            st.session_state.page = 'login'
            st.rerun()
        st.write("")
        if st.button("Create Account", key="signup_main"):
            st.session_state.page = 'signup'
            st.rerun()

def login_page():
    st.title("Welcome Back")
    email = st.text_input("Email/Phone")
    password = st.text_input("Password", type="password")
    st.write("")
    
    if st.button("Login", key="login_submit"):
        st.session_state.logged_in = True
        st.session_state.page = 'browse_cars'
        st.rerun()
    
    st.write("")
    if st.button("Forgot Password?", key="forgot_pwd"):
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
    
    # Category filters
    cols = st.columns(4)
    with cols[0]:
        if st.button("All"):
            st.session_state.category = None
            st.rerun()
    with cols[1]:
        if st.button("Luxury"):
            st.session_state.category = 'Luxury'
            st.rerun()
    with cols[2]:
        if st.button("SUV"):
            st.session_state.category = 'SUV'
            st.rerun()
    with cols[3]:
        if st.button("Sports"):
            st.session_state.category = 'Sports'
            st.rerun()
    
    st.write("---")
    
    # Car listings
    car_cols = st.columns(3)
    col_idx = 0
    
    for car, details in cars.items():
        show_car = True
        if search:
            show_car = search.lower() in car.lower()
        if st.session_state.category:
            show_car = show_car and details['category'] == st.session_state.category
            
        if show_car and details['available']:
            with car_cols[col_idx % 3]:
                with st.container():
                    st.markdown(f"""
                        <div class='car-card'>
                            <h3>{car}</h3>
                            <p style='color: #666;'>{details['location']}</p>
                            <p style='font-size: 1.2rem; font-weight: 600;'>AED {details['price']}/day</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Select {car}", key=f"select_{car}"):
                        st.session_state.selected_car = car
                        st.session_state.page = 'car_details'
                        st.rerun()
            col_idx += 1

def car_details_page():
    if not st.session_state.selected_car:
        st.session_state.page = 'browse_cars'
        st.rerun()
        
    car = st.session_state.selected_car
    details = cars[car]
    
    st.title(car)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div class='car-card'>
                <h3>Specifications</h3>
                {''.join(f"<p><strong>{k}:</strong> {v}</p>" for k, v in details['specs'].items())}
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class='car-card'>
                <h3>Price</h3>
                <p style='font-size: 1.5rem; font-weight: 600;'>AED {details['price']}/day</p>
                <p>{details['location']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Book Now", key="book_now"):
            st.session_state.page = 'booking'
            st.rerun()

def booking_page():
    if not st.session_state.selected_car:
        st.session_state.page = 'browse_cars'
        st.rerun()
        
    car = st.session_state.selected_car
    details = cars[car]
    
    st.title(f"Book {car}")
    
    col1, col2 = st.columns(2)
    with col1:
        pickup_date = st.date_input("Pick-up Date")
        pickup_time = st.time_input("Pick-up Time")
    with col2:
        return_date = st.date_input("Return Date")
        return_time = st.time_input("Return Time")
    
    location = st.selectbox("Location", ["Dubai Marina", "Downtown Dubai", "Palm Jumeirah"])
    payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card"])
    
    if st.button("Confirm Booking"):
        days = (return_date - pickup_date).days
        if days < 1:
            st.error("Return date must be after pickup date")
        else:
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
    if not st.session_state.booking_details:
        st.session_state.page = 'browse_cars'
        st.rerun()
        
    details = st.session_state.booking_details
    
    st.success("🎉 Booking Confirmed!")
    
    st.markdown(f"""
        <div class='car-card'>
            <h2>Booking Summary:</h2>
            <p><strong>Car:</strong> {details['car']}</p>
            <p><strong>Date:</strong> {details['date']}</p>
            <p><strong>Location:</strong> {details['location']}</p>
            <p><strong>Total:</strong> AED {details['total']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Book Another Car"):
        st.session_state.page = 'browse_cars'
        st.session_state.selected_car = None
        st.session_state.booking_details = None
        st.rerun()

def main():
    pages = {
        'welcome': welcome_page,
        'login': login_page,
        'signup': signup_page,
        'reset_password': reset_password_page,
        'browse_cars': browse_cars_page,
        'car_details': car_details_page,
        'booking': booking_page,
        'confirmation': confirmation_page
    }
    
    current_page = st.session_state.page
    if current_page in pages:
        pages[current_page]()

if __name__ == "__main__":
    main()
