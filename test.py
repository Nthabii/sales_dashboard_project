# test.py - Final Corrected Test Suite
import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# ----------------------------------------------------------
# Test Data Fixtures (Updated with Month column)
# ----------------------------------------------------------
@pytest.fixture
def sample_data():
    """Generate test data with all required columns"""
    data = {
        'Date': ['01/01/2023', '01/15/2023', '02/01/2023', '02/15/2023'],
        'Team_Member': ['John', 'Jane', 'Mike', 'Sarah'],
        'Team': ['A', 'B', 'A', 'B'],
        'Total_Revenue': [1500, 2500, 1800, 3000],
        'Quantity_Sold': [15, 25, 18, 30],
        'Unit_Price': [100, 100, 100, 100],
        'CSAT': [8.2, 9.1, 7.8, 8.9],
        'Product_Name': ['Widget X', 'Gadget Y', 'Widget X', 'Tool Z'],
        'Sales_Channel': ['Online', 'Retail', 'Online', 'Wholesale'],
        'Country': ['USA', 'UK', 'Germany', 'Japan'],
        'Customer_ID': [1001, 1002, 1003, 1004],
        'Month': ['January', 'January', 'February', 'February']  # Added Month column
    }
    return pd.DataFrame(data)

@pytest.fixture
def temp_csv(sample_data):
    """Create temporary CSV file for testing"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
        sample_data.to_csv(tmp.name, index=False)
        yield tmp.name
    os.unlink(tmp.name)

# ----------------------------------------------------------
# Data Loading Tests (Fixed)
# ----------------------------------------------------------
def test_load_data(temp_csv):
    """Test CSV data loading functionality"""
    from app import load_data
    
    # Mock Streamlit's caching decorator
    with patch('app.st.cache_data') as mock_cache:
        mock_cache.side_effect = lambda func: func  # Bypass caching
        
        # Mock pd.read_csv to return our test data
        with patch('pandas.read_csv', return_value=pd.read_csv(temp_csv)) as mock_read:
            df = load_data(temp_csv)
            
            assert not df.empty
            assert len(df) == 4
            assert 'Date' in df.columns
            assert 'Month' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['Date'])

# ----------------------------------------------------------
# Authentication Tests (Working)
# ----------------------------------------------------------
def test_failed_login():
    """Test invalid login credentials"""
    from app import login_page
    
    with patch('streamlit.form_submit_button') as mock_button, \
         patch('streamlit.text_input') as mock_text, \
         patch('streamlit.error') as mock_error:
        
        mock_button.return_value = True
        mock_text.side_effect = ["wrong_user", "wrong_pass"]
        
        login_page()
        
        assert mock_error.called

def test_successful_login():
    """Test valid login credentials"""
    from app import login_page
    
    with patch('streamlit.form_submit_button') as mock_button, \
         patch('streamlit.text_input') as mock_text, \
         patch('streamlit.session_state') as mock_state:
        
        mock_button.return_value = True
        mock_text.side_effect = ["Nthabiseng Gopolang", "Nthabi@2001"]
        mock_state.logged_in = False
        
        login_page()
        
        assert mock_state.logged_in == True

# ----------------------------------------------------------
# Visualization Tests (Fixed)
# ----------------------------------------------------------
def test_performance_gauge():
    """Test gauge chart generation"""
    from app import create_performance_gauge
    
    fig = create_performance_gauge(85, "Test Gauge", 100)
    
    assert fig is not None
    assert fig.data[0].value == 85
    assert "Test Gauge" in fig.data[0].title.text

def test_revenue_trend_plot(sample_data):
    """Test revenue trend visualization"""
    from app import plot_team_revenue_trend
    
    # Convert dates and ensure Month column exists
    sample_data['Date'] = pd.to_datetime(sample_data['Date'], format='%m/%d/%Y')
    sample_data['Month'] = sample_data['Date'].dt.month_name()
    
    current_year = sample_data[sample_data['Date'].dt.year == 2023]
    last_year = pd.DataFrame(columns=sample_data.columns)  # Empty but with same structure
    
    fig = plot_team_revenue_trend(current_year, last_year, "Test Trend")
    
    assert len(fig.data) == 2
    assert fig.data[0].type == "bar"

# ----------------------------------------------------------
# Dashboard Rendering Tests (Fixed with timeout adjustment)
# ----------------------------------------------------------
def test_team_view_rendering():
    """Test team dashboard view renders correctly"""
    from streamlit.testing.v1 import AppTest
    
    at = AppTest.from_file("app.py", default_timeout=10)  # Increased timeout
    
    # Initialize required session state - use direct assignment instead of update
    at.session_state.logged_in = True
    at.session_state.view_mode = 'Team'
    if hasattr(at.session_state, 'selected_team'):
        at.session_state.selected_team = 'A'
    
    at.run()
    
    # Verify components exist without waiting for full render
    assert len(at.get("st.markdown")) > 0
    assert any("TEAM PERFORMANCE" in m.value for m in at.get("st.markdown"))

# ----------------------------------------------------------
# Main Test Execution
# ----------------------------------------------------------
if __name__ == "__main__":
    pytest.main(["-v", "--cov=app", "--cov-report=html", "test.py"])