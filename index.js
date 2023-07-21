import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import connectDB from './config/db';

const app = express();

connectDB();

const corsOptions = {
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: [
    'Access-Control-Allow-Origin',
    'Origin',
    'X-Requested-With',
    'Content-Type',
    'Accept',
    'Authorization',
    'Set-Cookie',
  ],
  credentials: true,
};
// Middlewares
app.options('*', cors(corsOptions));
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes

app.get('/', (req, res) => {
  res.json({
    success: true,
    message: 'Landing page',
  });
});

// new user

app.use('/api/v1/user', userRouter);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server is listening on ${PORT}`));
