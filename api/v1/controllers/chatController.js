import User from '../models/UserModel.js';
import Chat from '../models/ChatModel.js';
import axios from 'axios';

export const getChatById = async (req, res) => {
  const chatID = req.params.id;
  if (!chatID) {
    return res.json({ success: false, responseText: 'invalid chat id' });
  }
  try {
    const chat = await Chat.findById(chatID);
    res.json({ success: true, responseText: 'chat retrieved', chat });
  } catch (error) {
    res.json({ success: false, responseText: 'there was an error', error });
  }
};

export const postMessage = async (req, res) => {
  const { uid, cid, message } = req.body;
  console.log(uid, cid, message);
  // save user msg
  try {
    let chat = await Chat.findById(cid);
    let user;
    if (!chat) {
      // first message of a new chat
      const obj = {
        sender: 'user',
        role: 'user',
        timestamp: new Date(),
        content: message,
      };

      user = await User.findById(uid);
      chat = new Chat({ userID: uid, email: user.email });
      chat.msgs.push(obj);
      await chat.save();
      const pyres = await axios.post(
        'https://hackrx-llms-api.anuranroy1.repl.co/get_prompt',
        chat
      );
      console.log(pyres);
      return res.json({ success: true, pyres });
      // send message to python backend and wait for response
      // update chat to add the python backend response
      // send the reponse to the frontend (include chat id)
    }
    chat.msgs.push({
      sender: 'user',
      role: 'user',
      timestamp: new Date(),
      content: message,
    });
    await chat.save();
    user = await User.findById(uid);
    const pyres = await axios.post(
      'https://hackrx-llms-api.anuranroy1.repl.co/get_prompt',
      chat
    );
    console.log(pyres);
    return res.json({ success: true, pyres });
    // send message to python backend and wait for response
    // update chat to add the python backend response
    // send the reponse to the frontend (include chat id)
  } catch (error) {
    res.json({ success: false, responseText: 'there was an error', error });
  }
};
