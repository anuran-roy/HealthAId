import { createAccessToken } from '../middleware/auth';
import User from '../models/UserModel';

/**
 * @param {*} req
 * Creates a new user
 * @returns {Object} user
 */
const createUser = async (req, res) => {
  // extract data from req body
  const {
    email,
    name,
    avatarURL,
    age,
    gender,
    weight,
    height,
    bloodGrp,
    sources,
  } = req.body;
  try {
    // calculate bmi - weight (kg) / height (m) squared
    const BMI = (weight / Math.pow(height, 2)).toFixed(2);
    const user = new User(
      email,
      name,
      avatarURL,
      age,
      gender,
      weight,
      height,
      BMI,
      bloodGrp,
      sources
    );
    await user.save();
    // generate token - payload -> user id and email
    const token = createAccessToken({ uid: user._id, email: user.email });
    console.log('new user token', token);
    // return response
    res.json({
      success: true,
      responseText: 'user created',
      data: user,
      token,
    });
  } catch (error) {
    console.log(error);
    res.json({
      success: true,
      responseText: 'There was an error',
      msg: error.msg,
      error,
    });
  }
};

/**
 * @param {*} req
 * @param {*} res
 * Checks that if user already exists
 * If user exists - login the user
 * Else - new user is created
 * @returns {Object} Response after user is created or logged in
 */
const loginUser = async (req, res) => {
  // get data from req body
  const { email } = req.body;
  try {
    let user = await User.findOne({ email: email });
    if (user) {
      // create token
      const token = createAccessToken({ uid: user._id, email: user.email });
      return res.json({
        success: true,
        responseText: 'user already exists, logging in',
        data: user,
        token,
      });
    }
    res.json({ success: false, responseText: 'user does not exist' });
  } catch (error) {
    console.log(error);
    return res.json({
      success: false,
      responseText: 'There was an error',
      msg: error.msg,
      error,
    });
  }
};

export default { createUser, loginUser };
