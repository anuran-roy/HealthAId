import express from 'express';
import { loginUser, createUser } from '../controllers/userController';

const userRouter = express.Router();

userRouter
  .route('/login')
  .get((req, res) => {
    res.json({ success: true, responseText: 'user login page' });
  })
  .post(loginUser);

userRouter
  .route('/register')
  .get((req, res) => {
    res.json({ success: true, responseText: 'user register page' });
  })
  .post(createUser);

export default userRouter;
