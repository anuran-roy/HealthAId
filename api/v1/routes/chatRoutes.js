import express from 'express';
import { getChatById, postMessage } from '../controllers/chatController';

const chatRouter = express.Router();

chatRouter.route('/msg').post(postMessage);
chatRouter.route('/:id').post(getChatById);

export default chatRouter;
