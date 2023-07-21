import User from '../models/UserModel.js';
import Chat from '../models/ChatModel.js';
import axios from 'axios';

/**
 * @param {*} req
 * @param {*} res
 * Retrieve the chat messages from the ID provided in the request body.
 * @returns {Object} All the chat messages with the given id
 */
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

/**
 * @param {*} req
 * @param {*} res
 * Runs everytie a message is posted by the user. Save the message in the database. Post the entire chat, latest message, and sources to the python backend and get the response. Save the response from the bot in the database, and return the result
 */
export const postMessage = async (req, res) => {
  const { uid, cid, message, sources } = req.body;
  console.log(uid, cid, message, sources);
  // save user msg
  try {
    let chat;
    const user = await User.findById(uid);
    if (!cid) {
      // create a new chat
      chat = new Chat({ userID: uid, email: user._id });
      const obj = {
        sender: 'user',
        role: 'system',
        timestamp: new Date(),
        content: message,
      };
      chat.msgs.push(obj);
      await chat.save();
      // make req to py backend
      console.log('CHAT', chat);
    } else {
      chat = await Chat.findById(cid);
      chat.msgs.push({
        sender: 'user',
        role: 'user',
        timestamp: new Date(),
        content: message,
      });
      await chat.save();
    }

    const pybackendData = { ...chat, sources };
    const pyres = await axios.post(
      'https://hackrx-llms-api.anuranroy1.repl.co/get_prompt',
      pybackendData
    );
    let botreply = '';
    let role = pyres?.data[0]?.message?.role;
    for (let i = 0; i < pyres.data.length; i++) {
      botreply += pyres?.data[i]?.message.content;
    }
    console.log(role, botreply);
    const botobj = {
      sender: 'bot',
      role: 'assistant',
      timestamp: new Date(),
      content: botreply,
    };
    chat.msgs.push(botobj);
    await chat.save();
    if (!cid) {
      user.chats.push(chat);
      await user.save();
    }
    res.json({
      success: true,
      responseText: 'chat posted',
      botreply,
      role,
      chat,
    });
  } catch (error) {
    console.log(error);
    res.json({ success: false, responseText: 'there was an error', error });
  }
};
