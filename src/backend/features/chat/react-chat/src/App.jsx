import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import GroupsPage from "./pages/GroupsPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/groups" element={<GroupsPage />} />
        <Route path="/chat" element={<ChatPage />} />

    </Routes>
  );
}
export default App;
