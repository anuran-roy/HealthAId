import express from 'express';
import { getChatById, postMessage } from '../controllers/chatController.js';

const chatRouter = express.Router();

chatRouter.route('/msg').post(postMessage);
chatRouter.route('/:id').get(getChatById);

export default chatRouter;
