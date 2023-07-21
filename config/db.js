import mongoose from 'mongoose';
const { connect, connection } = mongoose;
const dbURL = process.env.MONGODB_URL;

const connectDB = () => {
  connect(dbURL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  const db = connection;
  db.on('error', console.error.bind(console, 'Connection error:'));
  db.once('open', () => {
    console.log('Database connected');
  });
};

export default connectDB;
