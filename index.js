import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import connectDB from './config/db.js';
import userRouter from './api/v1/routes/userRoutes.js';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
const httpServer = createServer(app);
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
const io = new Server(httpServer, corsOptions);
io.on('connection', (socket) => {
  console.log(socket);
});

// chat socket
const chatSocket = io.of('/chat');
chatSocket.on('connection', (socket) => {
  console.log('someone connected', socket);
});
chatSocket.on('message', (message) => {
  console.log('message received', message);
  chatSocket.emit('received-this', message);
});

connectDB();


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
httpServer.listen(PORT, () => console.log(`Server is listening on ${PORT}`));
// app.listen(PORT, () => console.log(`Server is listening on ${PORT}`));
