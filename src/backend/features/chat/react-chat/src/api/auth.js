export async function getMe(token) {
  const res = await fetch("http://127.0.0.1:8000/api/auth/me", {
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  if (!res.ok) throw new Error("Ошибка получения пользователя");
  return await res.json();
}
