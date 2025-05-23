import React, { useEffect, useState } from 'react';
import Header from "/src/components/Header.jsx";
import Verified from "/src/components/Verified.jsx";
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function Verify() {
  const { token } = useParams();
  const [status, setStatus] = useState('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await axios.get(`/api/v1/verify/${token}`);
        setStatus('success');
        setMessage(response.data.message);
      } catch (error) {
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Verification failed');
      }
    };

    verifyEmail();
  }, [token]);

  return (
    <div>
      <Header/>
      {status === 'loading' && <p>Verifying...</p>}
      {status === 'success' && <Verified message={message}/>}
      {status === 'error' && <div className="error">{message}</div>}
    </div>
  );
}
