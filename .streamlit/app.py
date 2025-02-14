import streamlit as st
import datetime
from PIL import Image
import json

# Configure the page
st.set_page_config(page_title="Luxury Car Rentals", layout="wide")

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
        transform: translateY(-1px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stDateInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 0.75rem;
        background-color: white;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Cards */
    .car-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .car-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Category pills */
    .category-pill {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background-color: #F3F4F6;
        color: #4B5563;
        margin-right: 0.5rem;
        font-size: 0.875rem;
        cursor: pointer;
    }
    .category-pill:hover {
        background-color: #E5E7EB;
    }
    
    /* Price tags */
    .price-tag {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
    }
    
    /* Location text */
    .location-text {
        color: #6B7280;
        font-size: 0.875rem;
    }
    
    /* Success messages */
    .success-message {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample car data with images
cars = {
    'Lamborghini Urus': {
        'price': 2500,
        'location': 'Dubai Marina',
        'category': 'Luxury',
        'available': True,
        'image': 'https://images.unsplash.com/photo-1675603180863-6a458c699e75',
        'description': 'Ultra-luxury SUV with supercar performance',
        'specs': {'Power': '650 HP', 'Speed': '0-60 mph in 3.6s', 'Seats': '5'}
    },
    'Range Rover Sport': {
        'price': 1800,
        'location': 'Dubai Marina',
        'category': 'SUV',
        'available': True,
        'image': 'https://images.unsplash.com/photo-1675364232562-c990b2cacdb3',
        'description': 'Luxury SUV combining comfort and capability',
        'specs': {'Power': '523 HP', 'Speed': '0-60 mph in 4.3s', 'Seats': '5'}
    },
    'Ferrari F8': {
        'price': 3000,
        'location': 'Dubai Marina',
        'category': 'Sports',
        'available': True,
        'image': 'https://images.unsplash.com/photo-1675603180863-6a458c699e75',
        'description': 'Mid-engine sports car with incredible performance',
        'specs': {'Power': '710 HP', 'Speed': '0-60 mph in 2.9s', 'Seats': '2'}
    }
}

def welcome_page():
    st.markdown("""
        <div style='text-align: center; padding: 4rem 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 2rem;'>Luxury Car Rentals</h1>
            <p style='font-size: 1.25rem; color: #4B5563; margin-bottom: 3rem;'>
                Experience the finest automobiles Dubai has to offer
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login", key="login_main"):
            st.session_state.page = 'login'
        st.write("")
        if st.button("Create Account", key="signup_main"):
            st.session_state.page = 'signup'

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome Back</h1>", unsafe_allow_html=True)
        email = st.text_input("Email/Phone")
        password = st.text_input("Password", type="password")
        st.write("")
        
        if st.button("Login", key="login_submit"):
            st.session_state.logged_in = True
            st.session_state.page = 'browse_cars'
            st.rerun()
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Forgot Password?", key="forgot_pwd"):
            st.session_state.page = 'reset_password'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def browse_cars_page():
    st.markdown("<h1>Find your perfect ride</h1>", unsafe_allow_html=True)
    
    # Search and filters
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Search cars", placeholder="e.g., 'Lamborghini'")
    
    # Category filters
    st.markdown("""
        <div style='margin: 1rem 0;'>
            <span class='category-pill'>All</span>
            <span class='category-pill'>Luxury</span>
            <span class='category-pill'>SUV</span>
            <span class='category-pill'>Sports</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Car listings
    car_cols = st.columns(3)
    for idx, (car, details) in enumerate(cars.items()):
        if search.lower() in car.lower() and details['available']:
            with car_cols[idx % 3]:
                st.markdown(f"""
                    <div class='car-card'>
                        <img src='{details["image"]}' style='width: 100%; height: 200px; object-fit: cover; border-radius: 8px;'>
                        <h3 style='margin: 1rem 0;'>{car}</h3>
                        <p class='location-text'>{details["location"]}</p>
                        <p class='price-tag'>AED {details["price"]}/day</p>
                        <div style='margin-top: 1rem;'>
                            <span style='background: #F3F4F6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.875rem;'>
                                {details["category"]}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {car}", key=f"select_{car}"):
                    st.session_state.selected_car = car
                    st.session_state.page = 'car_details'
                    st.rerun()

def car_details_page():
    car = st.session_state.selected_car
    details = cars[car]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image(details['image'], use_column_width=True)
        
    with col2:
        st.markdown(f"""
            <div style='padding: 2rem;'>
                <h1>{car}</h1>
                <p class='price-tag'>AED {details['price']}/day</p>
                <p class='location-text'>{details['location']}</p>
                <p>{details['description']}</p>
                
                <div style='margin: 2rem 0;'>
                    <h3>Specifications</h3>
                    {''.join(f"<p><strong>{k}:</strong> {v}</p>" for k, v in details['specs'].items())}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Book Now", key="book_now"):
            st.session_state.page = 'booking'
            st.rerun()

def booking_page():
    car = st.session_state.selected_car
    details = cars[car]
    
    st.markdown(f"<h1>Book {car}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pickup_date = st.date_input("Pick-up Date")
        pickup_time = st.time_input("Pick-up Time")
    with col2:
        return_date = st.date_input("Return Date")
        return_time = st.time_input("Return Time")
    
    location = st.selectbox("Pick-up Location", ["Dubai Marina", "Downtown Dubai", "Palm Jumeirah"])
    
    st.markdown("<h3>Payment Details</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Card Number")
    with col2:
        st.text_input("CVV")
    
    if st.button("Confirm Booking", key="confirm_booking"):
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
    details = st.session_state.booking_details
    
    st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <div style='background-color: #DEF7EC; width: 80px; height: 80px; border-radius: 40px; margin: 0 auto; display: flex; align-items: center; justify-content: center;'>
                <span style='font-size: 2rem;'>✓</span>
            </div>
            <h1 style='margin: 2rem 0;'>Booking Confirmed!</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='max-width: 600px; margin: 0 auto; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3>Booking Summary</h3>
            <p><strong>Car:</strong> {details['car']}</p>
            <p><strong>Date:</strong> {details['date']}</p>
            <p><strong>Location:</strong> {details['location']}</p>
            <p><strong>Total:</strong> AED {details['total']}</p>
        </div>
    """, unsafe_allow_html=True)

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
