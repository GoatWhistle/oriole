import { useState } from 'react';
     import { useNavigate } from 'react-router-dom';
     import '../styles/LoginPage.css';

     const API_BASE_URL = 'http://127.0.0.1:8000';

     export default function LoginPage() {
       const navigate = useNavigate();
       const [email, setEmail] = useState('');
       const [password, setPassword] = useState('');
       const [error, setError] = useState('');

       const handleLogin = async e => {
         e.preventDefault();
         setError('');

         try {
           const response = await fetch(`${API_BASE_URL}/api/auth/token`, {
             method: 'POST',
             headers: {
               'Content-Type': 'application/x-www-form-urlencoded',
             },
             body: new URLSearchParams({
               username: email,
               password: password,
             }),
           });

           if (!response.ok) {
             throw new Error('Неверный логин или пароль');
           }

           const data = await response.json();
           localStorage.setItem('access_token', data.access_token);

           const meRes = await fetch(`${API_BASE_URL}/api/auth/me`, {
             headers: {
               Authorization: `Bearer ${data.access_token}`,
             },
           });

           if (!meRes.ok) {
             throw new Error('Ошибка получения данных пользователя');
           }

           const me = await meRes.json();
           localStorage.setItem('user_id', me.id);

           navigate('/groups');
         } catch (err) {
           setError(err.message || 'Ошибка входа');
         }
       };

       return (
         <div className="login-container">
           <form className="login-form" onSubmit={handleLogin}>
             <h2>Вход в Oriole Chat</h2>
             <input
               type="email"
               placeholder="Email"
               value={email}
               required
               onChange={e => setEmail(e.target.value)}
             />
             <input
               type="password"
               placeholder="Пароль"
               value={password}
               required
               onChange={e => setPassword(e.target.value)}
             />
             <button type="submit">Войти</button>
             {error && <p className="error-text">{error}</p>}
           </form>
         </div>
       );
     }
