CUSTOM_CSS = """
    <style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA;
    }
    
    .main {
        background-color: #F8F9FA;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1A1A1A;
    }
    
    /* Cards */
    .car-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1rem;
    }
    
    .car-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #593CFB;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #4930E3;
        transform: translateY(-1px);
    }
    
    /* Navigation Bar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        padding: 0 2rem;
    }
    
    /* Category Pills */
    .category-pill {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        margin-right: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .category-pill:hover {
        background: #F3F4F6;
    }
    
    .category-pill.active {
        background: #593CFB;
        color: white;
        border-color: #593CFB;
    }
    
    /* Forms */
    .auth-form {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Search Bar */
    .search-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Booking Summary */
    .booking-summary {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Success Messages */
    .success-message {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
"""
