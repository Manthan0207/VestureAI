import express from 'express';
import { connectDB } from './db/connectDB.js';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.route.js'
import sellerRoutes from './routes/seller.route.js'
import productRoutes from './routes/product.route.js'
import cookieParser from 'cookie-parser';
import cors from 'cors'

dotenv.config()


const app = express();

const PORT = process.env.PORT || 5000



app.use(cors({
    origin: "http://localhost:5173",
    credentials: true //to send cookies in the request from frontend
}))

app.use(express.json({ limit: "10mb" })) //allows us to parse incoming requests : req.body
app.use(cookieParser()) //this will allow us to parse incoming cookies(to use cookies in req obj)

app.use("/api/auth", authRoutes)
app.use("/api/seller", sellerRoutes)
app.use("/api/product", productRoutes)
// app.use("api/user-details", userRouter)

app.listen(3000, () => {
    connectDB()
    console.log(`Server running on ${3000}`);

})

