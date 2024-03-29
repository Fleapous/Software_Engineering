import React, { useState } from 'react';
import styled from '@emotion/styled';
import { Button, TextField, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LoginStore from '../../api/LoginStore';
import Navbar from '../../components/navbar/Navbar';
const LeftSideImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;

`;

const RightSideForm = styled.div`
  padding: 24px;
  justify-content: center;
`;

const LoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: white;
`;

const LoginTitleContainer = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: black;
  margin-bottom: 100px;
  font-family: Dubai-Medium;
  
`;

const LoginForm = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  width: 400px;
  height:120px;
`;

const LoginButton = styled(Button)`
  width: 150px;
  height: 40px;
  margin-top: 50px;
  border: none;
  border-radius: 5px;
  background-color: black;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-self: center;
  justify-content: center;

  &:hover {
    background-color: grey;
  }
`;

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [loginError,setLoginError] = useState('');

  const navigate = useNavigate();

  const validateEmail = () => {
    // TODO: consider if want to use email or username to login

    // const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // if (!emailRegex.test(email)) {
    //   setEmailError('Invalid email address');
    //   return false;
    // }
    // setEmailError('');
    return true;
  };

  const validatePassword = () => {
    if (password.length < 3) {
      setPasswordError('Password must be at least 3 characters');
      return false;
    }
    setPasswordError('');
    return true;
  };


  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    validateEmail(value);
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);
    validatePassword(value);
  };

  const isValid = () => validateEmail() && validatePassword();

  const fetchData = () =>{
    // TODO: change to email or username and update .login() method

    LoginStore.getState()
      .login(email, password)
      .then(() =>
        {
          navigate('/offices');
        }
      )
      .catch((error) => 
        {
          console.error('Invalid email or password');
          setLoginError("Incorrect Username or Password Entered!")
        })
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!isValid()) {
      return;
    }
    console.log('An email was submitted: ', email);
    console.log('A password was submitted: ', password);
    fetchData();
  };

  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
      <Navbar/>
      <Grid
          item
          xs={false}
          sm={4}
          md={7}
          sx={{
            backgroundImage: 'url(https://theadfocus.com/wp-content/uploads/2022/03/Times-Square-andreas-m-unsplash-scaled.jpg)',
            backgroundRepeat: 'no-repeat',
            backgroundColor: (t) =>
              t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <RightSideForm>
          <LoginContainer>
            <LoginTitleContainer>
              <h1>Welcome to Find Your Space!</h1>
            </LoginTitleContainer>

            <form onSubmit={handleSubmit}>
              <LoginForm>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Username"
                  name="email"
                  autoComplete="email"
                  autoFocus
                  value={email}
                  onChange={handleEmailChange}
                  error={!!emailError}
                  helperText={emailError}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={handlePasswordChange}
                  error={!!passwordError}
                  helperText={passwordError}
                />
                 {loginError && (
                  <p style={{ color: 'red', textAlign: 'center' }}>{loginError}</p>
                )}
                <LoginButton type="submit" centerRipple variant="contained" sx={{ mt: 4, mb: 4 }}>
                  Log in
                </LoginButton>
              </LoginForm>
            </form>
          </LoginContainer>
        </RightSideForm>
      </Grid>
    </Grid>
  );
};

export default Login;