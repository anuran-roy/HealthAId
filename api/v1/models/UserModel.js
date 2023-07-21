import mongoose from 'mongoose';
const { Schema, model } = mongoose;

const userSchema = new Schema(
  {
    email: String,
    name: {
      type: String,
      lowercase: true,
    },
    avatarURL: String,
    age: {
      type: Number,
      min: 0,
      max: 125,
    },
    gender: {
      type: String,
      enum: ['male', 'female', 'others'],
    },
    weight: Number,
    height: Number,
    bloodGrp: {
      type: String,
      uppercase: true,
      enum: ['A+', 'B+', 'O+', 'AB+', 'A-', 'B-', 'O-', 'AB-'],
    },
    BMI: Number,
    theme: {
      type: String,
      default: 'light',
    },
    chats: {
      type: [Schema.Types.ObjectId],
      ref: 'chat',
    },
    sources: [String],
    role: {
      type: String,
      enum: ['admin', 'user'],
      default: 'user',
    },
  },
  { timestamps: true }
);

const User = model('user', userSchema);

export default User;
