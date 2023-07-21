import express from 'express';

const chatRouter = express.Router();

chatRouter.route('/msg').post(postMessage);
chatRouter.route('/:id').post(getChatById);

export default chatRouter;
