export async function fetchGroups(token) {
  const res = await fetch("http://127.0.0.1:8000/api/groups/", {
    headers: {
      Authorization: "Bearer " + token,
    },
  });
  if (!res.ok) throw new Error("Не удалось загрузить группы");
  const data = await res.json();
  return data.data;
}
