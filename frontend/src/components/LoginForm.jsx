import styled from 'styled-components';
import React, { useState } from 'react';
import API from './api';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      grant_type: 'password',
      username: formData.username,
      password: formData.password,
      scope: '',
      client_id: '',
      client_secret: '',
    };

    try {
      const response = await API.post('/auth/login', payload, {
        headers: { 'Content-Type': 'application/json' },
      });

      const token = response.data.access_token || response.data.token;
      if (token) localStorage.setItem('token', token);

      alert('Login successful!');
    } catch (error) {
      alert(error.response?.data?.message || error.message);
    }
  };

  return (
    <StyledWrapper>
      <form className="form" onSubmit={handleSubmit}>
        <p className="title">Login</p>
        <p className="message">Enter your credentials to access your account.</p>

        <label>
          <input
            required
            name="username"
            type="text"
            className="input"
            value={formData.username}
            onChange={handleChange}
            placeholder=" "
          />
          <span>Email</span>
        </label>

        <label>
          <input
            required
            name="password"
            type="password"
            className="input"
            value={formData.password}
            onChange={handleChange}
            placeholder=" "
          />
          <span>Password</span>
        </label>

        <button className="submit" type="submit">Login</button>

        <p className="signin">
          Don't have an account? <a href="/register">Register</a>
        </p>
      </form>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  /* Можно использовать тот же CSS, что и для RegisterForm */
`;

export default LoginForm;
