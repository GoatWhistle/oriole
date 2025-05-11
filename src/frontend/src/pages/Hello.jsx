import React, { useEffect, useState } from 'react';
import Header from "/src/components/Header.jsx";

export default function Hello() {
  const [data, setData] = useState({ message: '' });

  useEffect(() => {
    fetch('/api/v1/hello')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
      <Header />
  );
}
