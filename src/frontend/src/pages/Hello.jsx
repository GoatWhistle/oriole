import React, { useEffect, useState } from 'react';

export default function Hello() {
  const [data, setData] = useState({ message: '' });

  useEffect(() => {
    fetch('/api/v1/hello')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '10vh' }}>
      <h1 style={{ fontSize: '3rem' }}>{data.message}</h1>
    </div>
  );
}
