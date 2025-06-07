# 🤖 Sales Agent AI Dashboard

A beautiful, real-time dashboard for sales lead management and analytics.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 🚀 **Live Demo**

**Dashboard URL:** [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

## ✨ **Features**

- 📊 **Real-time Overview** - Live metrics and system status
- 🎯 **Lead Management** - Track and manage sales leads
- 📧 **Email Campaigns** - Monitor email performance
- 📈 **Analytics** - Data insights and trends
- ⚙️ **Settings** - Configuration and connection testing

## 🔧 **Local Development**

### **Prerequisites**

- Python 3.11+
- MongoDB database
- OpenAI API key

### **Setup**

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/dashboard-deploy.git
   cd dashboard-deploy
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## 🚀 **Deploy to Streamlit Cloud**

### **One-Click Deployment**

1. **Fork this repository**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Click "New app"**
4. **Select this repository**
5. **Set main file to:** `dashboard.py`
6. **Add your secrets in Advanced Settings:**

```toml
MONGODB_URI = "mongodb+srv://your-connection-string"
OPENAI_API_KEY = "sk-your-openai-key"
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_USER_ID = "your-telegram-user-id"
```

7. **Click Deploy!** 🚀

Your dashboard will be live at: `https://your-app-name.streamlit.app`

## 🔐 **Environment Variables**

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGODB_URI` | ✅ Yes | MongoDB connection string |
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for AI features |
| `TELEGRAM_BOT_TOKEN` | ❌ Optional | For notification alerts |
| `TELEGRAM_USER_ID` | ❌ Optional | Your Telegram user ID |

## 📊 **Dashboard Pages**

### **📈 Overview**
- Real-time metrics and KPIs
- System status indicators  
- Activity charts

### **🎯 Lead Management**
- View recent leads
- Lead details and scoring
- Status tracking

### **📧 Email Campaigns**
- Email statistics
- Success/failure rates
- Recent email logs

### **📈 Analytics**
- Historical data trends
- Performance insights
- Data visualizations

### **⚙️ Settings**
- Configuration status
- Connection testing
- System information

## 🛡️ **Security**

- ✅ **No hardcoded secrets** - All sensitive data via environment variables
- ✅ **Streamlit Cloud security** - Secure secrets management
- ✅ **HTTPS by default** - SSL encryption included
- ✅ **Minimal dependencies** - Reduced attack surface

## 🆓 **Cost**

**100% FREE** when deployed on Streamlit Community Cloud!

- No monthly fees
- No credit card required
- Unlimited usage for public repositories

## 📞 **Support**

- 📖 **Documentation:** [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- 🐛 **Issues:** [Report bugs](https://github.com/your-username/dashboard-deploy/issues)
- 💬 **Community:** [Streamlit Community](https://discuss.streamlit.io)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using [Streamlit](https://streamlit.io)** 