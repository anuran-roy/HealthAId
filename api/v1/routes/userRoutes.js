import express from 'express';
import { loginUser } from '../controllers/userController';

const userRouter = express.Router();

userRouter
  .route('/login')
  .get((req, res) => {
    res.json({ success: true, responseText: 'user login page' });
  })
  .post(loginUser);

export default userRouter;
