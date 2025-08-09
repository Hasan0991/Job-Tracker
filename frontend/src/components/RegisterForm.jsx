import styled from 'styled-components';
import React, { useState } from 'react';
import API from "./api";
const RegisterForm = () => {
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    try {
      const response = await API.post('/auth/register', formData);
      alert('Registration successful!');
      setFormData({
        firstname: '',
        lastname: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    } catch (error) {
      alert(error.response?.data?.message || error.message);
    }
  };

  return (
    <StyledWrapper>
      <form className="form" onSubmit={handleSubmit}>
        <p className="title">Register</p>
        <p className="message">Signup now and get full access to our app.</p>
        <div className="flex">
          <label>
            <input
              required
              name="firstname"
              type="text"
              className="input"
              value={formData.firstname}
              onChange={handleChange}
              placeholder=" "
            />
            <span>Firstname</span>
          </label>
          <label>
            <input
              required
              name="lastname"
              type="text"
              className="input"
              value={formData.lastname}
              onChange={handleChange}
              placeholder=" "
            />
            <span>Lastname</span>
          </label>
        </div>
        <label>
          <input
            required
            name="email"
            type="email"
            className="input"
            value={formData.email}
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
        <label>
          <input
            required
            name="confirmPassword"
            type="password"
            className="input"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder=" "
          />
          <span>Confirm password</span>
        </label>
        <button className="submit" type="submit">Submit</button>
        <p className="signin">
          Already have an account? <a href="#">Signin</a>
        </p>
      </form>
    </StyledWrapper>
    
  );
};


const StyledWrapper = styled.div`
  .form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 350px;
    background-color: #fff;
    padding: 20px;
    border-radius: 20px;
    position: relative;
  }

  .title {
    font-size: 28px;
    color: royalblue;
    font-weight: 600;
    letter-spacing: -1px;
    position: relative;
    display: flex;
    align-items: center;
    padding-left: 30px;
  }

  .title::before,.title::after {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    border-radius: 50%;
    left: 0px;
    background-color: royalblue;
  }

  .title::before {
    width: 18px;
    height: 18px;
    background-color: royalblue;
  }

  .title::after {
    width: 18px;
    height: 18px;
    animation: pulse 1s linear infinite;
  }

  .message, .signin {
    color: rgba(88, 87, 87, 0.822);
    font-size: 14px;
  }

  .signin {
    text-align: center;
  }

  .signin a {
    color: royalblue;
  }

  .signin a:hover {
    text-decoration: underline royalblue;
  }

  .flex {
    display: flex;
    width: 100%;
    gap: 6px;
  }

  .form label {
    position: relative;
  }

  .form label .input {
    width: 100%;
    padding: 10px 10px 20px 10px;
    outline: 0;
    border: 1px solid rgba(105, 105, 105, 0.397);
    border-radius: 10px;
  }

  .form label .input + span {
    position: absolute;
    left: 10px;
    top: 15px;
    color: grey;
    font-size: 0.9em;
    cursor: text;
    transition: 0.3s ease;
  }

  .form label .input:placeholder-shown + span {
    top: 15px;
    font-size: 0.9em;
  }

  .form label .input:focus + span,.form label .input:valid + span {
    top: 30px;
    font-size: 0.7em;
    font-weight: 600;
  }

  .form label .input:valid + span {
    color: green;
  }

  .submit {
    border: none;
    outline: none;
    background-color: royalblue;
    padding: 10px;
    border-radius: 10px;
    color: #fff;
    font-size: 16px;
    transform: .3s ease;
  }

  .submit:hover {
    background-color: rgb(56, 90, 194);
  }

  @keyframes pulse {
    from {
      transform: scale(0.9);
      opacity: 1;
    }

    to {
      transform: scale(1.8);
      opacity: 0;
    }
  }`;

export default RegisterForm;
