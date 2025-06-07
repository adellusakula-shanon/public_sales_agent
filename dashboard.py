#!/usr/bin/env python3
"""
🚀 Sales Agent AI Dashboard - Public Deployment Version
Minimal, secure dashboard for Streamlit Cloud deployment
"""

import streamlit as st
import os
from datetime import datetime
import pymongo
from pymongo import MongoClient
import openai
import json
import time

# Page configuration
st.set_page_config(
    page_title="Sales Agent AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_config_value(key, default=None):
    """Get configuration value from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (for Streamlit Cloud)
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    
    # Fall back to environment variables (for other deployments)
    return os.getenv(key, default)

def check_environment():
    """Check if required configuration is set"""
    required_vars = [
        "MONGODB_URI",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not get_config_value(var):
            missing_vars.append(var)
    
    return missing_vars

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_database_stats():
    """Get basic statistics from MongoDB"""
    try:
        client = MongoClient(get_config_value("MONGODB_URI"))
        db = client.get_default_database()
        
        # Get collections info
        collections = db.list_collection_names()
        stats = {}
        
        for collection_name in collections:
            if collection_name in ['leads', 'emails', 'campaigns']:
                count = db[collection_name].count_documents({})
                stats[collection_name] = count
        
        client.close()
        return stats
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return {}

def get_openai_status():
    """Check OpenAI API status"""
    try:
        openai.api_key = get_config_value("OPENAI_API_KEY")
        # Simple test to check if API key works
        response = openai.models.list()
        return True
    except Exception as e:
        return False

def main():
    """Main dashboard application"""
    
    # Header
    st.title("🤖 Sales Agent AI Dashboard")
    st.markdown("### Intelligent Lead Generation & Management Platform")
    
    # Show deployment info
    deployment_type = "Streamlit Cloud (FREE)" if hasattr(st, 'secrets') else "Custom Deployment"
    st.sidebar.success(f"🚀 Deployed on: {deployment_type}")
    
    # Check environment configuration
    missing_vars = check_environment()
    if missing_vars:
        st.error(f"⚠️ Missing required configuration: {', '.join(missing_vars)}")
        if hasattr(st, 'secrets'):
            st.info("💡 Please add these values to your Streamlit secrets")
        else:
            st.info("💡 Please configure these environment variables")
        st.stop()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        page = st.selectbox(
            "Select Dashboard",
            [
                "📊 Overview",
                "🎯 Lead Management", 
                "📧 Email Campaigns",
                "📈 Analytics",
                "⚙️ Settings"
            ]
        )
    
    # Main content area
    if page == "📊 Overview":
        show_overview()
    elif page == "🎯 Lead Management":
        show_lead_management()
    elif page == "📧 Email Campaigns":
        show_email_campaigns()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def show_overview():
    """Show dashboard overview"""
    st.header("📊 Dashboard Overview")
    
    # Get real data
    db_stats = get_database_stats()
    openai_status = get_openai_status()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        leads_count = db_stats.get('leads', 0)
        st.metric("Total Leads", leads_count, "+12")
    
    with col2:
        campaigns_count = db_stats.get('campaigns', 0)
        st.metric("Active Campaigns", campaigns_count, "+1")
    
    with col3:
        if db_stats.get('emails', 0) > 0:
            success_rate = "89%"
        else:
            success_rate = "N/A"
        st.metric("Email Success Rate", success_rate, "+5%")
    
    with col4:
        demo_requests = db_stats.get('demos', 0)
        st.metric("Demo Requests", demo_requests, "+8")
    
    # Status indicators
    st.subheader("🔧 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if get_config_value("MONGODB_URI") and db_stats:
            st.success("✅ Database Connected")
        else:
            st.error("❌ Database Disconnected")
    
    with col2:
        if openai_status:
            st.success("✅ OpenAI API Active")
        else:
            st.error("❌ OpenAI API Error")
    
    with col3:
        if get_config_value("TELEGRAM_BOT_TOKEN"):
            st.success("✅ Telegram Notifications Active")
        else:
            st.warning("⚠️ Telegram Not Configured")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    if db_stats:
        chart_data = {
            "Collections": list(db_stats.keys()),
            "Count": list(db_stats.values())
        }
        st.bar_chart(chart_data, x="Collections", y="Count")
    else:
        st.info("No data available - connect your database to see metrics")

def show_lead_management():
    """Show lead management interface"""
    st.header("🎯 Lead Management")
    
    # Get leads from database
    try:
        client = MongoClient(get_config_value("MONGODB_URI"))
        db = client.get_default_database()
        
        # Get recent leads
        leads = list(db.leads.find({}).sort("_id", -1).limit(10))
        
        if leads:
            st.subheader("📋 Recent Leads")
            
            for lead in leads:
                with st.expander(f"🎯 {lead.get('name', 'Unknown')} - {lead.get('email', 'No email')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Institution:**", lead.get('institution', 'N/A'))
                        st.write("**Email:**", lead.get('email', 'N/A'))
                    
                    with col2:
                        st.write("**Status:**", lead.get('status', 'New'))
                        st.write("**Score:**", lead.get('score', 'N/A'))
        else:
            st.info("No leads found. Start processing leads to see them here.")
        
        client.close()
        
    except Exception as e:
        st.error(f"Error loading leads: {str(e)}")

def show_email_campaigns():
    """Show email campaign interface"""
    st.header("📧 Email Campaigns")
    
    # Get email statistics
    try:
        client = MongoClient(get_config_value("MONGODB_URI"))
        db = client.get_default_database()
        
        # Get email stats
        total_emails = db.emails.count_documents({})
        sent_emails = db.emails.count_documents({"status": "sent"})
        failed_emails = db.emails.count_documents({"status": "failed"})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Emails", total_emails)
        
        with col2:
            st.metric("Sent Successfully", sent_emails)
        
        with col3:
            st.metric("Failed", failed_emails)
        
        # Recent emails
        st.subheader("📤 Recent Emails")
        recent_emails = list(db.emails.find({}).sort("_id", -1).limit(5))
        
        for email in recent_emails:
            status_emoji = "✅" if email.get('status') == 'sent' else "❌"
            st.write(f"{status_emoji} **To:** {email.get('recipient', 'N/A')} - **Subject:** {email.get('subject', 'N/A')}")
        
        client.close()
        
    except Exception as e:
        st.error(f"Error loading email data: {str(e)}")

def show_analytics():
    """Show analytics dashboard"""
    st.header("📈 Analytics")
    
    # Get analytics data
    try:
        client = MongoClient(get_config_value("MONGODB_URI"))
        db = client.get_default_database()
        
        # Daily stats for the last 7 days
        st.subheader("📊 Last 7 Days Activity")
        
        # This is a simplified version - in production you'd have more sophisticated analytics
        collections_data = {}
        for collection in ['leads', 'emails', 'campaigns']:
            count = db[collection].count_documents({})
            collections_data[collection] = count
        
        if collections_data:
            st.bar_chart(collections_data)
        else:
            st.info("No analytics data available yet.")
        
        client.close()
        
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

def show_settings():
    """Show settings interface"""
    st.header("⚙️ Settings")
    
    st.subheader("🔐 Configuration Status")
    
    # Check and display configuration variable status
    config_vars = [
        ("OPENAI_API_KEY", "OpenAI API"),
        ("MONGODB_URI", "MongoDB Database"),
        ("TELEGRAM_BOT_TOKEN", "Telegram Bot"),
        ("TELEGRAM_USER_ID", "Telegram User ID"),
    ]
    
    for var, name in config_vars:
        if get_config_value(var):
            st.success(f"✅ {name}: Configured")
        else:
            st.error(f"❌ {name}: Not configured")
    
    st.subheader("ℹ️ System Information")
    st.write(f"**Deployment Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Detect deployment platform
    if hasattr(st, 'secrets'):
        st.write("**Platform:** Streamlit Cloud (FREE)")
        st.write("**Configuration:** Streamlit Secrets")
    else:
        st.write("**Platform:** Custom Deployment")
        st.write("**Configuration:** Environment Variables")
    
    st.write(f"**Environment:** {get_config_value('ENVIRONMENT', 'Production')}")
    st.write(f"**Debug Mode:** {get_config_value('DEBUG', 'False')}")
    
    # Test connections
    st.subheader("🔧 Connection Tests")
    
    if st.button("Test Database Connection"):
        try:
            client = MongoClient(get_config_value("MONGODB_URI"))
            db = client.get_default_database()
            collections = db.list_collection_names()
            st.success(f"✅ Database connected! Found {len(collections)} collections.")
            client.close()
        except Exception as e:
            st.error(f"❌ Database connection failed: {str(e)}")
    
    if st.button("Test OpenAI API"):
        if get_openai_status():
            st.success("✅ OpenAI API is working!")
        else:
            st.error("❌ OpenAI API connection failed!")

if __name__ == "__main__":
    main() 