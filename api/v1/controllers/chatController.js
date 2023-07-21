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
    let chat;
    const user = await User.findById(uid);
    if (!cid) {
      // create a new chat
      chat = new Chat({ userID: uid, email: user._id });
      const obj = {
        sender: 'user',
        role: 'user',
        timestamp: new Date(),
        content: message,
      };
      chat.msgs.push(obj);
      await chat.save();
      // make req to py backend
      console.log('CHAT', chat);
      const pyres = await axios.post(
        'https://hackrx-llms-api.anuranroy1.repl.co/get_prompt',
        chat
      );
      console.log(pyres.data);
      return res.json({ success: true, data: pyres.data });
    }
    chat = await Chat.findById(cid);
    chat.msgs.push({
      sender: 'user',
      role: 'user',
      timestamp: new Date(),
      content: message,
    });
    await chat.save();
    const pyres = await axios.post(
      'https://hackrx-llms-api.anuranroy1.repl.co/get_prompt',
      chat
    );
    console.log(pyres.data);
    res.json({ success: true, data: pyres.data });
    // send message to python backend and wait for response
    // update chat to add the python backend response
    // send the reponse to the frontend (include chat id)
  } catch (error) {
    console.log(error);
    res.json({ success: false, responseText: 'there was an error', error });
  }
};
