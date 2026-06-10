# Vesture AI: Virtual Try-On & Personalized Fashion

![Vesture AI App Showcase](https://i.imgur.com/your-app-showcase-gif.gif)

### An intelligent e-commerce platform that revolutionizes the online shopping experience with AI-powered virtual try-on and a personal stylist recommendation engine.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Manthan--Panseriya-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/manthan-panseriya-237739338/)

---
## 🎬 Demo

[![Watch the Demo](https://img.shields.io/badge/Watch-Demo_Video-red?style=for-the-badge&logo=google-drive)](https://drive.google.com/file/d/1boVufWQ2viYiR351IYX3M2CjgQzubwLB/view?usp=drivesdk)

---

## 🚀 About The Project

Online clothes shopping has two major problems: the uncertainty of **fit and appearance**, and the overwhelming **paradox of choice**. Vesture AI tackles both.

This full-stack MERN & FastAPI application is an end-to-end e-commerce solution that serves both **Buyers** and **Sellers**. Its core innovation lies in its two intelligent systems:

1.  **Virtual Try-On**: Users can upload a photo of themselves to see how a piece of clothing will actually look on their body, drastically reducing the uncertainty that leads to returns.

2.  **Personalized Recommendation Engine**: Going beyond simple filters, the platform acts as a personal stylist. It analyzes a user's unique profile—including skintone, body type, age, and style preferences—to recommend clothes they'll love.

This project is not just a storefront; it's a complete, AI-driven fashion ecosystem.

---

## ✨ Key Features

### For Buyers 🛍️

* **Full Authentication**: Secure sign-up, login, email verification, and password management.
* **AI-Powered Onboarding**: A guided process to capture user data like skintone, body type, and style preferences for a truly personalized experience.
* **Virtual Try-On**: See clothes on your own body before you buy.
* **Personalized Recommendations**: An intelligent stylist that suggests outfits tailored to you.
* **Standard E-commerce Flow**: A complete shopping experience with a cart, checkout, order tracking, and review system.
* **Wishlist**: Save your favorite items for later.

### For Sellers 📈

* **Dedicated Seller Dashboard**: A central hub to manage products, view sales, and track orders.
* **Complete Inventory Management**: Easily add, edit, and manage product listings with detailed forms.
* **Sales Analytics**: A data-rich dashboard providing insights into revenue, items sold, and top-performing products.
* **Order Management**: View and manage incoming orders.

---

## 🛠️ Tech Stack & Architecture

This project is built with a modern, scalable, microservices-inspired architecture to separate the core application logic from the high-performance AI services.

### **Dual-Backend Architecture**

* **E-commerce Backend (Node.js)**: A robust server built with Node.js, Express, and Mongoose to handle all core business logic, including user authentication, product management, orders, and payments.
* **AI Service (Python)**: A high-performance API built with FastAPI to serve the AI models for Virtual Try-On and personalized recommendations.

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-59282A?style=for-the-badge)

---

## ⚙️ Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Node.js (v18 or later)
* npm
* Python (v3.9 or later)
* pip
* MongoDB Atlas account (or local MongoDB instance)

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/Manthan0207/VestureAI.git
    ```

2.  **Setup the Backend (Node.js)**
    ```sh
    cd Server
    npm install
    ```
    Create a `.env` file in the `Server` directory and add the following variables:
    ```env
    # MongoDB Connection String
    MONGO_URI=your_mongodb_connection_string

    # Server Port
    PORT=3000

    # JWT Secret for authentication tokens
    JWT_SECRET=your_super_secret_jwt_key

    # Application Environment
    NODE_ENV=development

    # Frontend URL for CORS
    CLIENT_URL=http://localhost:5173

    # Gmail credentials for sending verification emails
    GMAIL_USER=your_gmail_address@gmail.com
    GMAIL_PASS=your_gmail_app_password

    # Cloudinary credentials for image storage
    CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
    CLOUDINARY_API_KEY=your_cloudinary_api_key
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret
    ```
    Then, start the server:
    ```sh
    npm start
    ```

### Model Weights Notice

The trained model weights used by the AI components of this project are not included in this repository.

These model files have been intentionally excluded from version control. As a result, features such as Virtual Try-On and certain AI-powered recommendations cannot be executed directly from a cloned copy of the repository without the corresponding model weights.

The complete source code, application architecture, API implementation, and integration logic are available for review.

If access to the model weights is required for evaluation, research, or demonstration purposes, please contact me at:

📧 **manthanpanseriya0205@gmail.com**

3.  **Setup the AI Service (FastAPI)**
    ```sh
    cd ML-API
    ```
    It is highly recommended to create a Python virtual environment (`venv`) to avoid global dependency issues.
    ```sh
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    # On MacOS/Linux:
    source venv/bin/activate
    ```
    Now, install the required packages within your activated environment:
    ```sh
    pip install -r requirements.txt
    ```
    Create a `.env` file if needed for any AI service API keys. Start the service:
    ```sh
    uvicorn main:app --reload
    ```

4.  **Setup the Frontend (React)**
    ```sh
    cd client/frontend
    npm install
    ```
    Create a `.env.local` file in the `client/frontend` directory and add your backend server URL:
    ```env
    VITE_SERVER_URL=http://localhost:3000
    ```
    Then, start the frontend development server:
    ```sh
    npm run dev
    ```

---

## 📬 Contact

Manthan Panseriya - [LinkedIn](https://www.linkedin.com/in/manthan-panseriya-237739338/) - manthanpanseriya0205@gmail.com
