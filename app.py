import streamlit as st

st.title("Hello World")
st.write("Testing deployment...")


'''import streamlit as st
import datetime
from PIL import Image
from db_utils import DBHandler
from car_data import cars
from styles import CUSTOM_CSS

# Initialize database handler
db = DBHandler()

# Configure the page
st.set_page_config(
    page_title="Luxury Car Rentals",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = None
if 'booking_details' not in st.session_state:
    st.session_state.booking_details = None
if 'category' not in st.session_state:
    st.session_state.category = None

def create_navbar():
    col1, col2, col3 = st.columns([2,8,2])
    with col1:
        st.markdown("""
            <div style='padding-top: 1rem;'>
                <h3>Luxury Cars</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.user_email:
            user = db.get_user(st.session_state.user_email)
            st.markdown(f"""
                <div style='text-align: right;'>
                    <p>Welcome, {user['name']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.user_email = None
                st.session_state.page = 'welcome'
                st.rerun()
        else:
            if st.button("Login"):
                st.session_state.page = 'login'
                st.rerun()

def welcome_page():
    st.markdown("""
        <div style='text-align: center; padding: 4rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 1rem;'>Luxury Car Rentals</h1>
            <p style='font-size: 1.25rem; color: #666; margin-bottom: 3rem;'>
                Experience the finest automobiles Dubai has to offer
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Featured cars
    st.markdown("<h2>Featured Vehicles</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (car, details) in enumerate(list(cars.items())[:3]):
        with cols[idx]:
            st.markdown(f"""
                <div class='car-card'>
                    <img src='{details["image"]}' style='width: 100%; height: 200px; object-fit: cover; border-radius: 8px;'>
                    <h3 style='margin: 1rem 0;'>{car}</h3>
                    <p style='color: #666;'>{details["location"]}</p>
                    <p style='font-size: 1.25rem; font-weight: 600;'>AED {details["price"]}/day</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Details", key=f"view_{idx}"):
                if st.session_state.user_email:
                    st.session_state.selected_car = car
                    st.session_state.page = 'car_details'
                else:
                    st.session_state.page = 'login'
                st.rerun()

def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("""
            <div class='auth-form'>
                <h1 style='text-align: center; margin-bottom: 2rem;'>Welcome Back</h1>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if db.verify_login(email, password):
                    st.session_state.user_email = email
                    st.session_state.page = 'browse_cars'
                    st.rerun()
                else:
                    st.error("Invalid email or password")
        
        st.markdown("""
            <div style='text-align: center; margin-top: 1rem;'>
                <p>Don't have an account?</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()

def signup_page():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("""
            <div class='auth-form'>
                <h1 style='text-align: center; margin-bottom: 2rem;'>Create Account</h1>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Create Account", use_container_width=True):
                if password != confirm_password:
                    st.error("Passwords don't match!")
                elif not name or not email or not phone:
                    st.error("Please fill in all fields")
                else:
                    db.add_user(email, password, name, phone)
                    st.session_state.user_email = email
                    st.session_state.page = 'browse_cars'
                    st.rerun()

def browse_cars_page():
    st.markdown("<h1>Find your perfect ride</h1>", unsafe_allow_html=True)
    
    # Search and filters
    with st.container():
        st.markdown("<div class='search-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("Search cars", placeholder="e.g., 'Lamborghini'")
        
        # Category filters
        st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
        cols = st.columns(4)
        categories = ['All', 'Luxury', 'SUV', 'Sports']
        for idx, category in enumerate(categories):
            with cols[idx]:
                if st.button(
                    category,
                    key=f"cat_{category}",
                    use_container_width=True,
                    type="secondary" if st.session_state.category != category else "primary"
                ):
                    st.session_state.category = category if category != 'All' else None
                    st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Car listings
    st.write("")
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
                st.markdown(f"""
                    <div class='car-card'>
                        <img src='{details["image"]}' 
                             style='width: 100%; height: 200px; object-fit: cover; border-radius: 8px;'>
                        <h3 style='margin: 1rem 0;'>{car}</h3>
                        <p style='color: #666;'>{details["location"]}</p>
                        <p style='font-size: 1.25rem; font-weight: 600;'>AED {details["price"]}/day</p>
                        <p style='color: #666; margin: 0.5rem 0;'>{details["description"][:100]}...</p>
                        <div style='margin-top: 1rem;'>
                            <span class='category-pill'>{details["category"]}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("View Details", key=f"select_{car}", use_container_width=True):
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
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div class='car-card'>
                <img src='{details["image"]}' 
                     style='width: 100%; height: 400px; object-fit: cover; border-radius: 8px;'>
                <h1 style='margin: 1rem 0;'>{car}</h1>
                <p style='color: #666; margin-bottom: 2rem;'>{details["description"]}</p>
                
                <h3>Specifications</h3>
                <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0;'>
                    {''.join(f"<div><strong>{k}:</strong> {v}</div>" for k, v in details['specs'].items())}
                </div>
                
                <h3>Features</h3>
                <ul style='columns: 2; margin: 1rem 0;'>
                    {''.join(f"<li>{feature}</li>" for feature in details['features'])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='car-card'>
                <h2>Rental Details</h2>
                <p style='font-size: 2rem; font-weight: 600; margin: 1rem 0;'>
                    AED {details["price"]}<span style='font-size: 1rem; font-weight: normal;'>/day</span>
                </p>
                <p style='color: #666;'>{details["location"]}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Book Now", use_container_width=True):
            st.session_state.page = 'booking'
            st.rerun()

def booking_page():
    if not st.session_state.selected_car:
        st.session_state.page = 'browse_cars'
        st.rerun()
        
    car = st.session_state.selected_car
    details = cars[car]
    
    st.markdown(f"<h1>Book {car}</h1>", unsafe_allow_html=True)
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            pickup_date = st.date_input("Pick-up Date", min_value=datetime.date.today())
            pickup_time = st.time_input("Pick-up Time")
        with col2:
            return_date = st.date_input("Return Date", min_value=pickup_date)
            return_time = st.time_input("Return Time")
        
        location = st.selectbox("Pick-up Location", ["Dubai Marina", "Downtown Dubai", "Palm Jumeirah"])
        
        st.markdown("<h3>Payment Details</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number")
        with col2:
            cvv = st.text_input("CVV", type="password")
        
        if st.form_submit_button("Confirm Booking", use_container_width=True):
            days = (return_date - pickup_date).days
            if days < 1:
                st.error("Return date must be after pickup date")
            else:
                total = days * details['price']
                booking_details = {
                    'car': car,
                    'pickup_date': pickup_date.strftime("%b %d, %Y"),
                    'return_date': return_date.strftime("%b %d, %Y"),
                    'location': location,
                    'total': total,
                    'status': 'confirmed'
                }
                db.add_booking(st.session_state.user_email, booking_details)
                st.session_state.booking_details = booking_details
                st.session_state.page = 'confirmation'
                st.rerun()

def confirmation_page():
    if not st.session_state.booking_details:
        st.session_state.page = 'browse_cars'
        st.rerun()
        
    details = st.session_state.booking_details
    
    st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <div style='background-color: #DEF7EC; width: 80px; height: 80px; border-radius: 40px; 
                      margin: 0 auto; display: flex; align-items: center; justify-content: center;'>
                <span style='font-size: 2rem;'>✓</span>
            </div>
            <h1 style='margin: 2rem 0;'>Booking Confirmed!</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
            <div class='booking-summary'>
                <h2>Booking Summary</h2>
                <div style='margin: 2rem 0;'>
                    <p><strong>Car:</strong> {details['car']}</p>
                    <p><strong>Pick-up Date:</strong> {details['pickup_date']}</p>
                    <p><strong>Return Date:</strong> {details['return_date']}</p>
                    <p><strong>Location:</strong> {details['location']}</p>
                    <p><strong>Total:</strong> AED {details['total']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Book Another Car", use_container_width=True):
            st.session_state.page = 'browse_cars'
            st.session_state.selected_car = None
            st.session_state.booking_details = None
            st.rerun()

def main():
    create_navbar()
    
    pages = {
        'welcome': welcome_page,
        'login': login_page,
        'signup': signup_page,
        'browse_cars': browse_cars_page,
        'car_details': car_details_page,
        'booking': booking_page,
        'confirmation': confirmation_page
    }
    
    current_page = st.session_state.page
    if current_page in pages:
        pages[current_page]()

if __name__ == "__main__":
    main()''''
