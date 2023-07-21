import mongoose from 'mongoose';
const { Schema, model } = mongoose;

const chatSchema = new Schema(
  {
    userID: {
      type: [Schema.Types.ObjectId],
      ref: 'user',
    },
    email: String,
    msgs: [
      {
        content: {
          type: String,
          trim: true,
          required: true,
        },
        timestamp: Date,
        sender: {
          type: String,
          enum: ['user', 'bot'],
        },
        role: {
          type: String,
          enum: ['system', 'user', 'assistant'],
          default: 'user',
        },
      },
    ],
  },
  { timestamps: true }
);

const Chat = model('chat', chatSchema);

export default Chat;
